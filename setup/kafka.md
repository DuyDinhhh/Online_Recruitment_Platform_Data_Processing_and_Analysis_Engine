# **Run Kafka sever**

## **Go to the directory of kafka**

### **Start zoo keeper**

`bin/zookeeper-server-start.sh config/zookeeper.properties`

### **Start kafka server**

`bin/kafka-server-start.sh config/server.properties`

### **Create kafka topic - kafka topic name: "topic01"**

`bin/kafka-topics.sh --create --bootstrap-server 192.168.64.1:9092 --replication-factor 1 --partitions 1 --topic topic01`

### **Start kafka consumer**

`bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic01 --from-beginning`

### **Start kafka sink-connector**

`bin/connect-standalone.sh config/connect-standalone.properties config/cassandra-sink-connector.properties`
