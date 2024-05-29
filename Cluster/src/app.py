from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, TimestampType
from pyspark.sql.functions import from_json, udf
from keras.api.saving import load_model
from preprocess import preprocess

SPARK_MASTER_IP = "local"
KAFKA_BROKER_IP = "INSIDE://kafka:9092"
KAFKA_TOPIC = "tweets"

json_schema = StructType([
    StructField('usertag', StringType(), True), \
    StructField('text', StringType(), False), \
    StructField('time_date', TimestampType(), False), \
    StructField('label', StringType(), True)]
)

spark = SparkSession \
    .builder \
    .appName("kafka handler") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
    .config("spark.sql.shuffle.partitions", 4) \
    .master(SPARK_MASTER_IP) \
    .getOrCreate()

print("reading kafka")

streaming_df = spark.readStream\
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER_IP) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

print("read kafka")

model = load_model("model.keras")
model_broadcast = spark.sparkContext.broadcast(model)

def predict_udf(text):
    model = model_broadcast.value
    text = preprocess(text)
    prediction = model.predict(text)
    return prediction  # Adjust based on your model's output format

# Register the UDF
predict = udf(predict_udf, StringType())

spark.udf.register("predict",predict)

json_df = streaming_df.selectExpr("cast(value as string) as value")

json_expanded_df = json_df.withColumn("value", from_json(json_df["value"], json_schema)).select("value.*") 

predict_df = json_expanded_df.withColumn("label", predict(json_expanded_df["text"]))

print("writing")

query = json_expanded_df.writeStream\
    .trigger(processingTime="10 seconds") \
    .format("console") \
    .outputMode("update") \
    .start()

print("finished writing")

query.awaitTermination()