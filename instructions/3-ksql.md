### Run two terminal windows, side by side, both running ksqlDB CLI


```
docker exec -it kafka-python-workshop_ksql-server_1  ksql http://localhost:8088
```


### ksqlDB basics

1. Create a stream

```
----
CREATE STREAM MOVEMENTS (PERSON VARCHAR KEY, LOCATION VARCHAR) 
    WITH (VALUE_FORMAT='JSON', PARTITIONS=1, KAFKA_TOPIC='movements');
----
```

2. Query the stream

```
----
SELECT TIMESTAMPTOSTRING(ROWTIME,'yyyy-MM-dd HH:mm:ss','Europe/London') AS EVENT_TS, 
       PERSON,
       LOCATION 
  FROM MOVEMENTS
  EMIT CHANGES;
```


3. Insert some data

```
----
INSERT INTO MOVEMENTS VALUES ('robin', 'York');
INSERT INTO MOVEMENTS VALUES ('robin', 'Leeds');
INSERT INTO MOVEMENTS VALUES ('robin', 'Ilkley');
----
```



### topic management from  ksql 


1. Show that a new topic has been created

```
----
SHOW TOPICS;
----
```

2. Dump the topic contents

```
----
PRINT 'leeds-users' FROM BEGINNING;
----
```



https://github.com/tmcgrath/kafka-connect-examples/blob/master/mysql/mysql-bulk-sink.json