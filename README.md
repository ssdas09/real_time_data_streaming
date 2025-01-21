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
docker-compose up -d
```
