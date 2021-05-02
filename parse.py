import requests
from bs4 import BeautifulSoup

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
    items = soup.find_all('div', class_='box-title')
    print(items)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Подключение успешно')
        print(get_content(html.text))
    else:
        print('Ошибка подключения')


parse()
