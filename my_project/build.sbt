name := "KafkaStreamDemo"
organization := "guru.learningjournal"
version := "0.1"
scalaVersion   := "3.3.1"
autoScalaLibrary := false
val sparkVersion = "3.5.1"

val sparkDependencies = Seq(
    "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-sql-kafka-0-10" % sparkVersion
)

libraryDependencies ++= sparkDependencies