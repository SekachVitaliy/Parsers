import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from random import uniform


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.content


def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(ua)


def main():
    url = 'http://sitespy.ru/my-ip'

    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')

    for i in range(10):
        sleep(uniform(3, 6))
        print(1)
        proxy = {'http': 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(useragents)}
        try:
            html = get_html(url, useragent, proxy)
        except:
            continue
        get_ip(html)


if __name__ == '__main__':
    main()
