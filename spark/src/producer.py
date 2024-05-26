from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9093',value_serializer=lambda m: json.dumps(m).encode('ascii'))
future = producer.send('tweets', {
    "usertag":"test",
    "text":"test",
    "time_date":"2023-12-30 11:27:35",
    "label":"test"
})
future.get(timeout = 10)