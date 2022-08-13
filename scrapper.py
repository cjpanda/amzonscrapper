import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep 


headers = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'})

search_query = 'home office'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

items = []
for i in range(1, 5):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # items.extend(soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'}))
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text 
        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span',  {'aria-label': True})[1].text
        except AttributeError:
            continue
        try:
            price =result.find('span', {'class': 'a-offscreen'}).text
            # price1 = result.find('span', {'class': 'a-price-whole'}).text
            # price2 = result.find('span', {'class': 'a-price-fraction'}).text
            # price = float(price1 + price2)
            product_url = 'http://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    sleep(1.5)

df = pd.DataFrame(items, columns=['Product', 'Rating', 'Rating Count', 'Price', 'Url'])
df.to_csv('{0}.csv'.format(search_query), index=False)


