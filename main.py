import requests
import csv
from bs4 import BeautifulSoup as bs

def write_to(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['pricebucks'], data['price'], data['image'], data['description']])

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('ul', class_="pagination").find_all('a')[-1].attrs.get('data-page')
    if page_list is not None:
        return int(page_list)
    else:
        return 0

def get_data(html):
    soup = bs(html, 'lxml')
    carlist = soup.find('div', class_='table-view-list').find_all('div', class_='list-item list-label')

    for cars in carlist:
        try:
            title = cars.find('div', class_="block title").find('h2').text.strip()
        except AttributeError:
            title = ''

        try:
            pricebucks = cars.find('div', class_="block price").find('strong').text.split()
            pricebucks = ' '.join(pricebucks)
        except AttributeError:
            pricebucks = ''

        try:
            price = cars.find('div', class_="block price").find('p').text.replace(pricebucks, '').split()
            price = ' '.join(price)
        except AttributeError:
            price = ''

        try:
            image = cars.find('div', class_="thumb-item-carousel").find('img').attrs.get('data-src')
        except:
            image = ''

        try:
            description = cars.find('div', class_="block info-wrapper item-info-wrapper").text.split()
            description = ''.join(description)
        except AttributeError:
            description = ''

        product_dict = {
            'title': title,
            'pricebucks': pricebucks,
            'price': price,
            'image': image,
            'description': description
        }

        write_to(product_dict)

        for i in product_dict:
            f = 'вы успешно спарсили'
            print(i, f'{f}')

def main():
    base_url = 'https://www.mashina.kg/search/all/'
    html = get_html(base_url)
    number = get_total(html)
    for i in range(1, number + 1):
        url_with_page = base_url + f'?page={i}'
        html = get_html(url_with_page)
        get_data(html)

with open('data.csv', 'w') as file:
   writer = csv.writer(file)
   writer.writerow(['title', 'pricebucks', 'price', 'image', 'description'])

main()
