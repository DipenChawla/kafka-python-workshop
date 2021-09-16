from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
import time
from confluent_kafka import SerializingProducer, DeserializingConsumer
from confluent_kafka.serialization import StringSerializer, StringDeserializer


def list_topics(KAFKA_BOOTSTRAP_SERVERS):
    consumer_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "anygroup",
        "auto.offset.reset": "earliest",
        "security.protocol": "plaintext",
        "enable.auto.commit": False,
    }

    consumer = Consumer(consumer_conf)
    return list(consumer.list_topics().topics)


def get_metadata_topic(KAFKA_BOOTSTRAP_SERVERS, topic):
    consumer_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "anygroup",
        "auto.offset.reset": "earliest",
        "security.protocol": "plaintext",
        "enable.auto.commit": False,
    }

    consumer = Consumer(consumer_conf)
    meta = consumer.list_topics().topics[topic]
    return f"topic: {meta.topic}, partitions: {len(meta.partitions)}"


def create_topic(KAFKA_BOOTSTRAP_SERVERS, topic):
    admin_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    }
    admin_client = AdminClient(admin_conf)
    topic_list = []
    topic_list.append(NewTopic(topic=topic, num_partitions=5, replication_factor=1))
    resp = admin_client.create_topics(new_topics=topic_list, validate_only=False)
    time.sleep(5)
    if resp.get(topic).result() is None:
        return "topic created!"
    else:
        return resp.get(topic).result()


def delete_topic(KAFKA_BOOTSTRAP_SERVERS, topic):
    admin_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    }
    admin_client = AdminClient(admin_conf)
    resp = admin_client.delete_topics(topics=[topic])
    time.sleep(5)
    if resp.get(topic).result() is None:
        return "topic deleted!"
    else:
        return resp.get(topic).result()


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def get_kafka_producer(KAFKA_BOOTSTRAP_SERVERS):
    producer_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "value.serializer": StringSerializer(),
    }
    producer = SerializingProducer(producer_conf)
    return producer


def get_kafka_consumer(KAFKA_BOOTSTRAP_SERVERS, consumer_group):
    consumer_conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": consumer_group,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "value.deserializer": StringDeserializer(),
    }
    consumer = DeserializingConsumer(consumer_conf)
    return consumer