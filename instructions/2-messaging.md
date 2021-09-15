This section will review the most common operations you will perform on your Kafka cluster.

For this workshop, we will be using the [confluent-kafka](https://github.com/confluentinc/confluent-kafka-python) library for Python. The library is a wrapper around librdkafka and is highly performant and battle-tested in production.
Other options like [kafka-python](https://github.com/dpkp/kafka-python) and [aiokafka](https://github.com/aio-libs/aiokafka) exist as well.

confluent-kafka essentially provides 3 interfaces: a high-level Producer, Consumer and AdminClient

# Creating, or deleting a topic 

You have the option of either adding topics manually or having them be created automatically when data is first published to a non-existent topic. If topics are auto-created then you may want to tune the default [topic configurations](http://kafka.apache.org/documentation.html#topicconfigs) used for auto-created topics.

To perform operations on a given topic, we use confluent_kafka's [AdminClient](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#module-confluent_kafka.admin) module

## Important configurations - Topic Level

1. Replication Factor : The replication factor controls how many servers will replicate each message that is written. The replication factor of your topic determines the availability of your data.
If your replication factor (RF) is 3, you can afford to lose 2 brokers and still be able to perform operations on it

2. Partition Count: The partition count controls how many shards the data can be split into. If you have 3 partitions of your topic, the data will be evenly distributed to the 3 partitions and can be served by upto 3 servers (not counting replicas).
Also, the number of partitions reflects the maximum number of consumers you can have reading concurrently from the topic

The full set of configurations can be found [here](http://kafka.apache.org/documentation.html#topicconfigs)


* Manually adding a topic -

    ```python
    # create-topic.py
    from helpers import list_topics, create_topic
    topic = "airports-data"
    KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"

    print(f"List of topics before creation : {list_topics(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS)}\n")
    print(create_topic(KAFKA_BOOTSTRAP_SERVERS, topic))
    print(f"List of topics after creation : {list_topics(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS)}\n")
    ```

* Deleting a topic

    ```python
    # delete_topic.py
    from helpers import list_topics, delete_topic
    topic = "airports-data"
    KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"

    print(f"List of topics before deletion : {list_topics(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS)} \n")
    print(delete_topic(KAFKA_BOOTSTRAP_SERVERS, topic))
    print(f"List of topics after deletion : {list_topics(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS)} \n")
    ```

* Get metadata of a topic

    ```python
    # get_metadata_topic.py
    from helpers import get_metadata_topic
    topic = "airports-data"
    KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
    print(get_metadata_topic(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS, topic=topic))
    ```

The response from the create and delete operations returns a Future class, which can be awaited to get the result of the operation

# Publishing data to a topic

The publisher or producer implementation can be used to send a stream of data to a topic, synchronously or asynchronously.
It is possible to attach a key to each message, in which case the producer guarantees that all messages with the same key will arrive to the same partition. If you do not have a key, Kafka uses it's own hashing algorithm to generate one for you


## Important configurations - Producer Level

1. Bootstrap Servers: This is the list of broker URLs to connect to the Kafka cluster. Depending upon the type of security protocols set by Kafka cluster, you may need to provide additional fields for authenticating and transacting with the brokers

2. Serializers: The `key.serializer` and `value.serializer` classes instruct the SerializingProducer on how to convert the message payload to bytes.
The `confluent_kafka` library providers built-in serializers like StringSerializer, JSONSerializer and AvroSerializer

The full set of configurations can be found [here](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md#configuration-properties)

* Publishing the airports data to a topic

    ```python
    #producer.py
    import json
    from helpers import delivery_report, get_kafka_producer

    KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
    producer = get_kafka_producer(KAFKA_BOOTSTRAP_SERVERS)

    with open("../data/airports.json") as f:
        data = json.load(f)
        for i in data:
            producer.poll(0)
            res = producer.produce('airports-data', value=json.dumps(i), on_delivery=delivery_report)
        producer.flush()
    print("Produced records to topic")
    ```

    The above method implements a callback (alias `on_delivery`) argument to pass a function that will be called from `poll()` when the message has been successfully delivered or permanently fails delivery.
    The `flush()` method can be called to poll and register all remaining callbacks (until the length is 0)


# Subscribing to data from a topic

The subscriber or consumer implementation can be used to read streams of data from topics in the Kafka cluster.

## Important configurations - Consumer Level

1. Bootstrap Servers: Same as producer

2. Serializers: Same as producer

3. Consumer Group: 

    A consumer group is a group of Kafka consumers (:mindblown:) that share the same group ID.
    As the official documentation for Consumer Group in Kafka says 
    > “If all the consumer instances have the same consumer group, then the records will effectively be load-balanced over the consumer instances.”
    >
    What that effectively means is that all the consumer groups will read messages from different partitions but will effectively work together so as to maintain the offset order for that group.

    It is possible (and, recommended) to have separate consumer groups if you would like to read the same data for multiple usecases

4. Commit Offset Semantics:

    The offset is a simple integer number that is used by Kafka to maintain the current position of a consumer 
    Whenever a consumer reads a new message(s), the consumer acknowledges by incrementing the offset count to indicate the data has been consumed.

    That acknowledgement can be done after a fixed number of ms (`auto.commit.interval.ms`) or once the message is received or once the processing on this message is completed.

    This leads to different behaviour of consumers in case of a record being mis-processed.
    If auto-commits are turned on, the message offset might be committed before the mis-processing occurs leading to `best-effort` or `at-most-once` delivery semantics.

    However, if the committs are made after the processing is done (successfully), it leads to `atleast-once` delivery guarantee.

    Read [this article](https://www.thebookofjoel.com/python-kafka-consumers) to know more about delivery semantics and to learn about another type of semantics called as `exactly-once` semantics

    The full set of configurations can be found [here](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md#configuration-properties)

* Publishing the airports data to a topic

    ```python
    # consumer.py
    import json
    from helpers import get_kafka_consumer

    KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"

    consumer = get_kafka_consumer(KAFKA_BOOTSTRAP_SERVERS, "east-coast-dpt")
    TOPIC_NAME = ["airports-data"]
    consumer.subscribe(TOPIC_NAME)

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        s = json.loads(msg.value())
        print(s)
        consumer.commit(asynchronous=False)
    consumer.close()
    ```

    The `poll()` method consumes a single message, calls callbacks and returns events.
    You can check the returned event for a KafkaMessage object or a KafkaError
    The consumer implementation provides a handy number of functions like `seek()`, `pause()`, `resume()`, `position()` to read message streams as required by the application
