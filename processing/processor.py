import pika, sys, os

from contracts_pb2 import NewsMessage


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='news_processor')

    def callback(ch, method, properties, body):
        msg = NewsMessage()
        msg.ParseFromString(body)
        print(" [x] Received %r" % msg.Timestamp)

    channel.basic_consume(queue='news_processor', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
