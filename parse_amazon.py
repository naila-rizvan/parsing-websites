import json
import random
from bs4 import BeautifulSoup
import requests

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

# Randomly choose a User-Agent from the list
headers = {'User-Agent': random.choice(user_agents)}


def get_product_links(query,page_num=1):

    search_url = f"https://www.amazon.in/s?k={query}&page={page_num}"       # Search URL Page wise
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')               # Parse scraped data as HTML

    links = soup.find_all(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    product_links = []

    # Build product links
    for link in links:
        link_href = link['href']
        if 'http' in link_href:
            full_url = link_href
        else:
            full_url = "https://www.amazon.in" + link_href
        product_links.append(full_url)

    return product_links

def extract_product_info(product_url):
    # Extract info from each product page
    source = requests.get(product_url,headers=headers)
    page = BeautifulSoup(source.content,"html.parser")

    # Extract Product Title, Price, Rating
    title = page.find(id="productTitle").get_text()
    price = page.find(class_='a-price-whole').get_text()
    rating = page.find("span",{"class":"a-icon-alt"}).get_text()

    title = title.strip()
    price = price[:-1]
    if rating is None:
        rating = "No Rating"
    else:
        rating = float(rating[0:3])

    product_info = {
        "product_name": title,
        "price": price,
        "rating": rating
    }

    return product_info


if __name__=="__main__":

    filename = 'Product Info.jsonl'

    with open(filename,'w') as file:
        page_number = 1

        while True:
            print(f"Searching page {page_number}...")

            prod_links = get_product_links("monitor",page_number)       # Search term - monitor
            prod_links = list(set(prod_links))                                # Remove duplicates from the list

            if not prod_links or page_number==2:
                break

            for product_url in prod_links:
                try:
                    prod_info = extract_product_info(product_url)
                    print(prod_info)
                    if prod_info:
                        file.write(json.dumps(prod_info)+"\n")              # Write as a JSON file
                except Exception as err:
                    print(f"Failed to process URL: {product_url}.\nError: {err}")

            page_number +=1
