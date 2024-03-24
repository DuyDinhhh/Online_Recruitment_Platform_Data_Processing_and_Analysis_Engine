import os
#os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/jdk-20.jdk/Contents/Home"
#os.environ["SPARK_HOME"] = "/Users/nguyentadinhduy/spark-3.5.0-bin-hadoop3"
#os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
os.environ["SPARK_HOME"] = "/opt/spark"
os.environ['PYSPARK_SUBMIT_ARGS']="--master local[2] pyspark-shell"
import findspark
findspark.init()
from pyspark.sql import SparkSession
host = 'mysqlproject'
#port = '3307'
port = '3306'
db_name = 'data_engineering'
user = 'root'
password = 'root'
#url = 'jdbc:mysql://' + host + ':' + port + '/' + db_name
url = f'jdbc:mysql://{host}:{port}/{db_name}?user={user}&password={password}'
driver = "com.mysql.cj.jdbc.Driver"
def get_latest_time_cassandra():
    data = spark.read.format("org.apache.spark.sql.cassandra").option("spark.cassandra.connection.host", "my-cassandra").option("spark.cassandra.connection.port", "9042").option("spark.cassandra.auth.username", "cassandra").option("spark.cassandra.auth.password", "cassandra").options(table="tracking", keyspace="study_de").load()
    cassandra_latest_time = data.agg({'ts':'max'}).take(1)[0][0]
    return cassandra_latest_time

def get_latest_time_mysql(url,driver,user,password):    
    sql = """(select max(latest_update_time) from events) data"""
    mysql_time = spark.read.format('jdbc').options(url=url, driver=driver, dbtable=sql, user=user, password=password).load()
    mysql_time = mysql_time.take(1)[0][0]
    if mysql_time is None:
        mysql_latest = '1998-01-01 23:59:59'
    else :
        mysql_latest = mysql_time.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_latest

#def main():
#    cassandra_time = get_latest_time_cassandra()
##    print('Cassandra latest time is {}'.format(cassandra_time))
#    mysql_time = get_latest_time_mysql(url,driver,user,password)
##    print('MySQL latest time is {}'.format(mysql_time))
#    if cassandra_time > mysql_time:
#        spark.stop()
#        return True
#    else:
#        spark.stop()
#        return False
def main():
    cassandra_time = get_latest_time_cassandra()
    mysql_time = get_latest_time_mysql(url,driver,user,password)
    result = cassandra_time > mysql_time
    print("true" if result else "false")


# if __name__ == "__main__":
#     spark = SparkSession.builder \
#     .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,mysql:mysql-connector-java:8.0.30") \
#     .getOrCreate()
#     main()
if __name__ == "__main__":
    spark = SparkSession.builder \
    .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.30") \
    .getOrCreate()
    main()
