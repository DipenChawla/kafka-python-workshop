from confluent_kafka import SerializingProducer
import json
from confluent_kafka.serialization import StringSerializer


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


KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
producer = get_kafka_producer(KAFKA_BOOTSTRAP_SERVERS)

with open("../data/airports.json") as f:
    data = json.load(f)
    for i in data:
        producer.poll(0)
        res = producer.produce('flights-data', value=json.dumps(data), on_delivery=delivery_report)
    producer.flush()
print("Produced records to topic")
