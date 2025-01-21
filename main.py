import pandas as pd
from confluent_kafka import Producer
import json

# Kafka configuration
kafka_config = {
    'bootstrap.servers':'localhost:29092',  # Replace with your Kafka broker
}
kafka_topic = 'yellow-taxi'  # Replace with your Kafka topic name

# Initialize Kafka producer
producer = Producer(kafka_config)
print(producer)

def delivery_report(err, msg):
    """Callback function for delivery report."""
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record {msg.key()} successfully sent to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Read Parquet file
parquet_file = r"C:\Users\swayam.das\Downloads\yellow_tripdata_2024-01 (1).parquet"  # Replace with the path to your Parquet file
df = pd.read_parquet(parquet_file)
df['tpep_pickup_datetime']=df['tpep_pickup_datetime'].astype(str)
df['tpep_dropoff_datetime']=df['tpep_dropoff_datetime'].astype(str)
print(df.info())
# Send rows to Kafka topic
for index, row in df.iterrows():
    try:
        # Convert row to JSON
        message = row.to_dict()
        producer.produce(
            kafka_topic,
            key=str(index),  # Use index as key
            value=json.dumps(message),
            callback=delivery_report
        )
        producer.flush()  # Ensure messages are sent
    except Exception as e:
        print(f"Error sending record {index}: {e}")

print("Finished sending records to Kafka.")
