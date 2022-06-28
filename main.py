from urllib import response
import requests
from bs4 import BeautifulSoup
import json
from random import randrange
import time
from requests.exceptions import TooManyRedirects



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def get_articles_urls(url):
    with requests.Session() as session:
        response = session.get(url=url, headers=headers)
    s = requests.session()

    soup = BeautifulSoup(response.text, 'lxml')
    pnavigation_count = int(soup.find('div', class_='pagination').find_all('a')[-2].text)
    

    articls_url_list = []

    
    for page in range (1, pnavigation_count + 1):
    # for page in range (1, 50):
        url = f'https://1progs.ru/page/{page}/'

        response = s.get(url=f'https://1progs.ru/page/{page}/', headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'lxml')

        articls_url= soup.find_all('a', class_='read_more')


        for au in articls_url:
            art_url = au.get('href', allow_redirects=False)
            articls_url_list.append(art_url)
        
        print(f'Обработано {page}/{pnavigation_count}')

    with open('articls_url.txt', 'w', encoding='utf-8') as file:
        for url in articls_url_list:
            file.write(f"{url}\n")

    # with open('index.html', 'w', encoding="utf-8") as file:
    #     file.write(response.text)

def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    urls_count = len(urls_list)
    s = requests.session()
    rsult_data = []



    for url in enumerate(urls_list[:100]):
        response = s.get(url=url[1], headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'lxml')

        # time.sleep(randrange(2, 5))

        try:
            articl_link_download = soup.find('blockquote').find('a').get('href').strip()
        except AttributeError:
            articl_link_download = 'None'

        try:
            article_password = soup.find('strong').text.strip() 
        except AttributeError:
            article_password = 'None'

        try:
            article_title = soup.find('header', class_='entry-header').find('h1', class_='entry-title').text.strip()
        except AttributeError:
            article_title = 'None'
            
        try:
            article_text = soup.find('div', class_='entry-content').find('p').text.strip()
        except AttributeError:
            article_text = 'None'       

        try:
           article_img = soup.find('div', class_='entry-content').find('img', class_="size-full").get('src')   
        except AttributeError:
            article_img = 'None'



        rsult_data.append(
            {
                'original_url': url[1],
                'article_title': article_title,
                'article_text': article_text,
                'article_img': article_img,
                'articl_link_download': articl_link_download,
                'article_password': article_password
            }
        )
        print(f'Обработал {url[0] + 1}/{urls_count}')


    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(rsult_data, file, indent=4, ensure_ascii=False)


def main():
    # get_articles_urls(url='https://1progs.ru/')
    get_data('articls_url.txt')


if __name__ == '__main__':
    main()