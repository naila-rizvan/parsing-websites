import random
import requests
from bs4 import BeautifulSoup
import csv

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

# Randomly choose a User-Agent from the list
headers = {'User-Agent': random.choice(user_agents)}

# Get the source code of the web page
source = requests.get("https://themondebooks.com/blog/", headers=headers).text

# Parse the source code as HTML code
soup = BeautifulSoup(source,'lxml')
# print(soup.prettify())

csv_file = open("blog_list.csv","w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline','Summary','Blog Link'])


articles = soup.find_all("div", class_="elementor-image-box-content")

for article in articles:
    headline = article.a.string
    summary = article.p.text
    link = article.a['href']
    print(headline)
    print(summary)
    print(link)
    print()
    csv_writer.writerow([headline,summary,link])


csv_file.close()