from google.cloud import firestore
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import os



class POST_ORM:
    counter = 0

    def __init__(self):
        self.connection = firestore.Client()
  
    def save(self,post):
        data = { "post":post.text, "label":post.label,"usertag":post.usertag,"time_date":post.time_date}
        self.connection.collection("posts").document().set(data)
        POST_ORM.counter = POST_ORM.counter + 1
        
    def close(self):
        self.connection.close()




class KAFKA_PRODUCER:
    counter = 0

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=os.environ.get("KAFKA_SERVER"),value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.topic = os.environ.get("KAFKA_TOPIC")

    def save(self,post):    
        future = self.producer.send(self.topic, { "post":post.text, "label":post.label,"usertag":post.usertag,"time_date":post.time_date})
        future.get(timeout = 10)
        KAFKA_PRODUCER.counter = KAFKA_PRODUCER.counter + 1
    

    def close(self):
        self.producer.close()



if __name__ == "__main__":
    class test_class:
        def __init__(self) -> None:
            self.text = "testing"
            self.label = "l"
            self.usertag = "ayoub"
            self.time_date = "time_test"
    post_orm = POST_ORM()
    post_orm.save(test_class())
    pass