FROM apache/airflow:2.3.0-python3.8
# Install additional dependencies
RUN pip install findspark

# Initialize Airflow database and create default user (commands adapted for Dockerfile)
RUN airflow db init && airflow users create --username admin --password admin --firstname Duy --lastname Dinh --role Admin --email duynene2004@gmail.com

USER root
# Install JDK
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr

USER airflow
