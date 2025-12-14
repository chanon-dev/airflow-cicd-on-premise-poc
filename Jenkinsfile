pipeline {
    agent any

    // Optional: Keep parameters for "Manual" runs or testing
    parameters {
        choice(name: 'ENV_NAME', choices: ['AUTO', 'DEV', 'UAT', 'PROD'], description: 'Select ENV (AUTO = detect from Job Name)')
    }

    environment {
        // Dynamic Tag based on Git Commit (calculated in Initialize stage or shell)
        // AIRFLOW_IMAGE_NAME will be set dynamically
        COMPOSE_PROJECT_NAME = 'airflow-production' // Default, can be overwritten
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    // Logic to determine Environment
                    def targetEnv = params.ENV_NAME
                    
                    if (targetEnv == 'AUTO' || targetEnv == null) {
                        def jobName = env.JOB_BASE_NAME.toUpperCase()
                        if (jobName.contains('DEV')) targetEnv = 'DEV'
                        else if (jobName.contains('UAT')) targetEnv = 'UAT'
                        else targetEnv = 'PROD'
                    }

                    echo "Deploying to Environment: ${targetEnv}"
                    
                    if (targetEnv == 'DEV') {
                        env.COMPOSE_PROJECT_NAME = 'airflow-dev'
                        env.AIRFLOW_PORT = '8082'
                        env.FLOWER_PORT = '5557'
                    } else if (targetEnv == 'UAT') {
                        env.COMPOSE_PROJECT_NAME = 'airflow-uat'
                        env.AIRFLOW_PORT = '8081'
                        env.FLOWER_PORT = '5556'
                    } else {
                        env.COMPOSE_PROJECT_NAME = 'airflow-prod'
                        env.AIRFLOW_PORT = '8080'
                        env.FLOWER_PORT = '5555'
                    }

                    // Versioning Strategy: Short Git Hash
                    def gitHash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.AIRFLOW_IMAGE_TAG = gitHash
                    env.AIRFLOW_IMAGE_NAME = "my-custom-airflow:${gitHash}"
                    
                    echo "Configured for ${env.COMPOSE_PROJECT_NAME} on Port ${env.AIRFLOW_PORT}"
                    echo "Version: ${env.AIRFLOW_IMAGE_TAG}"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test DAGs') {
            steps {
                script {
                    echo "Running DAG Integrity Tests..."
                    // We need a temporary container with Airflow installed to run the tests.
                    // We can reuse the official image or build a test image.
                    // Simple approach: Build a test image (or the actual image) and run pytest inside it.
                    
                    // 1. Build the image (Testing Phase)
                    sh "docker build -t ${env.AIRFLOW_IMAGE_NAME} ."
                    
                    // 2. Run Pytest inside the container
                    // Mounting tests folder just for this step if it's not in the image yet
                    try {
                        sh """
                            docker run --rm \
                                --entrypoint /bin/bash \
                                -v \$(pwd)/tests:/opt/airflow/tests \
                                ${env.AIRFLOW_IMAGE_NAME} \
                                -c "pip install pytest && pytest /opt/airflow/tests/test_dag_integrity.py"
                        """
                    } catch (Exception e) {
                        error "DAG Tests Failed! Aborting deployment."
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Secure Secrets Handling
                // Assuming you have 'airflow-postgres-creds' (Username/Password) in Jenkins credentials.
                // If not, it falls back to empty, but syntax is valid.
                // For POC, we fallback to defaults if not found.
                script {
                     // Ensure basic .env exist
                    sh 'echo "AIRFLOW_UID=50000" > .env'
                    
                    withCredentials([usernamePassword(credentialsId: 'airflow-postgres-creds', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        sh """
                            export COMPOSE_PROJECT_NAME=${env.COMPOSE_PROJECT_NAME}
                            export AIRFLOW_PORT=${env.AIRFLOW_PORT}
                            export FLOWER_PORT=${env.FLOWER_PORT}
                            export AIRFLOW_IMAGE_NAME=${env.AIRFLOW_IMAGE_NAME}
                            
                            # Use Credentials if available, else default (for POC ease)
                            export POSTGRES_USER=\${DB_USER:-airflow}
                            export POSTGRES_PASSWORD=\${DB_PASS:-airflow}
                            export POSTGRES_DB=\${POSTGRES_DB:-airflow}
                            
                            echo "Deploying Image: ${env.AIRFLOW_IMAGE_NAME}"
                            docker compose up -d
                        """
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                   echo "Cleaning up..."
                   sh 'docker system prune -f'
                }
            }
        }
    }
}
