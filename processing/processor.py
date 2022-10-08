import pika, sys, os

import grpc
from contracts_pb2 import NewsMessage
import contracts_pb2_grpc

import psycopg2


MODEL_SERVICE_IP = 'localhost:8001'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='news_processor')

    def callback(ch, method, properties, body):
        msg = NewsMessage()
        msg.ParseFromString(body)

        with grpc.insecure_channel(MODEL_SERVICE_IP) as channel:
            stub = contracts_pb2_grpc.ModelServiceStub(channel)
            response = stub.GetModelServiceAnswer(msg)

        msg.ML.CopyFrom(response)

        conn = psycopg2.connect(dbname='db', user='postgres', 
                        password='postgres', host='localhost')
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()

        for item in msg.ML.Categories:
            print(" [x] Received" + str(item.Probability))

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
