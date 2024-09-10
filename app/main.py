import json
import time
import os

from faker import Faker
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient

from adminTools import topic_exists, create_topic, callback
from pizzaProducer import PizzaProvider
from orderProducer import producePizzaOrder
from customerProducer import produceCustomer
from productProducer import produceProduct


# --- Define Inputs ---
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:19092')
topic_names = os.getenv('TOPICS', "customers,pizza-orders,products").split(',')
topic_names = [topic.strip() for topic in topic_names] #Strip any extra whitespace
max_batches = int(os.getenv('MAX_BATCHES', 500))
messageDelaySeconds = float(os.getenv('MESSAGE_DELAY_SECONDS', 2))


config = {
    'bootstrap.servers': bootstrap_servers,
}

# --- Define producer ---
producer = Producer(config)

# --- Check topics created ---
admin_client = AdminClient(config)

for topic in topic_names:
    print(f"Checking if topic '{topic}' exists.")
    if not topic_exists(admin_client, topic):
        create_topic(admin_client, topic)
        print(f"Topic '{topic}' created successfully.")
    else:
        print(f"Topic '{topic}' already exists.")


# --- Enrich Faker with custom provider ---
fake = Faker()
provider = PizzaProvider # from the imported module
fake.add_provider(provider) 
# fake has been enriched with PizzaProvider and can now be referenced

# --- Create the stream ---
counter = 0

while counter < max_batches:
    for topic in topic_names:
        if topic == 'customers':
            payload = produceCustomer()
        elif topic == 'pizza-orders':
            payload = producePizzaOrder(counter, fake)
        elif topic == 'products':
            payload = produceProduct()
        else:
            exit()

        key = next(iter(payload))
        encoded_key = key.encode('utf-8')
        message = json.dumps(payload[key])
        encoded_message = message.encode('utf-8')
        producer.produce(topic = topic, value = encoded_message, key = encoded_key, on_delivery=callback)
        producer.flush()
        print(f'')
        
    time.sleep(messageDelaySeconds)

    if (counter % max_batches) == 0:
        producer.flush()
    
    counter += 1

producer.flush()

print(f"Max batches ({max_batches}) reached, stopping producer.")