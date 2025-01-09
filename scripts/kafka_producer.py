from kafka import KafkaProducer
import requests
import json

KAFKA_TOPIC = "cotizaciones"
KAFKA_SERVER = "kafka:9092"

def fetch_and_send_to_kafka():
    url = 'https://dolarapi.com/v1/dolares'
    response = requests.get(url)

    if response.status_code == 200:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        data = response.json()
        producer.send(KAFKA_TOPIC, data)
        print("Datos enviados a Kafka")
        producer.close()
    else:
        raise Exception(f"Error al obtener datos: {response.status_code}")

if __name__ == "__main__":
    fetch_and_send_to_kafka()
