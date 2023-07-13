from config.config import PikaConfig
import pika
from pika.exchange_type import ExchangeType
from pika.channel import Channel
import logging

class PikaContainer:
    config = PikaConfig(
        load_type=PikaConfig.LoadType.ENV,
        config_file="config/config.yml",
        section="flask",
    )

    @classmethod
    @property
    def connection(cls) -> pika.BlockingConnection:
        logging.info(f"Connection object created: host={cls.config.rabbitmq_host}")
        return pika.BlockingConnection(pika.ConnectionParameters(cls.config.rabbitmq_host, 
            credentials=pika.PlainCredentials(cls.config.rabbitmq_username, 
                                           cls.config.rabbitmq_password)))

    @classmethod
    def get_channel(cls, connection: pika.BlockingConnection) -> Channel:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=cls.config.rabbitmq_exchange,
            exchange_type=ExchangeType.direct,
            passive=False,
            durable=True,
            auto_delete=False)
        channel.queue_declare(queue=cls.config.rabbitmq_queue, auto_delete=True)
        channel.queue_bind(
            queue=cls.config.rabbitmq_queue, 
            exchange=cls.config.rabbitmq_exchange, 
            routing_key=cls.config.rabbitmq_routing_key)
        channel.basic_qos(prefetch_count=1)
        return channel