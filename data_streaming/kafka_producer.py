import csv
import json
import time
from confluent_kafka import Producer

# Kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address (adjust as needed)
}

# Kafka topic
topic = 'jobposts'  # Specify the Kafka topic you want to produce messages to

# CSV file path
file_path = 'data_streaming/IT.csv'  # Specify the path to the CSV file

# Function to produce messages to Kafka with real-time simulation
def produce_messages(file_path, delay=1.0):
    # Create Kafka Producer instance
    producer = Producer(kafka_config)

    # Read CSV file and produce each row as a message to Kafka
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        # Create a CSV reader
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV data
        for row in csv_reader:
            # Convert the row dictionary to a JSON string
            json_string = json.dumps(row)

            # Produce the message to the Kafka topic
            producer.produce(topic, key=None, value=json_string.encode('utf-8'))

            # Optional: Handle delivery reports for messages
            producer.poll(0)

            # Introduce a delay to simulate real-time data streaming
            time.sleep(delay)

    # Flush any remaining messages
    producer.flush()

    print(f"Data produced to Kafka topic '{topic}' at a rate of {delay} seconds per message.")

# Run the function to produce messages from the CSV file with a delay
produce_messages(file_path, delay=1.0)
