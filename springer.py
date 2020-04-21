# Initial URL: https://www.springernature.com/gp/researchers/the-source/blog/blogposts-life-in-research/access-textbooks-for-free-during-the-coronavirus-lockdown/17897628
# You can copy from my Colab: https://colab.research.google.com/drive/1wFxT-LnLQ77t2uGOOOkR9WHa4Pq9yQ53
# Not tested in local environment

import requests
from bs4 import BeautifulSoup
from google.colab import drive
drive.mount('/content/drive')

s = requests.Session()
data = open('drive/My Drive/Colab Notebooks/springer.txt')

for link in data:
    #print(link)
    r = s.get(link, allow_redirects = True)
    if r.status_code==200:
        bsoup = BeautifulSoup(r.text, 'html.parser')
        book_title = bsoup.findAll('div', attrs={'class': 'page-title'})[0].find('h1').text
        print(book_title)
        all_links = bsoup.findAll('a', attrs={'title': 'Download this book in PDF format'})[0]['href']
        #print("http://link.springer.com" + all_links[0]['href']) # extract only first occurence
        #print("http://link.springer.com" + all_links) # extract only first occurence
        file_url = "http://link.springer.com" + all_links
        r = s.get(file_url, stream = True)
        with open("drive/My Drive/Colab Notebooks/" + book_title, "wb") as file:  
            for block in r.iter_content(chunk_size = 1024): 
                if block:  
                    file.write(block) 