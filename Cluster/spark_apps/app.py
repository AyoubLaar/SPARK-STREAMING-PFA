from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType, TimestampType, IntegerType
from pyspark.sql.functions import from_json, udf, current_timestamp
from keras.models import load_model
from preprocess import preprocess
import pandas as pd

SPARK_MASTER_IP = "local"
KAFKA_BROKER_IP = "INSIDE://kafka:9092"
KAFKA_TOPIC = "tweets"
ES_INDEX="tweets_2"

def configure_spark():
    spark = SparkSession \
        .builder \
        .appName("Real time tweets processing") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
        .config("spark.sql.shuffle.partitions", 4) \
        .config("spark.es.nodes", "elasticsearch") \
        .config("spark.es.port", "9200") \
        .config("spark.es.index.auto.create", "true") \
        .master(SPARK_MASTER_IP) \
        .getOrCreate()
    return spark

def read_kafka(spark):
    streaming_df = spark.readStream\
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER_IP) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()
    return streaming_df

def broadcast_model(spark):
    model = load_model("model.keras")
    global model_broadcast
    model_broadcast = spark.sparkContext.broadcast(model)
    return model_broadcast

#excel short anim nakba leila warah tell famili stori forc villag palestin exist resist date last year may re post nakba76 anniversari free palestin ceasefir gaza now
def predict_udf(text):
    model = model_broadcast.value
    preprocessed_text = preprocess(text)
    input_data = pd.Series(preprocessed_text)
    prediction = model.predict(input_data)
    result = int(prediction[0][0] >= 0.5)
    return result

def transform_data(df):
    json_schema = StructType([
        StructField('usertag', StringType(), True), \
        StructField('text', StringType(), False), \
        StructField('time_date', TimestampType(), False), \
        StructField('label', IntegerType(), True)]
    )
    json_df = df.selectExpr("cast(value as string) as value")
    json_expanded_df = json_df.withColumn("value", from_json(json_df["value"], json_schema)).select("value.*") 
    predict_df = json_expanded_df.withColumn("label", predict(json_expanded_df["text"]))
    df.withColumn("timestamp", current_timestamp())
    return predict_df

def save(output_df):
    query = output_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("checkpointLocation", "/tmp/spark_checkpoints") \
    .option("es.resource", ES_INDEX) \
    .start()
    query.awaitTermination()

spark = configure_spark()
predict = udf(predict_udf, StringType())
spark.udf.register("predict",predict)
broadcast_model(spark)
df = read_kafka(spark)
output_df = transform_data(df)
save(output_df)