import org.apache.log4j.Logger
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, expr, from_json}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Dataset}



object KafkaStreamDemo extends Serializable {
  @transient lazy val logger: Logger = Logger.getLogger(getClass.getName)

  def main(args: Array[String]): Unit = {

    //Creating sparksession

      val spark = SparkSession.builder()
      .master("local[*]")
      .appName("Kafka Stream Demo")
      .config("spark.streaming.stopGracefullyOnShutdown", "true")
      .getOrCreate()

    // Define PostgreSQL connection properties
    val pgUrl = "jdbc:postgresql://localhost:5432/postgres" // Adjust the URL as needed
    val pgProperties = new java.util.Properties()
    pgProperties.setProperty("user", "postgres") // PostgreSQL username
    pgProperties.setProperty("password", "user") // PostgreSQL password


    val jsonSchema = new StructType()
      .add("Title", StringType)
      .add("Location", StringType)
      .add("Company", StringType)
      .add("Job type", StringType)
      .add("Job description", StringType)

      //creating the kafka dataframe
    val kafkaStreamDF = spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "jobposts")
      .option("startingOffsets", "earliest")
      .load()
    
// Convert value column (containing Kafka message) to string
    val kafkaDF = kafkaStreamDF.selectExpr("CAST(value AS STRING) as jsonString")

// Parse JSON string and convert it to DataFrame using the schema
    val jsonDF = kafkaDF
      .select(from_json(col("jsonString"), jsonSchema).as("data"))
      .select("data.*")

    def myFunc( batchDF:DataFrame, batchID:Long ) : Unit = {
    batchDF.write
          .mode("append")
          .jdbc(pgUrl, "jobs", pgProperties)
}



    // Write the data to PostgreSQL using the Spark JDBC API
    val query = jsonDF.writeStream
      .foreachBatch(myFunc _)
      .start()

    logger.info("Listening to Kafka")
    query.awaitTermination()
  }
}
