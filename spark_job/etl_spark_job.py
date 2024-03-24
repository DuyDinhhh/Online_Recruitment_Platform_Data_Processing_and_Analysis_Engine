import os
os.environ["JAVA_HOME"] = "/opt/java"
#os.environ["SPARK_HOME"] = "/Users/nguyentadinhduy/spark-3.5.0-bin-hadoop3"
#os.environ["JAVA_HOME"] = "/opt/java/cc"
os.environ["SPARK_HOME"] = "/opt/spark"
os.environ['PYSPARK_SUBMIT_ARGS']="--master local[2] pyspark-shell"

import findspark
#findspark.add_packages('mysql:mysql-connector-java:8.0.30')
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
import pyspark.sql.functions as sf
from uuid import *
from pyspark.sql.functions import when
#from "./login_mysql" import host,port,db_name,user,password,url,driver 
#host = 'localhost'
host = 'mysqlproject'
port = '3306'
db_name = 'data_engineering'
user = 'root'
password = 'root'
#url = 'jdbc:mysql://' + host + ':' + port + '/' + db_name
url = f'jdbc:mysql://{host}:{port}/{db_name}?user={user}&password={password}'
#driver = "com.mysql.jdbc.Driver"
driver = "com.mysql.cj.jdbc.Driver"

def process_click_data(data):
    clicks_data = data.filter(data.custom_track == 'click')
    clicks_data = clicks_data.na.fill({'bid':0})
    clicks_data = clicks_data.na.fill({'job_id':0})
    clicks_data = clicks_data.na.fill({'publisher_id':0})
    clicks_data = clicks_data.na.fill({'group_id':0})
    clicks_data = clicks_data.na.fill({'campaign_id':0})
    clicks_data.registerTempTable('clicks')
    clicks_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , avg(bid) as bid_set, count(*) as clicks , sum(bid) as spend_hour from clicks
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return clicks_output 

def process_conversion_data(data):
    conversion_data = data.filter(data.custom_track == 'conversion')
    conversion_data = conversion_data.na.fill({'job_id':0})
    conversion_data = conversion_data.na.fill({'publisher_id':0})
    conversion_data = conversion_data.na.fill({'group_id':0})
    conversion_data = conversion_data.na.fill({'campaign_id':0})
    conversion_data.registerTempTable('conversion')
    conversion_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as conversions  from conversion
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return conversion_output 
    
def process_qualified_data(data):
    qualified_data = data.filter(data.custom_track == 'qualified')
    qualified_data = qualified_data.na.fill({'job_id':0})
    qualified_data = qualified_data.na.fill({'publisher_id':0})
    qualified_data = qualified_data.na.fill({'group_id':0})
    qualified_data = qualified_data.na.fill({'campaign_id':0})
    qualified_data.registerTempTable('qualified')
    qualified_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as qualified  from qualified
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return qualified_output

def process_unqualified_data(data):
    unqualified_data = data.filter(data.custom_track == 'unqualified')
    unqualified_data = unqualified_data.na.fill({'job_id':0})
    unqualified_data = unqualified_data.na.fill({'publisher_id':0})
    unqualified_data = unqualified_data.na.fill({'group_id':0})
    unqualified_data = unqualified_data.na.fill({'campaign_id':0})
    unqualified_data.registerTempTable('unqualified')
    unqualified_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as unqualified  from unqualified
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return unqualified_output


