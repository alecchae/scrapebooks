import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

url = "http://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', {'class': 'product_pod'})


def addbooks(_writer, _next_books):
    for _book in _next_books:
        _title = _book.h3.a.attrs['title']
        _price = _book.select('.price_color')[0].get_text()
        _availability = _book.select('.availability')[0].get_text().strip()
        _url_title = _title.replace(" ", "%")
        _author_url = 'https://www.googleapis.com/books/v1/volumes?q=' + _url_title
        _resp = requests.get(_author_url)
        _json = _resp.json()
        _authors = json['items'][0]['volumeInfo']['authors']
        _author = ', '.join([str(elem) for elem in _authors])
        _writer.writerow([_title, _author, _price, _availability])


with open('books.csv', mode='w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Author', 'Price', 'Availability'])

    for book in books:
        title = book.h3.a.attrs['title']
        price = book.select('.price_color')[0].get_text()
        availability = book.select('.availability')[0].get_text().strip()
        url_title = title.replace(" ", "%")
        author_url = 'https://www.googleapis.com/books/v1/volumes?q=' + url_title
        resp = requests.get(author_url)
        json = resp.json()
        authors = json['items'][0]['volumeInfo']['authors']
        author = ', '.join([str(elem) for elem in authors])
        writer.writerow([title, author, price, availability])

    while True:
        next_page = soup.select_one('li.next>a')
        print(next_page)
        if next_page:
            next_url = next_page.get('href')
            url = urljoin(url, next_url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            next_books = soup.find_all('article', {'class': 'product_pod'})

            for book in next_books:
                title = book.h3.a.attrs['title']
                price = book.select('.price_color')[0].get_text()
                availability = book.select('.availability')[0].get_text().strip()
                url_title = title.replace(" ", "%")
                print(url_title)
                author_url = 'https://www.googleapis.com/books/v1/volumes?q=' + url_title
                print(author_url)
                resp = requests.get(author_url)
                json = resp.json()
                try:
                    authors = json['items'][0]['volumeInfo']['authors']
                    author = ', '.join([str(elem) for elem in authors])
                except KeyError:
                    author = None
                writer.writerow([title, author, price, availability])
        else:
            break

