import requests
import csv
from bs4 import BeautifulSoup as BS


def get_html(page, price_found):
    try:
        url = f'https://auto.ria.com/search/?categories.main.id=1&region.id[' \
              f'0]=6&price.USD.lte={price_found}&price.currency=1&abroad.not=0&custom.not=1&page={page}&size=10'
        r = requests.get(url)
        global html
        html = BS(r.content, 'html.parser')
    except Exception:
        print('Ошибка открытия')
        return 0


def parse_avtoria(pages, price_found):
    ote4estvennie_avto = {'УАЗ', 'ВАЗ', 'ЗАЗ', 'ЛАДА', 'НИВА', 'ГАЗ'}
    ote4estvennie = open("ote4estvennie.txt.txt", "w", encoding="utf-8")
    inomarki = open("inomarki.txt.txt", "w", encoding="utf-8")
    print("Файл открыт ")
    for page in range(pages):
        get_html(page, price_found)
        element = 16
        while element <= 28:
            car_links = str(html.select(f'#searchResults > section:nth-child({element}) > div.content-bar > '
                                        f'div.content > div.head-ticket > div > a'))
            price = str(html.select(f'#searchResults > section:nth-child({element}) > div.content-bar > div.content > '
                                    f'div.price-ticket > span > span:nth-child(1)'))
            element += 1
            link = car_links[car_links.find('href="') + 6:car_links.find('" target')]
            text = car_links[car_links.find('title="') + 7:car_links.find('">')]
            price = price[price.find('USD">') + 5:price.find('</span')]
            if price:
                if ote4estvennie_avto & set(text.split()):
                    car = f'{text}, {price}, USD , {link}\n'
                    inomarki.write(car)
                else:
                    car = f'{text}, {price}, USD, {link}\n'
                    ote4estvennie.write(car)

    inomarki.close()
    ote4estvennie.close()
    print("Файл закрыт")


def main():
    pages = int(input('Введите количество страниц для поиска:'))
    price_found = int(input('До какой суммы искать авто?'))
    parse_avtoria(pages, price_found)


if __name__ == '__main__':
    main()
