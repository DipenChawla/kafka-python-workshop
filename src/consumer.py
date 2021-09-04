from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer
import json

KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"

consumer_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "east-coast-dept",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
    "value.deserializer": StringDeserializer(),
}

consumer = DeserializingConsumer(consumer_conf)

TOPIC_NAME = ["flights-data"]
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
