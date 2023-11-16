import fake_headers
import requests
from bs4 import BeautifulSoup


# Попробуем получать интересующие вакансии на сайте headhunter самыми первыми :)
# https://spb.hh.ru/

# 1. Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург".
# Эти параметры задаются по ссылке https://spb.hh.ru/search/vacancy?text=python&area=1&area=2

def get_response():
    parse_link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    headers_gen = fake_headers.Headers(browser='firefox', os='win')

    html_data = requests.get(url=parse_link, headers=headers_gen.generate())
    # print(html_data.text)
    print(html_data.status_code)

    job_search(raw_markup=html_data)


# 2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
def job_search(raw_markup):
    list_search = ['Django', 'Flask']

    soup = BeautifulSoup(raw_markup.text, features='html.parser')

    # извлекаем посты
    posts = soup.find(name='main', class_='vacancy-serp-content')
    # print(posts)
    # name_tag = posts.find_all(class_='serp-item__title')
    name_tag = posts.find_all(name='a', class_='serp-item__title')

    suitable_data = []

    for vacancy in name_tag:
        # name_vacancy = vacancy.text
        # words_list = name_vacancy.split()

        link_vacancy = vacancy.get('href')
        vacancy_data = parse_link_vacancy(link_vacancy)

        if vacancy_data is not None:
            suitable_data.append(vacancy_data)
        else:
            continue


def parse_link_vacancy(link):
    """
    Переходит по ссылке и ищет те вакансии, у которых в описании есть ключевые слова 'Django' и 'Flask'
    """
    headers_gen = fake_headers.Headers(browser='firefox', os='win')

    html_data = requests.get(url=link, headers=headers_gen.generate())
    print(html_data.status_code)

    soup = BeautifulSoup(html_data.text, features='html.parser')

    # извлекаем посты
    posts = soup.find(name='main', class_='vacancy-serp-content')



# 3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.


###
get_response()