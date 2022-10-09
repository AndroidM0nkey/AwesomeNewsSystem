import pika

from contracts_pb2 import NewsMessage

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='news_processor')

nm = NewsMessage(
    Title='Минэкономразвития резко улучшило прогноз спада ВВП России',
    Body='Минэкономразвития резко улучшило прогноз спада российской экономики в ближайшие годы. Новым прогнозом глава министерства Максим Решетников поделился в среду, 21 сентября, в рамках правительственного часа в Совете Федерации, передает «Интерфакс».',
    Timestamp=20
)
channel.basic_publish(exchange='', routing_key='news_processor', body=nm.SerializeToString())
print("DONE")
connection.close()
