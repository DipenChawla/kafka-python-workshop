from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
import time


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
