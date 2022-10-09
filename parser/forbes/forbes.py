from requests import get
from bs4 import BeautifulSoup
from time import sleep
from contracts_pb2 import ParsedArticle
from datetime import datetime

page_url = "https://www.forbes.ru/tegi/ekonomika?page=1"
base_url = "https://www.forbes.ru"

INTERVAL = 10 # in seconds 
processed = "processed.txt"
queue = "news_processor"

def validate(href):
    with open(processed,'r',encoding = 'utf-8') as f:
        data = f.read()
        if data.find(href) > -1:
            return False
        else:
            return True

def processed_href(href):
    with open(processed,'a',encoding = 'utf-8') as f:
        f.write(href + "\n")

def start():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    while 1:
        r = get(page_url)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, 'html.parser') 
        for block in soup.find_all('div', class_="_3dtP5"):
            title = ""
            href = ""
            if block.find('div', class_="_2npuA"): # big
                title = block.find('div', class_="_2npuA").find('div', class_="_1fQ6O").get_text()
                href = block.find('div', class_="_2npuA").find('a', class_="_1QIeJ")["href"]
            elif block.find('div', class_="laBq1 _1Lp5N"): # small with pic
                title = block.find('div', class_="laBq1 _1Lp5N").find('p', class_="_3Ew4G").get_text()
                href = block.find('div', class_="laBq1 _1Lp5N").find('a', class_="_3eGVH")["href"]
            elif block.find('div', class_="laBq1"): # small no pic
                title = block.find('div', class_="laBq1").find('div', class_="_2iYJc").get_text()
                href = block.find('div', class_="laBq1").find('a', class_="_3eGVH")["href"]
            else:
                continue
            if not validate(href):
                continue
            r_cur = get(base_url + href)
            if r_cur.status_code != 200:
                continue
            soup_cur = BeautifulSoup(r_cur.text, 'html.parser') 
            text = ""
            for art in soup_cur.find_all('p', itemprop="articleBody"):
                text += art.get_text(separator=" ").strip() + "\n"
            if text == "":
                continue
            # print(title) # to queue
            nm = ParsedArticle(
                    Title=title.strip(),
                    Body=text,
                    Timestamp=datetime.utcnow().timestamp()
                )
                channel.basic_publish(exchange='', routing_key='rbc', body=nm.SerializeToString())
            processed_href(href)
        sleep(INTERVAL)
    connection.close()

if __name__ == '__main__':
    start()