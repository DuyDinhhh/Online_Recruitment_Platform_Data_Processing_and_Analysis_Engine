from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType
from pyspark.sql.functions import col,struct,to_json
from datetime import datetime
from cassandra.util import uuid_from_time
import random
import time
scala_version = '2.12.17'
spark_version = '3.5.0'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.3.1'
]

spark=SparkSession.builder.config("spark.jars.packages",'com.datastax.spark:spark-cassandra-connector_2.12:3.1.0').master("local").appName("kafka-example").config("spark.jars.packages", ",".join(packages)).getOrCreate()
 

mysql_host = 'localhost'
mysql_port = '3307'
mysql_db_name = 'data_engineering'
mysql_user = 'root'
mysql_password = 'root'

def get_data_from_job():
    # Read job data from MySQL
    jobs_data = spark.read.format("jdbc").option("url", f"jdbc:mysql://{mysql_host}:{mysql_port}/{mysql_db_name}") \
        .option("dbtable", "(select id as job_id, campaign_id, group_id, company_id from job) as tmp") \
        .option("user", mysql_user).option("password", mysql_password).option("driver", "com.mysql.cj.jdbc.Driver").load()
    return jobs_data

def get_data_from_publisher():
    # Read publisher data from MySQL
    publisher_data = spark.read.format("jdbc").option("url", f"jdbc:mysql://{mysql_host}:{mysql_port}/{mysql_db_name}") \
        .option("dbtable", "(select distinct(id) as publisher_id from master_publisher) as tmp") \
        .option("user", mysql_user).option("password", mysql_password).option("driver", "com.mysql.cj.jdbc.Driver").load()
    return publisher_data

def generating_dummy_data(n_records):
    publisher = get_data_from_publisher()
    jobs_data = get_data_from_job()
    publisher_list = [row['publisher_id'] for row in publisher.collect()]
    job_list = [row['job_id'] for row in jobs_data.collect()]
    campaign_list = [row['campaign_id'] for row in jobs_data.collect()]
    group_list = [row['group_id'] for row in jobs_data.filter(jobs_data['group_id'].isNotNull()).select('group_id').collect()]
    for i in range(n_records):
        create_time = datetime.now()
        bid = random.randint(0, 1)
        interact = ['click', 'conversion', 'qualified', 'unqualified']
        custom_track = random.choices(interact, weights=(70, 10, 10, 10))[0]
        job_id = random.choice(job_list)
        publisher_id = random.choice(publisher_list)
        group_id = random.choice(group_list)
        campaign_id = random.choice(campaign_list)
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        uuid_time = str(uuid_from_time(create_time))
        data=spark.createDataFrame([(uuid_time, bid, campaign_id, custom_track, group_id, job_id, publisher_id, ts)],["create_time", "bid", "campaign_id", "custom_track", "group_id", "job_id", "publisher_id", "ts"]) \
            .withColumn("create_time", col("create_time").cast(StringType()))
        json_df = data.select(
            col("publisher_id").cast(StringType()).alias("key"),
            to_json(struct([col(name) for name in data.columns])).alias("value")
        )
        json_df.write\
               .format("kafka")\
               .option("kafka.bootstrap.servers", "192.168.64.1:9092")\
               .option("topic", "test15")\
               .save()
    print("Data Generated Successfully")


status = "ON"
while status == "ON":
    generating_dummy_data(n_records=random.randint(1, 20))
    time.sleep(30)
 


