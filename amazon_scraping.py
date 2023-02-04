import requests
from bs4 import BeautifulSoup
from csv import writer
import time

product_Url = []
product_title = []
product_price = []
product_rating = []
product_review = []
product_asin = []
product_description = []


def main(URL):
    # File = open("output.csv", "w", newline='',encoding="UTF-8")
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    # Making the HTTP Request
    webpage_all = requests.get(URL, headers=HEADERS)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage_all.content, "lxml")
    findall = soup.findAll("div", attrs={"data-component-type": "s-search-result"})
    # retrieving product URL
    try:
        for url in findall:
            url_parent = url.find("a",
                                  attrs={'class': 'a-link-normal s-underline-text s-underline-link-text '
                                                  's-link-style a-text-normal'}, href=True)
            product_url = 'https://www.amazon.com' + url_parent['href']
            product_Url.append(product_url)

            webpage_product = requests.get(product_url, headers=HEADERS)
            # Creating the Soup Object containing all data
            soup1 = BeautifulSoup(webpage_product.content, "lxml")

            # retrieving product title
            try:
                # Outer Tag Object
                title_string = url.find("span", attrs={'class': 'a-size-medium a-color-base '
                                                                'a-text-normal'}).text.strip().replace(',', '')
                product_title.append(title_string)
            except AttributeError:
                title_string = "NA"
                product_title.append(title_string)

            # retrieving Description
            try:
                _description = []
                description = soup1.find("div", attrs={'id': 'feature-bullets'})
                description = description.find("ul")
                description = description.findAll("li")
                for a in description:
                    _description.append(
                        '* ' + a.find("span", attrs={'class': 'a-list-item'}).text.strip().replace(',', ''))
                product_description.append(_description)
            except AttributeError:
                _description = "NA"
                product_description.append(_description)

            # retrieving Price
            try:
                price = url.find("span", attrs={'class': 'a-price-whole'}).string.strip().replace(',', '')
                product_price.append(price)
            except AttributeError:
                try:
                    price = url.find("span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
                    product_price.append(price)
                except:
                    price = "NA"
                    product_price.append(price)

            # retrieving product rating
            try:
                rating = url.find("i", attrs={'class': 'a-icon a-icon-star-small a-star-small-4 '
                                                       'aok-align-bottom'}).string.strip().replace(',', '')
                product_rating.append(rating)
            except AttributeError:
                try:
                    rating = url.find("span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
                    product_rating.append(rating)
                except:
                    rating = "NA"
                    product_rating.append(rating)

            #  retrieving Number of reviews
            try:
                review_count = url.find("div", attrs={'class': 'a-row a-size-small'})
                review_count = review_count.find("span", attrs={
                    'class': 'a-size-base s-underline-text'}).string.strip().replace('-', '')
                product_review.append(review_count)
            except AttributeError:
                review_count = "NA"
                product_review.append(review_count)

    except AttributeError:
        product_url = "NA"
        product_Url.append(product_url)
    # retrieving ASIN
    try:
        # Outer Tag Object
        all_asin = soup.findAll("div", attrs={"data-component-type": "s-search-result"})
        for asin in all_asin:
            asin_id = asin["data-asin"].strip()
            product_asin.append(asin_id)
    except AttributeError:
        asin_id = "NA"
        product_asin.append(asin_id)
    time.sleep(2)


if __name__ == '__main__':
    # opening our url file to access URLs
    file = open("url.txt", "r")
    # iterating over the urls
    for links in file.readlines():
        main(links)
        time.sleep(5)

    print('Product URL:', len(product_Url), product_Url)
    print('Product Title:', len(product_title), product_title)
    print('Product Price:', len(product_price), product_price)
    print('Product Rating:', len(product_rating), product_rating)
    print('Product Review:', len(product_review), product_review)
    print('Product ASIN:', len(product_asin), product_asin)
    print('Product Description:', len(product_description), product_description)

    with open("out.csv", "w", newline='', encoding='UTF-8') as f:
        thewriter = writer(f)
        header = ['Product Url', 'Product Title', 'Price', 'Rating', 'Number of Review', 'ASIN',
                  'Product Description']
        thewriter.writerow(header)
        for i in range(len(product_Url)):
            productInfo = [product_Url[i], product_title[i], product_price[i], product_rating[i], product_review[i], product_asin[i], product_description[i]]
            thewriter.writerow(productInfo)

