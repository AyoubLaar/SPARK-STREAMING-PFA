from kafka import KafkaProducer
import json
import pandas as pd
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9093',value_serializer=lambda m: json.dumps(m).encode('ascii'))
data = pd.read_csv("data/unlabeled_tweets.csv")
for row in data.values:
#post,usertag,time_date,label
    future = producer.send('tweets', {
        "text":row[0],
        "usertag":row[1],
        "time_date":row[2],
        "label":row[3]
    })
    future.get(timeout = 10)
    sleep(1)
