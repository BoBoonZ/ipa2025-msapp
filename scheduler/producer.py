import pika
import os

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_user = os.getenv("RABBITMQ_USER", "admin")
rabbitmq_pass = os.getenv("RABBITMQ_PASS", "rabbitmq")


def produce(host, body):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    )

    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(
        queue="router_jobs",
        exchange="jobs",
        routing_key="check_interfaces",
    )

    channel.basic_publish(
        exchange="jobs",
        routing_key="check_interfaces",
        body=body,
    )

    connection.close()


if __name__ == "__main__":
    produce("localhost", "192.168.1.44")
