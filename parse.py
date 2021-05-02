import requests
from bs4 import BeautifulSoup
import re

URL = 'https://belgorod.ml-respect.ru/car/kia/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
    'accept': '*/*'
    }

def get_html(url, params=None):  # parse all pages
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div', class_='card-row--inner')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('div', class_='box-title').get_text(strip=True),
            #'link': item.find('a', class_='box-title', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href'],
            'link': item.find('a',class_='box-images transparent',href=True).get("href"),
            'price': item.find('div', class_='new-price').get_text(),
        })
    print(cars)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Подключение успешно')
        print(get_content(html.text))
    else:
        print('Ошибка подключения')


parse()
