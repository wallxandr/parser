import json
import bs4
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def get_data(url):
    result = []
    city = url.split('/')[7]

    for i in range(1, 26):
        req = url + str(i)

        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = r"D:\programming\python\chromedriver.exe"
        driver = webdriver.Chrome(
            chrome_driver_binary, chrome_options=options)

        driver.get(req)
        WebDriverWait(driver, 10)
        data = driver.page_source
        driver.close()

        soup = bs4.BeautifulSoup(data, 'html.parser')
        cards = soup.select('div[data-cy="l-card"]')

        try:
            for card in cards:
                current_site = {}
                current_site['href'] = ('https://www.olx.ua') + \
                    str(card.find('a').get('href'))
                current_site['name'] = card.find('h6').text
                current_site['price'] = ''.join(
                    [n for n in card.find('p').text if n.isdigit()])
                result.append(current_site)
            time.sleep(random.randint(4, 5))
        except (NameError, AttributeError):
            break

    with open(f'olx_result_{city}.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    get_data(
        'https://www.olx.ua/d/nedvizhimost/kvartiry/prodazha-kvartir/kiev/?currency=UAH&page=')


if __name__ == "__main__":
    main()
