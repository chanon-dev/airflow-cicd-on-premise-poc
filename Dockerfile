FROM apache/airflow:3.1.4

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy DAGs and Plugins into the image
# This allows the image to be self-contained for CI/CD
COPY --chown=airflow:root ./dags /opt/airflow/dags
COPY --chown=airflow:root ./plugins /opt/airflow/plugins
# COPY --chown=airflow:root ./requirements.txt /requirements.txt
# RUN pip install --no-cache-dir -r /requirements.txt
