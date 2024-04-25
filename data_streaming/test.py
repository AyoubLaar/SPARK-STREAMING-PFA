from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Create a local StreamingContext with two working threads and batch interval of 1 second
sc = SparkContext(appName="KafkaWordCount")
ssc = StreamingContext(sc, 1)

message = KafkaUtils.createDirectStream(ssc, topics = ['testtopic'], kafkaParams={"metadata.broker.list": "localhost:9092"})

words = message.map(lambda x: x[1].flatMap(lambda x: x.split(" ")))

wordcount = words.map(lambda x: (x, 1).reduceByKey(lambda a,b: a+b))     
      
wordcount.pprint()
ssc.start()  
ssc.awaitTermination()  
