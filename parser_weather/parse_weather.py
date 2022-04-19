import requests
from bs4 import BeautifulSoup as BS


def parse_weather(url):
    try:
        r = requests.get(url)
    except BaseException as Error:
        print('Не удалось открыть сайт')
        return
    html = BS(r.content, 'html.parser')
    weather_weak = {}
    for el in html.select('.bd1'):
        date = html.select('.date')
        month = html.select('.month')
        min_temperature = html.select(".min > span")
        max_temperature = html.select(".max > span")
        for i in range(len(date)):
            weather_weak[i] = f"Температура {date[i].text} {month[i].text}  от  {min_temperature[i].text} до {max_temperature[i].text}"
            print(weather_weak[i])


def main():
    url = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D1%87%D0%B5%D1%80%D0%BD%D0%B8%D0%B3%D0%BE%D0%B2'
    parse_weather(url)


if __name__ == '__main__':
    main()
