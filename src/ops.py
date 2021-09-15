from src.helpers import list_topics, get_metadata_topic, create_topic, delete_topic
KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
admin_conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
}
topic = "flights-data"

print(list_topics(KAFKA_BOOTSTRAP_SERVERS=KAFKA_BOOTSTRAP_SERVERS))

print(get_metadata_topic(KAFKA_BOOTSTRAP_SERVERS, "flights-data"))

print(create_topic(KAFKA_BOOTSTRAP_SERVERS, topic))
print(delete_topic(KAFKA_BOOTSTRAP_SERVERS, topic))
