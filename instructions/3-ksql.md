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


1. Show topic which is present in the kafka cluster.

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



## Pull vs Push query 

```A push query is a form of query issued by a client that subscribes to a result as it changes in real-time. A good example of a push query is subscribing to a particular user's geographic location.```

```
SELECT TIMESTAMPTOSTRING(ROWTIME,'yyyy-MM-dd HH:mm:ss','Europe/London') AS EVENT_TS, 
       PERSON,
       LOCATION 
  FROM MOVEMENTS
  EMIT CHANGES;
```

```A pull query is a form of query issued by a client that retrieves a result as of "now", like a query against a traditional RDBS.```

```
SELECT TIMESTAMPTOSTRING(ROWTIME,'yyyy-MM-dd HH:mm:ss','Europe/London') AS EVENT_TS, 
       PERSON,
       LOCATION 
  FROM MOVEMENTS WHERE PERSON='robin'
  
```


## filtering the data on runtime 
```SELECT * 
FROM MOVEMENTS
WHERE LOCATION='York' 
```


# Create Stream from stream .


```
CREATE STREAM filtered_stream  AS
   SELECT  *
    FROM MOVEMENTS
    WHERE LOCATION='York' 
    EMIT CHANGES;
```





### What are Streams and Tables?

  > Both Streams and Tables are wrappers on top of Kafka topics, which has continuous never-ending data. But, conceptually these abstractions are different because-

1. Streams represent data in motion capturing events happening in the world, and has the following features-

> Unbounded
 - Storing a never-ending continuous flow of data and thus Streams are unbounded as they have no limit.
> Immutable
  - Any new data that comes in gets appended to the current stream and does not modify any of the existing records, making it completely immutable.


1.  While A table represents the data at rest or a materialized view of that stream of events with the latest value of a key and has the following features-

> Bounded
- Represents a snapshot of the stream at a time, and therefore it has its limits defined.
> Mutable
- Any new data(<Key, Value> pair) that comes in gets added to the current table if the table does not have an existing entry with the same key otherwise, the existing record is mutated to have the latest value for that key.



## Create table on topics 

```
CREATE TABLE MOVEMENTS_TABLE (
     PERSON PRIMARY KEY,
     LOCATION BIGINT,
   ) WITH (
     KAFKA_TOPIC = 'MOVEMENTS', 
     VALUE_FORMAT = 'JSON'
   );
```


## Create and aggregated stream table 

```
CREATE TABLE AGG_MOVEMENT AS
   SELECT
      MOVEMENTS.LOCATION
      count(*) AS loc_count
   FROM MOVEMENTS 
   WINDOW TUMBLING (7 DAYS)
   GROUP BY MOVEMENTS.LOCATION
   EMIT CHANGES;

```



https://github.com/tmcgrath/kafka-connect-examples/blob/master/mysql/mysql-bulk-sink.json