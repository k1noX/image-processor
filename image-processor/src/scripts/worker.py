import pika, sys
import logging
import functools
from pika.exchange_type import ExchangeType
import pika.exceptions

sys.path.append('../src')

from injectors.pika import PikaContainer
from services.processing import process_task, finish_task_with_error

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def on_message(chan, method_frame, header_frame, body, userdata=None):
    LOGGER.info('Delivery properties: %s, message metadata: %s', method_frame, header_frame)
    LOGGER.info('Userdata: %s, message body: %s', userdata, body)
    id = int(body)
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)
    try:
        process_task(id)
    except Exception as e:
        finish_task_with_error(id, ''.join(e.args))

def main():
    connection = PikaContainer.connection

    channel = PikaContainer.get_channel(connection)

    on_message_callback = functools.partial(
        on_message, userdata='on_message_userdata')
    channel.basic_consume(PikaContainer.config.rabbitmq_queue, 
                          on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


logging.info(f"Worker loaded")
if __name__ == "__main__":
    main()
