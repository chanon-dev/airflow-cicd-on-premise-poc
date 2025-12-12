# Airflow CI/CD with Jenkins

This project demonstrates a local CI/CD pipeline for Apache Airflow using Jenkins and Docker.
When code is pushed to this repository (or a local git repo), Jenkins will rebuild the Airflow Docker image and restart the services.

## Prerequisites

- Docker Desktop (or Engine) installed and running.
- Git.

## Environment Architecture

We support 3 concurrent environments on your machine:

| Job Name (Contains) | Env | Port | Project Name |
| :--- | :--- | :--- | :--- |
| **.../DEV** | **DEV** | `8082` | `airflow-dev` |
| **.../UAT** | **UAT** | `8081` | `airflow-uat` |
| **.../PROD** | **PROD** | `8080` | `airflow-prod` |

## Jenkins Setup (Separate Jobs Strategy)

### 1. Start Jenkins

Run the Jenkins container which listens on port `8989`.

```bash
docker-compose -f docker-compose.jenkins.yml up -d --build
```

### 1.1 Configure Credentials (SSH) (Important!)

Since Jenkins runs in Docker, it needs your SSH key to access GitHub.

1. **Get your Private Key**:

    ```bash
    cat ~/.ssh/id_rsa
    # Copy the content from -----BEGIN... to ...END-----
    ```

2. **Add to Jenkins**:
    - Go to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)**.
    - Click **+ Add Credentials**.
    - **Kind**: `SSH Username with private key`.
    - **Username**: `git` (Must be exact!).
    - **Private Key**: Select **Enter directly** and paste your ley.
    - **ID**: `github-ssh-key`.
    - Click **Create**.
3. **Disable Host Key Checking** (For Local Dev):
    - Go to **Manage Jenkins** -> **Security**.
    - Under **Git Host Key Verification Configuration**, select **No verification**.
    - Click **Save**.

### 2. Create Jobs

You will create 3 separate Pipeline Jobs (or a Folder with 3 jobs inside) to represent each environment. Use the following naming convention:

- **DEV** (e.g., `MyProject-DEV`)
- **UAT** (e.g., `MyProject-UAT`)
- **PROD** (e.g., `MyProject-PROD`)

### 3. Configure Jobs

For each job (`DEV`, `UAT`, `PROD`):

1. **Definition**: `Pipeline script from SCM`.
2. **SCM**: `Git`.
3. **Repository URL**: Enter the path to this folder (e.g., `/Users/chanon/Desktop/airflow-cicd`).
4. **Script Path**: `Jenkinsfile`
5. Save.

### 4. Deploy

- Click **Build Now** on the specific job.
- The pipeline automatically detects the environment from the job name and deploys to the correct port.

## Notes

- The `docker-compose.yml` is configured for **CeleryExecutor** with Redis and Postgres.
- **CI/CD Logic**: The pipeline builds a custom image `my-custom-airflow:latest` containing your DAGs.
- The `volumes` for DAGs are disabled in `docker-compose.yml` to ensure the deployed container uses the immutable image built by Jenkins.
- Jenkins passes `COMPOSE_PROJECT_NAME` and ports dynamically to isolate the environments.
