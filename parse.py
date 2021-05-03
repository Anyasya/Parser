import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://belgorod.ml-respect.ru/car/'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
    'accept': '*/*'
    }

HOST = 'https://belgorod.ml-respect.ru'

FILE = 'cars.csv'
def get_html(url, params=None):  # parse all pages
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_='page_list')
    if pagination:
        return pagination.text[-2]
    else:
        return 1

def save_file(items,path):
     with open (path,'w',newline='') as file:
         writer = csv.writer(file,delimiter = ';')
         writer.writerow(['Марка','Цена','Ссылка'])
         for item in items:
             writer.writerow([item['title'], item['price'], item['link']])


def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div', class_='card-row--inner')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('div', class_='box-title').get_text(strip=True),
            'link': HOST + item.find('a',class_='box-images transparent',href=True).get("href"),   # find.find_next
            'price': item.find('div', class_='new-price').get_text()
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        page_count = int(get_pages_count(html.text))
        for page in range(1,page_count + 1):
            print('Парсинг',page,'страницы из',page_count,'страниц...')
            html = get_html(URL + f'?PAGEN_1={page}')
            cars.extend(get_content(html.text))
            save_file(cars, FILE)
        print('Сохранено', len(cars), 'запись(-ей)')


    else:
        print('Ошибка подключения')


parse()
