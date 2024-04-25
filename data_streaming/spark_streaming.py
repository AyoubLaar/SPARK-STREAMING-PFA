from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType
import os
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.13:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1 pyspark-shell'


# Initialize SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Define schema for CSV data
schema = StructType() \
    .add("Poste date", StringType()) \
    .add("Title", StringType()) \
    .add("Location", StringType()) \
    .add("Company", StringType()) \
    .add("Job type", StringType()) \
    .add("Job description", StringType()) \

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "jobposts") \
    .load()

# Parse CSV data
parsed_df = df.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("data")).select("data.*")

#write data to the console
query = parsed_df \
    .writeStream \
    .format("console") \
    .start()

query.awaitTermination()

# Perform processing on the data
#processed_df = parsed_df ...

# Write data to PostgreSQL
'''query = processed_df \
    .writeStream \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/your_database") \
    .option("dbtable", "your_table") \
    .option("user", "your_username") \
    .option("password", "your_password") \
    .start()

query.awaitTermination()'''
