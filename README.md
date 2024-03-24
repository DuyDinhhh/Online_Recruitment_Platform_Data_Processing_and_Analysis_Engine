# **Objective**

This project is about creating a system to handle and make sense of the activity records from a job recruitment platform. The main aim is to keep, work on, and study these records to help the company decide what to do next. It uses Kafka to organize incoming data and sends this untouched data to Cassandra, which is like a big storage space. Then, PySpark takes this data, changes it, and puts it into MySQL, where it is kept for future use. We use Grafana to make charts and graphs of the data. The whole project is set up with Docker, which makes it easier to start and run the system.

- Tech stack: PySpark, Kafka, Airflow, Docker, Cassandra, MySQL, Grafana, Python.

# **Architecture**

![Architecture](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/assets/Architecture.png?raw=true)

## **Raw data**

- The website's log data is captured in real-time and initially stored in Cassandra. From there, PySpark is used to transform the data, after which it is sent to Kafka. Finally, the processed data is pushed from Kafka into a MySQL database through a Kafka connector.
- Log data schema

```sh
.
root
 |-- create_time: string (nullable = false)
 |-- bid: integer (nullable = true)
 |-- bn: string (nullable = true)
 |-- campaign_id: integer (nullable = true)
 |-- cd: integer (nullable = true)
 |-- custom_track: string (nullable = true)
 |-- de: string (nullable = true)
 |-- dl: string (nullable = true)
 |-- dt: string (nullable = true)
 |-- ed: string (nullable = true)
 |-- ev: integer (nullable = true)
 |-- group_id: integer (nullable = true)
 |-- id: string (nullable = true)
 |-- job_id: integer (nullable = true)
 |-- md: string (nullable = true)
 |-- publisher_id: integer (nullable = true)
 |-- rl: string (nullable = true)
 |-- sr: string (nullable = true)
 |-- ts: string (nullable = true)
 |-- tz: integer (nullable = true)
 |-- ua: string (nullable = true)
 |-- uid: string (nullable = true)
 |-- utm_campaign: string (nullable = true)
 |-- utm_content: string (nullable = true)
 |-- utm_medium: string (nullable = true)
 |-- utm_source: string (nullable = true)
 |-- utm_term: string (nullable = true)
 |-- v: integer (nullable = true)
 |-- vp: string (nullable = true)
```

![log_data](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/assets/logdata.png?raw=true)

# **Processing Data**

Read and review the data recording user actions in the log data, notice that there are actions with analytical value in the column `["custom_track"]` including: `clicks, conversion, qualified, unqualified`. Processing raw data to obtain valuable clean data:

- Filter actions with analytical value in column `["custom_track"] `including: `clicks, conversion, qualified, unqualified`.
- Remove null values, replace with 0 to be able to calculate.
- Calculate the basic values of data for in-depth analysis.
- Use pySpark to write Spark jobs and process data efficiently.
  Data after processing is saved to Data Warehouse is MySQL for storage and in-depth analysis.

## **Clean data**

- Clean data schema

```sh
root
 |-- job_id: string (nullable = true)
 |-- dates: date (nullable = true)
 |-- hours: integer (nullable = true)
 |-- publisher_id: long (nullable = true)
 |-- company_id: integer (nullable = true)
 |-- campaign_id: double (nullable = false)
 |-- group_id: double (nullable = false)
 |-- disqualified_application: long (nullable = true)
 |-- qualified_application: long (nullable = true)
 |-- conversion: long (nullable = true)
 |-- clicks: long (nullable = true)
 |-- bid_set: double (nullable = false)
 |-- spend_hour: double (nullable = false)
 |-- sources: string (nullable = false)
```

![clean_data](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/assets/cleandata.png?raw=true)

# **Visualizing Data with Grafana**

![visualization](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/assets/visualization.png?raw=true)

# **Set up**

## **Pre-requisite**

**Kafka setup**

- Read instructions in file kafka\Run kafka sever.txt.

**Spark setup**

- Install Spark (used 3.5.0).

**Airflow setup**

- Install Airflow in Docker Compose.

**Cassandra setup**

- Install Cassandra.

**MySQL setup**

- Install Mysql.

# **Get Going!**

- Setup Kafka service and start sending log data from website [set up](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/setup/kafka.md)
- Setup Airflow to trigger the data pipeline [set up](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/airflow/README.md)
- Setup Grafana for data visualization Setup [set up](https://github.com/DuyDinhhh/Online_Recruitment_Platform_Data_Processing_and_Analysis_Engine/blob/main/setup/grafana.md)

