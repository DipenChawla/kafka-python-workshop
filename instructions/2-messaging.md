This section will review the most common operations you will perform on your Kafka cluster.

# Creating, or deleting a topic 

You have the option of either adding topics manually or having them be created automatically when data is first published to a non-existent topic. If topics are auto-created then you may want to tune the default [topic configurations](http://kafka.apache.org/documentation.html#topicconfigs) used for auto-created topics.

To perform operations on a given topic, we use confluent_kafka's [AdminClient](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#module-confluent_kafka.admin) module

Manually adding a topic -

```python
admin_client = AdminClient(...)
topic_list = []
topic_list.append(NewTopic(topic=topic)
resp = admin_client.create_topics(new_topics=topic_list)
```

Deleting a topic

```python
resp = admin_client.delete_topics(topics=[topic])
```

The response from the above operations returns a Future class, which can be awaited to get the result of the operation

## Important configurations - Topic Level

1. Replication Factor : The replication factor controls how many servers will replicate each message that is written. The replication factor of your topic determines the availability of your data.
If your replication factor (RF) is 3, you can afford to lose 2 brokers and still be able to perform operations on it

2. Partition Count: The partition count controls how many shards the data can be split into. If you have 3 partitions of your topic, the data will be evenly distributed to the 3 partitions and can be served by upto 3 servers (not counting replicas).
Also, the number of partitions reflects the maximum number of consumers you can have reading concurrently from the topic

The full set of configurations can be found [here](http://kafka.apache.org/documentation.html#topicconfigs)


# Publishing data to a topic

The publisher or producer implementation can be used to send a stream of data to a topic, synchronously or asynchronously.
It is possible to attach a key to each message, in which case the producer guarantees that all messages with the same key will arrive to the same partition. If you do not have a key, Kafka uses it's own hashing algorithm to generate one for you

```python
res = producer.produce(topic, value=json.dumps(data))
```

### TODO: write here about async, poll() and flush()


## Important configurations - Producer Level

1. Bootstrap Servers: This is the list of broker URLs to connect to the Kafka cluster. Depending upon the type of security protocols set by Kafka cluster, you may need to provide additional fields for authenticating and transacting with the brokers

2. Serializers: The `key.serializer` and `value.serializer` classes instruct the SerializingProducer on how to convert the message payload to bytes.
The `confluent_kafka` library providers built-in serializers like StringSerializer, JSONSerializer and AvroSerializer

The full set of configurations can be found [here](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md#configuration-properties)


# Subscribing to data from a topic

The subscriber or consumer implementation can be used to read streams of data from topics in the Kafka cluster.

