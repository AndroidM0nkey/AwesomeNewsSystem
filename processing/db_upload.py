import pandas as pd
import pika
from contracts_pb2 import NewsMessage
import logging


def bd_update(csv: string, verbose=500):
    """
        input:
            csv: csv file path to data for update
            verbose: logging info, show every i % verbose iterations
    """
    df = pd.read_csv()
    
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='news_processor')

    for i in range(len(df)):
        try:
            title = df.loc[i].title
            text = df.loc[i].text
            
            nm = NewsMessage(
                Title=title,
                Body=text,
                Timestamp=20
            )
            channel.basic_publish(exchange='', routing_key='news_processor', body=nm.SerializeToString())

            if verbose != 0 and (i + 1) % verbose == 0:
                print(f'Added {i + 1} / {len(df)} records')
        except Exception as e:
            logging.warning(f'Error at {i}:\n{repr(e)}')


    print("DONE")
    connection.close()