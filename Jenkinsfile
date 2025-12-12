pipeline {
    agent any

    // Optional: Keep parameters for "Manual" runs or testing
    parameters {
        choice(name: 'ENV_NAME', choices: ['AUTO', 'DEV', 'UAT', 'PROD'], description: 'Select ENV (AUTO = detect from Job Name)')
    }

    environment {
        AIRFLOW_IMAGE_NAME = 'my-custom-airflow:latest'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    // Logic to determine Environment
                    def targetEnv = params.ENV_NAME
                    
                    if (targetEnv == 'AUTO' || targetEnv == null) {
                        // Detect from Job Name (e.g. "TMS-DATA-MIGRATION/DEV")
                        def jobName = env.JOB_BASE_NAME.toUpperCase()
                        
                        if (jobName.contains('DEV')) {
                            targetEnv = 'DEV'
                        } else if (jobName.contains('UAT')) {
                            targetEnv = 'UAT'
                        } else if (jobName.contains('PROD')) {
                            targetEnv = 'PROD'
                        } else {
                            error "Could not auto-detect environment from Job Name: ${jobName}. Please rename job to include DEV, UAT, or PROD."
                        }
                    }

                    echo "Deploying to Environment: ${targetEnv}"
                    
                    // Define environment-specific variables
                    if (targetEnv == 'DEV') {
                        env.COMPOSE_PROJECT_NAME = 'airflow-dev'
                        env.AIRFLOW_PORT = '8082'
                        env.FLOWER_PORT = '5557'
                    } else if (targetEnv == 'UAT') {
                        env.COMPOSE_PROJECT_NAME = 'airflow-uat'
                        env.AIRFLOW_PORT = '8081'
                        env.FLOWER_PORT = '5556'
                    } else {
                        // PROD
                        env.COMPOSE_PROJECT_NAME = 'airflow-prod'
                        env.AIRFLOW_PORT = '8080'
                        env.FLOWER_PORT = '5555'
                    }
                    
                    echo "Configured for ${env.COMPOSE_PROJECT_NAME} on Port ${env.AIRFLOW_PORT}"
                }
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Airflow Image') {
            steps {
                script {
                    echo "Building Docker Image..."
                    sh 'docker build -t ${AIRFLOW_IMAGE_NAME} .'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Ensure basic .env exists
                    sh 'echo "AIRFLOW_UID=50000" > .env'

                    sh """
                        export COMPOSE_PROJECT_NAME=${env.COMPOSE_PROJECT_NAME}
                        export AIRFLOW_PORT=${env.AIRFLOW_PORT}
                        export FLOWER_PORT=${env.FLOWER_PORT}
                        export AIRFLOW_IMAGE_NAME=${env.AIRFLOW_IMAGE_NAME}
                        
                        docker compose up -d
                    """
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
