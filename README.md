# send-to-rabbitmq

Sends all `.json` files from the `input/` folder to a RabbitMQ queue.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package manager
- [Docker](https://www.docker.com/) — optional, for containerized runs and local RabbitMQ

## Setup

### 1. Configure environment variables

Copy `.env.example` to `.env` and fill in your RabbitMQ credentials:

```sh
cp .env.example .env
```

| Variable           | Default      | Description              |
|--------------------|--------------|--------------------------|
| `RABBITMQ_HOST`    | `localhost`  | RabbitMQ server hostname |
| `RABBITMQ_PORT`    | `5672`       | AMQP port                |
| `RABBITMQ_USER`    | `guest`      | Username                 |
| `RABBITMQ_PASSWORD`| `guest`      | Password                 |
| `RABBITMQ_VHOST`   | `/`          | Virtual host             |
| `RABBITMQ_QUEUE`   | `json_files` | Target queue name        |

### 2. Add JSON files

Place the `.json` files you want to send inside the `input/` folder:

```
input/
  order-001.json
  order-002.json
```

## Running

### With uv (local)

```sh
uv run main.py
```

### With Docker

**Start a local RabbitMQ instance:**

```sh
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

**Build and run the application:**

```sh
docker build -t send-to-rabbitmq .
docker run --env-file .env --network host send-to-rabbitmq
```

## Verifying

Open the RabbitMQ management UI at [http://localhost:15672](http://localhost:15672) (default credentials: `guest` / `guest`), go to **Queues**, and check the `json_files` queue (or your configured queue name) to confirm messages arrived.
