import json
import os
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv()


def get_connection_params() -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(
        username=os.getenv("RABBITMQ_USER", "guest"),
        password=os.getenv("RABBITMQ_PASSWORD", "guest"),
    )
    return pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
    )


def send_json_files(input_dir: Path, queue_name: str) -> None:
    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        print(f"No .json files found in '{input_dir}'")
        return

    connection = pika.BlockingConnection(get_connection_params())
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    properties = pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
        content_type="application/json",
    )

    for json_file in json_files:
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json_file.read_bytes(),
            properties=properties,
        )
        print(f"Sent: {json_file.name}")

    connection.close()
    print(f"\nDone. {len(json_files)} message(s) sent to queue '{queue_name}'.")


def main() -> None:
    queue_name = os.getenv("RABBITMQ_QUEUE", "json_files")
    input_dir = Path("input")
    send_json_files(input_dir, queue_name)


if __name__ == "__main__":
    main()
