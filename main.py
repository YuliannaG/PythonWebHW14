import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import asyncio

from model import Book, Base


def parse_data():
    library_ = []
    url = 'https://ottawa.bibliocommons.com/explore/bestsellers/5925_new_york_times/'
    while True:
        html_doc = requests.get(url)
        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            books = soup.find('div', attrs={'class': 'cp_bib_list clearfix'}).find_all('div', attrs={'class': 'col-xs-12 list_item_outer clearfix'})
            for book in books:
                img_url = book.find('img')['src']
                rating = book.find('div', class_="cp_ratings")['data-rating_value']
                title = book.find('span', class_="title").text
                author = None
                try:
                    author_bulk = book.find('a', class_="author_detail_link").text
                    author = re.match(r'^[A-Za-z]*, [A-Za-z]*', author_bulk).group(0)
                except AttributeError:
                    pass
                category = book.find('span', class_="value bestSellerCategory").text
                position_in_category = book.find_all('span', class_="value")[2].text

                available = "No information"
                try:
                    if book.find('button', class_="btn btn-highlight btn-block"):
                        available = "Not available"
                    else:
                        available = "Available"
                except AttributeError:
                    pass
                library_.append({
                    'img_url': img_url,
                    'rating': rating,
                    'title': title,
                    'author': author,
                    'category': category,
                    'position_in_category': position_in_category,
                    'available': available
                })
                # print(title)
            try:
               nextpage = soup.find('a', testid="link_nextpage")['href']
               url = f'https://ottawa.bibliocommons.com{nextpage}'
            except TypeError:
                break
    return library_


if __name__ == '__main__':
    library = parse_data()
    engine = create_engine("sqlite:///nyt_books.db")
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    session = Session()
    for el in library:
        library_book = Book(img_url=el.get('img_url'), rating=el.get('rating'), title=el.get('title'),
                            author=el.get('author'), category=el.get('category'),
                            position_in_category=el.get('position_in_category'), available=el.get('available'))
        session.add(library_book)
    session.commit()
    session.close()
