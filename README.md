# Iceberg Kafka Connect Docker Setup

This repository provides a comprehensive Docker Compose setup for integrating **Apache Kafka**, **Kafka Connect**, **Iceberg**, **MinIO**, and **Trino**. It includes a Python script that simulates the production of messages to a Kafka topic. These messages are then consumed by Kafka Connect and inserted into an **Apache Iceberg** table using the Kafka Iceberg connector. The messages are stored in **MinIO**, which acts as the storage backend for Iceberg.

## Architecture

The system architecture is composed of the following services:

- **Kafka Broker**: The core message broker that handles the production and consumption of messages.
- **Kafka Connect**: The connector framework that pulls messages from Kafka and inserts them into Iceberg.
- **Iceberg Rest API**: Provides a REST interface for interacting with Iceberg, managing metadata, and loading data.
- **MinIO**: Acts as a scalable S3-compatible storage for Iceberg data.
- **Trino**: An SQL query engine used to query Iceberg tables.
- **Spark with Iceberg**: A Spark cluster integrated with Iceberg, allowing the processing of data stored in Iceberg tables.
- **mc (MinIO Client)**: A utility to configure and interact with MinIO.

## Prerequisites

- Docker
- Docker Compose
- Python 3.x (for the `main.py` script)

## Quick Start

To get up and running with the provided Docker Compose setup and Python script, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

### 2. Start the Docker Containers

Use Docker Compose to build and start all the services in the background.

```bash
docker-compose up -d
```

This command will bring up the following services:
- Kafka Broker
- Kafka Connect
- Iceberg Rest API
- MinIO (for storage)
- Trino
- Spark with Iceberg
- MinIO Client (`mc`)

### 3. Create a Kafka Topic

After the Docker containers are up and running, you need to create a Kafka topic for the producer to send messages to.

Run the following command to create the `yellow-taxi` topic:

```bash
docker exec -t broker kafka-topics --create --topic yellow-taxi --partitions 6 --bootstrap-server broker:9092
```

### 4. Configure Kafka Connect to Use the Iceberg Sink Connector

Next, you need to configure Kafka Connect to consume messages from the `yellow-taxi` Kafka topic and insert them into an Iceberg table. You can do this by sending a `POST` request with the configuration for the **Iceberg Sink Connector**.

Use `curl` to send the configuration to the Kafka Connect REST API:

```bash
curl -X POST \
  http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iceberg-sink-connector",
    "config": {
      "connector.class": "io.tabular.iceberg.connect.IcebergSinkConnector",
      "tasks.max": "6",
      "topics": "yellow-taxi",
      "iceberg.tables": "taxi.yellow",
      "iceberg.catalog": "nyc",
      "iceberg.catalog.type": "rest",
      "iceberg.catalog.uri": "http://iceberg-rest:8181",
      "iceberg.catalog.client.region": "us-east-1",
      "iceberg.catalog.s3.endpoint": "http://minio:9000",
      "iceberg.catalog.s3.path-style-access": "true",
      "iceberg.tables.auto-create-enabled": "true",
      "iceberg.tables.evolve-schema-enabled": "true",
      "iceberg.control.commit.interval-ms": 180000,
      "key.converter": "org.apache.kafka.connect.storage.StringConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter.schemas.enable": "false"
    }
  }'
```

This configuration sets up the Kafka Connect **Iceberg Sink Connector** to consume from the `yellow-taxi` topic and insert the messages into the `taxi.yellow` Iceberg table, using MinIO as the S3-compatible storage backend.

### 5. Produce Messages to Kafka

Once the Kafka topic and the Kafka Connect configuration are set up, you can produce messages to the `yellow-taxi` Kafka topic.

You can use the `main.py` script to produce test messages. Run the following Python script to produce messages:

```bash
python main.py
```

The script will send messages to the Kafka topic `yellow-taxi`. Kafka Connect will then process these messages and insert them into the Iceberg table.

### 6. Query Data Using Trino

Trino is configured to connect to the Iceberg tables. You can query the Iceberg tables via the Trino web UI available at [http://localhost:8085](http://localhost:8085).

Example query to check the inserted data:

```sql
SELECT * FROM iceberg_catalog.schema_name.table_name;
```

### 7. Explore Spark Integration

The Spark cluster integrated with Iceberg allows you to process the data stored in Iceberg tables. You can use Jupyter notebooks (available on port 8888) to explore and query data from the Iceberg tables.

## Docker Compose Services

### 1. **broker** (Kafka Broker)
- **Image**: `confluentinc/cp-kafka:7.4.1`
- **Ports**: `29092:29092` (External Kafka listener)
- **Environment**: Configured for KRaft mode (no Zookeeper).

### 2. **connect** (Kafka Connect)
- **Image**: `confluentinc/cp-kafka-connect-base:7.3.0`
- **Ports**: `8083:8083` (Kafka Connect REST API)
- **Environment**: Configured with the Iceberg Kafka connector.

### 3. **spark-iceberg**
- **Image**: `tabulario/spark-iceberg`
- **Ports**: `8888:8888` (Jupyter Notebooks), `8080:8080` (Spark UI)
- **Volumes**: Mounts local directories for warehouse and notebooks.

### 4. **rest** (Iceberg REST API)
- **Image**: `tabulario/iceberg-rest`
- **Ports**: `8181:8181`
- **Environment**: Configured to connect to MinIO as the Iceberg storage backend.

### 5. **minio**
- **Image**: `minio/minio`
- **Ports**: `9000:9000` (MinIO API), `9001:9001` (MinIO Console)
- **Environment**: Configured with MinIO access keys.

### 6. **mc** (MinIO Client)
- **Image**: `minio/mc`
- Configures MinIO storage, creates the `warehouse` bucket, and sets the access policy.

### 7. **trino**
- **Image**: `trinodb/trino`
- **Ports**: `8085:8080` (Trino Web UI)
- **Environment**: Configured to connect to Iceberg tables.

## File Descriptions

- **docker-compose.yml**: Defines all the services and their configurations.
- **main.py**: Python script that produces messages to Kafka.
- **iceberg-kafka-connect-0.6.19**: The Iceberg Kafka connector, mounted as a volume in the Kafka Connect container.

## Troubleshooting

- If services are not starting properly, check the logs of individual containers using:

  ```bash
  docker-compose logs <service_name>
  ```

- To restart the services after changes, run:

  ```bash
  docker-compose down
  docker-compose up --build
  ```

## Conclusion

This setup provides a simple, end-to-end pipeline for producing, processing, and querying data with Apache Kafka, Iceberg, and MinIO. The integration allows for scalable, distributed data storage and querying, with an easy-to-use interface through Trino and Spark.

Happy coding! 🎉
