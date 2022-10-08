from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pandas import DataFrame
from pathlib import Path
from logging import warning
from time import sleep
 
INTERVAL = 10 # seconds

base_url = "https://www.consultant.ru"
news_url = "https://www.consultant.ru/legalnews/"
processed = "processed.txt"


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
    while 1:
        session = HTMLSession()
        resp = session.get(news_url)
        if resp.status_code != 200:
            warning(f"got {resp.status_code} for base url")
            break
        resp.html.render(timeout=20)
        soup = BeautifulSoup(resp.html.html, 'html.parser')

        for item in soup.find_all('div', class_='listing-news__item'):
            res = {"title":"", "text":"", "ts":""}
            cur_href = item.find('a', class_='listing-news__item-title')["href"]
            if not validate(cur_href):
                continue
            cur_url = base_url + cur_href
            resp_cur = session.get(cur_url)
            if resp_cur.status_code != 200:
                warning(f"got {resp_cur.status_code} for url {cur_url}")
                break
            res["title"] = item.find('a', class_='listing-news__item-title').get_text()
            res["ts"] = item["data-published-at"]
            resp_cur.html.render(timeout=20)
            soup_cur = BeautifulSoup(resp_cur.html.html, 'html.parser').find(class_="news-page__content")
            res["text"] = soup_cur.get_text(separator=' ')
            print(res["title"]) # send to queue
            processed_href(cur_href)
        sleep(INTERVAL)

if __name__ == '__main__':
    start()