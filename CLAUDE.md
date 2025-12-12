# Airflow CI/CD Project with Jenkins

## Overview

This project sets up an automated deployment pipeline for Apache Airflow using a local Jenkins container.

- **Goal**: Auto-deploy Airflow on local machine when code is pushed to GitHub.
- **Stack**: Airflow (Docker), Jenkins (Docker), GitHub.

## Commands

- **Start Airflow**: `AIRFLOW_IMAGE_NAME=my-custom-airflow:latest docker-compose up -d`
- **Stop Airflow**: `docker-compose down`
- **Start Jenkins**: `docker-compose -f docker-compose.jenkins.yml up -d`
- **Stop Jenkins**: `docker-compose -f docker-compose.jenkins.yml down`
- **View Airflow Logs**: `docker-compose logs -f`
- **View Jenkins Logs**: `docker-compose -f docker-compose.jenkins.yml logs -f`

## Architecture

1. **GitHub**: Source code repository.
2. **Jenkins**: Runs in a container. Mounts `/var/run/docker.sock` to control host Docker.
3. **Deployment**: Jenkins Pipeline (`Jenkinsfile`) runs `docker-compose up -d --build` to update Airflow containers.

## Setup Instructions

1. **Jenkins**:
   - Run `docker-compose -f docker-compose.jenkins.yml up -d`
   - Access at `http://localhost:8080`
   - Install "Docker" and "Docker Pipeline" plugins.
   - Create a new "Pipeline" job.
   - Point to this GitHub repository.
2. **GitHub Webhook**:
   - Point webhook to your Jenkins URL (use ngrok if local: `ngrok http 8080`).

## File Structure

- `docker-compose.yml`: Airflow services (Webserver, Scheduler, etc.)
- `docker-compose.jenkins.yml`: Jenkins service.
- `Jenkinsfile`: Pipeline definition.
- `dags/`: Airflow DAGs.
