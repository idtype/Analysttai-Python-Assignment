from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import makecsv as msv
from bs4 import BeautifulSoup
import json

service = Service(executable_path='./webdriver/chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument("--window-size=640,560")
chrome_options.add_argument('--no-sandbox')


def get_urls(main_url, todo_items=0):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    items_parsed = 0
    items = []
    driver.get(main_url)
    while items_parsed < todo_items:
        data = BeautifulSoup(driver.page_source, "html.parser")
        for item in data.select('div[data-asin][data-index]:not([data-asin=""])'):
            # title = item.select('div.s-title-instructions-style')[0].text
            asin = item['data-asin']
            title = item.select('h2>a>span')[0].text
            price_elem = item.select_one('span.a-price-whole')
            price = None
            if price_elem is not None:
                price = price_elem.text
            stars = None
            raters = None
            if len(item.select('span[aria-label$="stars"]')) > 0:
                stars = item.select('span[aria-label$="stars"]')[0]['aria-label'].split(' ')[0]
                raters = item.select('span[aria-label$="stars"]+span[aria-label]')[0]['aria-label']
            # link = 'https://amazon.in' + item.select('span[data-component-type] > a')[0]['href']
            link = 'https://amazon.com/dp/' + asin
            item_info = {
                'title': title, 'price': price, 'link': link,
                'stars': stars, 'ratings': raters, 'asin': asin,
                'features': [], 'manufacturer': "", 'description': ""
            }
            items.append(item_info)
            items_parsed += 1
        print(items)
        next_page = data.select_one("a.s-pagination-next:not(.s-pagination-disabled)")
        print(next_page)
        if next_page is not None:
            url = '/'.join(driver.current_url.split('/')[:3]) + next_page['href']
            driver.get(url)
        else: break
    driver.close()
    return items


def get_extra_details(items):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    for item in items:
        driver.get(item['link'])
        page = BeautifulSoup(driver.page_source, "html.parser")
        if 'not found' in page.select_one('title').text.lower():
            print("ASIN:{} Skipped".format(item['asin']))
            continue
        item['features'] = [d.text.strip() for d in page.select('div#feature-bullets li:not([id])')]
        prdesc = page.select_one('div#productDescription')
        if prdesc is not None:
            item['description'] = prdesc.text.strip()

        info_table = page.select('table#productDetails_detailBullets_sections1 tr')
        for info in info_table:
            # print(info)
            info_key = info.select_one('th').text.strip()
            if info_key.lower() != 'manufacturer': continue
            info_value = info.select('td.prodDetAttrValue')
            if len(info_value) > 0:
                info_value = info_value[0].text.strip()
                item['manufacturer'] = info_value
            break
    driver.close()


if __name__ == '__main__':
    initial_url = "https://www.amazon.in/s?k=bags&crid=2UUIZ0NGD3CYV&sprefix=bags%2Caps%2C888"
    bag_data = get_urls(initial_url, 200)
    get_extra_details(bag_data)
    msg = msv.make_csv(bag_data, "bags")
    print(msg)



