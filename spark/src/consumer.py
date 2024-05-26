from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'tweets',
     bootstrap_servers=['localhost:9093'],
     auto_offset_reset="latest",
     enable_auto_commit=True,
     value_deserializer = lambda x : json.loads(x))

for message in consumer:
    print(message.value)