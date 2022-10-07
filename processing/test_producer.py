import pika

from contracts_pb2 import NewsMessage

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='news_processor')

nm = NewsMessage(Timestamp=294738497)
channel.basic_publish(exchange='', routing_key='news_processor', body=nm.SerializeToString())
print("DONE")
connection.close()
