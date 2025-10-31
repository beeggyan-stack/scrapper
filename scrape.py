# python -m pip install requests
# => get data from web (html, json, xml)
# python -m pip install beautifulsoup4
# => parse html


import requests
from bs4 import BeautifulSoup


url = "http://books.toscrape.com/"


def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the page.")
        return []

    # Set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    all_books = []
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        all_books.append(
            {
                "title": title,
                "currency": currency,
                "price": price,
            }
        )
    return all_books


books = scrape_books(url)

with open("books.json", "w", encoding="utf-8") as f:
    import json
    
    json.dump(books, f, indent=4, ensure_ascii=False)