def process_final_data(clicks_output,conversion_output,qualified_output,unqualified_output):
    final_data = clicks_output.join(conversion_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full').\
    join(qualified_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full').\
    join(unqualified_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full')
    return final_data 

def process_cassandra_data(data):
    clicks_output = process_click_data(data)
    conversion_output = process_conversion_data(data)
    qualified_output = process_qualified_data(data)
    unqualified_output = process_unqualified_data(data)
    final_data = process_final_data(clicks_output,conversion_output,qualified_output,unqualified_output)
    return final_data


def import_to_mysql(output):
    final_output = output.select('job_id','date','hour','publisher_id','company_id','campaign_id','group_id','unqualified','qualified','conversions','clicks','bid_set','spend_hour')
    final_output = final_output.withColumnRenamed('date','dates').withColumnRenamed('hour','hours').withColumnRenamed('qualified','qualified_application').\
    withColumnRenamed('unqualified','disqualified_application').withColumnRenamed('conversions','conversion')
    final_output = final_output.withColumn('sources',lit('Cassandra'))
    final_output.write.format("jdbc") \
    .option("driver","com.mysql.cj.jdbc.Driver") \
    .option("url", f'jdbc:mysql://{host}:{port}/{db_name}?user={user}&password={password}') \
    .option("dbtable", "events") \
    .mode("append") \
    .option("user", "root") \
    .option("password", "root") \
    .save()
    return print('Data imported successfully')
def main_task(mysql_time):
#    host = 'localhost'
#    port = '3307'
#    db_name = 'data_engineering'
#    user = 'root'
#    password = 'root'
#    url = 'jdbc:mysql://' + host + ':' + port + '/' + db_name
#    driver = "com.mysql.cj.jdbc.Driver"
    host = 'mysqlproject'
    port = '3306'
    db_name = 'data_engineering'
    user = 'root'
    password = 'root'
    #url = 'jdbc:mysql://' + host + ':' + port + '/' + db_name
    url = f'jdbc:mysql://{host}:{port}/{db_name}?user={user}&password={password}'
    #driver = "com.mysql.jdbc.Driver"
    driver = "com.mysql.cj.jdbc.Driver"
    print('The host is ' ,host)
    print('The port using is ',port)
    print('The db using is ',db_name)
    print('-----------------------------')
    print('Retrieving data from Cassandra')
    print('-----------------------------')
    data = spark.read.format("org.apache.spark.sql.cassandra").option("spark.cassandra.connection.host", "my-cassandra").option("spark.cassandra.connection.port", "9042").option("spark.cassandra.auth.username", "cassandra").option("spark.cassandra.auth.password", "cassandra").options(table="tracking", keyspace="study_de").load() \
    .where(col('ts') >= mysql_time)
#    data = spark.read.format("org.apache.spark.sql.cassandra").options(table="tracking",keyspace="study_de").load().where(col('ts')>= mysql_time)
    print('-----------------------------')
    print('Selecting data from Cassandra')
    print('-----------------------------')
    data = data.select('ts','job_id','custom_track','bid','campaign_id','group_id','publisher_id')
    data = data.filter(data.job_id.isNotNull())
#   process_df = process_df(df)
    print('-----------------------------')
    print('Processing Cassandra Output')
    print('-----------------------------')
    cassandra_output = process_cassandra_data(data)
    print('-----------------------------')
    print('Merge Company Data')
    print('-----------------------------')
    company = retrieve_company_data(url,driver,user,password)
    print('-----------------------------')
    print('Finalizing Output')
    print('-----------------------------')
    final_output = cassandra_output.join(company,'job_id','left').drop(company.group_id).drop(company.campaign_id)
    print('-----------------------------')
    print('Import Output to MySQL')
    print('-----------------------------')
#    final_output.show()
    import_to_mysql(final_output)
    return print('Task Finished')

def retrieve_company_data(url,driver,user,password):
    sql = """(SELECT id as job_id, company_id, group_id, campaign_id FROM job) test"""
    company = spark.read.format('jdbc').options(url=url, driver=driver, dbtable=sql, user=user, password=password).load()
    return company 

def get_mysql_latest_time():    
    sql = """(select max(latest_update_time) from events) data"""
    mysql_time = spark.read.format('jdbc').options(url=url, driver=driver, dbtable=sql, user=user, password=password).load()
    mysql_time = mysql_time.take(1)[0][0]
    if mysql_time is None:
        mysql_latest = '1998-01-01 23:59:59'
    else :
        mysql_latest = mysql_time.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_latest

if __name__ == "__main__":
    spark = SparkSession.builder \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,mysql:mysql-connector-java:8.0.30") \
    .getOrCreate()
    mysql_time = get_mysql_latest_time()
    main_task(mysql_time)

