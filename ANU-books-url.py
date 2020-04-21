import requests
from bs4 import BeautifulSoup
import re
import csv

s = requests.Session()
book_links = []
pdf_links = {}

r = s.get("https://press.anu.edu.au/publications/books")
if r.status_code==200:
    bsoup = BeautifulSoup(r.text, 'html.parser')
    lastpage = bsoup.findAll('li', attrs={'class': 'page-item'})[-1].text
    all_links = bsoup.findAll('a', text="Download for free")
    for link in all_links:
        book_links.append("https://press.anu.edu.au" + link['href'])

for i in range(1, int(lastpage)):
    r = s.get("https://press.anu.edu.au/publications/books?p=" + str(i))
    if r.status_code==200:
        bsoup = BeautifulSoup(r.text, 'html.parser')
        all_links = bsoup.findAll('a', text="Download for free")
        for link in all_links:
            book_links.append("https://press.anu.edu.au" + link['href'])
print("Books found: " + str(len(book_links)))
print(book_links)

f = open('ANU-books.csv', 'a+', newline='')
with f:
    for book_link in book_links:
        r = s.get(book_link)
        if r.status_code==200:
            bsoup = BeautifulSoup(r.text, 'html.parser')
            file_url = bsoup.findAll('a', attrs={'class': 'pub-citation-download-btn'})[0]['href']
            book_title = re.sub(r'[^\sa-zA-Z0-9\\-]', "_", str(bsoup.title.text))
            savedata = [book_title, file_url]       
            writer = csv.writer(f)
            writer.writerow(savedata)
