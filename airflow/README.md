# **Airflow in Docker Compose**

We configure Docker to check every 2 minutes if new data is available in the data lake. If new data is found, it will trigger an ETL script to extract, transform, and load the data into the data warehouse.

```
.
├── dags
│   └── etl-pipeline.py
├── Dockerfile
└── docker-compose.yml
```

**1. Start docker**

```
docker compose up --build
```

**2. Setup network**

```
docker network create my_network
docker network connect my_network mysqlproject
docker network connect my_network my-cassandra
docker network connect my_network airflow-etl-pipeline-container-1
```

**3. Setup network**

```
Visit [http://localhost:8080](http://localhost:8080)

```
