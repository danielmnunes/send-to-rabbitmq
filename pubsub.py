import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import pubsub_v1

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
TOPIC_ID = os.getenv("GCP_TOPIC_ID", "")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def publicar_mensagem(payload: dict, **atributos: str) -> str:
    data = json.dumps(payload).encode("utf-8")
    future = publisher.publish(topic_path, data=data, **atributos)
    message_id = future.result()
    print(f"Mensagem publicada: {message_id}")
    return message_id


def send_json_files(input_dir: Path) -> None:
    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        print(f"No .json files found in '{input_dir}'")
        return

    for json_file in json_files:
        payload = json.loads(json_file.read_text(encoding="utf-8"))
        publicar_mensagem(payload, filename=json_file.name)

    print(f"\nDone. {len(json_files)} message(s) sent to topic '{topic_path}'.")


def main() -> None:
    if not PROJECT_ID or not TOPIC_ID:
        raise ValueError("GCP_PROJECT_ID and GCP_TOPIC_ID must be set in .env")
    send_json_files(Path("input"))


if __name__ == "__main__":
    main()
