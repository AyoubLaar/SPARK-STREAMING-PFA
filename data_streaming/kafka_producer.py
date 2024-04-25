from confluent_kafka import Producer
import csv
import time

# Kafka broker configuration
bootstrap_servers = 'localhost:9092'
topic = 'jobposts'

# Function to publish CSV data to Kafka topic
def publish_csv_to_kafka(file_path):
    # Create Kafka Producer instance
    producer = Producer({'bootstrap.servers': bootstrap_servers})

    # Read CSV file and publish each line as a message to Kafka
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # Convert row to string and send to Kafka topic
            producer.produce(topic, str(row).encode('utf-8'))
            # Flush messages to ensure they are sent immediately
            producer.flush()
            # Introduce a delay (optional)
            time.sleep(1)

    # Close the Kafka Producer
    producer.flush()
    producer.close()

# Example usage
file_path = '/home/noureddine/Desktop/VS code coding/python/indeed-job-analysis/IT.csv'
publish_csv_to_kafka(file_path)
