from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame
from time import sleep

INTERVAL = 10 # in seconds 
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
        r = get(f"https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=economics&limit=20")
        print(r.status_code)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.json()["html"], 'html.parser')
        # print(soup.prettify())
        for a in soup.find_all('a', class_="item__link"):
            title = a.get_text().strip().replace(""" 
                                                    """, " ")
            cur_href = a["href"]

            if not validate(cur_href):
                continue
            r_cur = get(a["href"])
            if r.status_code != 200:
                continue
            soup_cur = BeautifulSoup(r_cur.text, 'html.parser')
            art = BeautifulSoup(r_cur.text, 'html.parser').find('div', class_="article__text article__text_free")
            if art.find('div', "article__main-image"):
                art.find('div', "article__main-image").decompose()
            if art.find('div', "video-autoplay-recommend"):
                art.find('div', "video-autoplay-recommend").decompose()
            if art.find('div', "article__inline-item"):
                art.find('div', "article__inline-item").decompose()
            if art.find('div', "pro-anons__wrapper"):
                art.find('div', "pro-anons__wrapper").decompose()
            if art.find('div', "article__tabs-wrapper js-article-tabs-wrapper"):
                art.find('div', "article__tabs-wrapper js-article-tabs-wrapper").decompose()
            if art.find('a', "social-networks js-social-networks js-yandex-counter"):
                art.find('a', "social-networks js-social-networks js-yandex-counter").decompose()
            text = art.get_text(separator=" ").strip()
            text = text.replace("     www.adv.rbc.ru      ", "")
            text = text.replace("\n", "")
            print(title) # publish to queue
            processed_href(cur_href)
        sleep(INTERVAL)

if __name__ == '__main__':
    start()