import org.apache.log4j.Logger
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, expr, from_json}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._


object KafkaStreamDemo extends Serializable {
  @transient lazy val logger: Logger = Logger.getLogger(getClass.getName)

  def main(args: Array[String]): Unit = {

    //Creating sparksession
    val spark = SparkSession.builder()
      .master("local[3]")
      .appName("Kafka Stream Demo")
      .config("spark.streaming.stopGracefullyOnShutdown", "true")
      .getOrCreate()

    //determine csv schema
    val schema = StructType(
      StructField("Poste date", StringType),
      StructField("Title", StringType),
      StructField("Location", StringType),
      StructField("Company", StringType),
      StructField("Job type", StringType),
      StructField("Job description", StringType))

      //creating the kafka dataframe
    val kafkaStreamDF = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "jobposts")
      .option("startingOffsets", "earliest")
      .load()
    
// Convert value column (containing Kafka message) to string
    val kafkaDF = kafkaStreamDF.selectExpr("CAST(value AS STRING)")

    // Print the content of the DataFrame to the console
    val query = kafkaDF
      .writeStream
      .outputMode("append")
      .format("console")
      .start()

    logger.info("Listening to Kafka")
    query.awaitTermination()}}
