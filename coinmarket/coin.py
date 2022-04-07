import requests
from bs4 import BeautifulSoup
import csv
import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('tbody').find_all('tr', class_='cmc-table-row')
    links = []
    for i in table:
        a = i.find('a', class_='cmc-link').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links


def get_page(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = soup.find('h2').text.strip()
    except:
        name = ''

    try:
        price = soup.find('div', class_='priceValue').text.strip()
    except:
        price = ''

    data = {'name': name,
            'price': price}

    return data


def write_csv(data):
    with open('coin.csv', 'a', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['price']))
        print(data['name'], 'parsed')


def get_csv(url):
        html = get_html(url)
        data = get_page(html)
        write_csv(data)


def main():
    start = datetime.datetime.now()
    url = 'https://coinmarketcap.com/ru/all/views/all'
    links = get_links(get_html(url))
    with Pool(40)as p:
        p.map(get_csv, links)
    end = datetime.datetime.now()
    print(end - start)


if __name__ == '__main__':
    main()
