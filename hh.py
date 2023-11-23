import json
import time
from pprint import pprint

import fake_headers
import requests
from bs4 import BeautifulSoup


# Попробуем получать интересующие вакансии на сайте headhunter самыми первыми :)
# https://spb.hh.ru/

# 1. Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург".
# Эти параметры задаются по ссылке https://spb.hh.ru/search/vacancy?text=python&area=1&area=2

def get_response():
    """
    Парсит страницу hh с поиском по "Python" и городами "Москва" и "Санкт-Петербург"
    :return:массив HTML
    """

    parse_link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    headers_gen = fake_headers.Headers(browser='firefox', os='win')

    html_data = requests.get(url=parse_link, headers=headers_gen.generate())

    return html_data

    # job_search(raw_markup=html_data)


# 2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
def job_search(raw_markup):
    """
    Из HTML-массива извлекается каждая ссылка на вакансию и передаётся в parse_link_vacancy()
    :param raw_markup: HTML-массив
    :return: Список со списками, содержащие данные по вакансиям, удовлетворяющие ключевым словам
    """

    soup = BeautifulSoup(raw_markup.text, features='html.parser')

    posts = soup.find(name='main', class_='vacancy-serp-content')
    name_tag = posts.find_all(name='a', class_='serp-item__title')

    list_of_suitable_vacancies = []

    for vacancy in name_tag:
        link_vacancy = vacancy.get('href')
        vacancy_data = parse_link_vacancy(link_vacancy)

        if vacancy_data is not None:
            list_of_suitable_vacancies.append(vacancy_data)

    pprint(list_of_suitable_vacancies)
    return list_of_suitable_vacancies


def parse_link_vacancy(link):
    """
    Переходит по ссылке и ищет в описании ключевые слова 'Django' и 'Flask'
    :param link: ссылка на вакансию
    :return: если условие соблюдается - список с данными о вакансии (ссылка, вилка зп, название компании, город),
    иначе None
    """

    headers_gen = fake_headers.Headers(browser='firefox', os='win')
    html_page = requests.get(url=link, headers=headers_gen.generate())
    soup = BeautifulSoup(html_page.text, features='html.parser')
    name_vacancy = soup.find(name='h1', class_='bloko-header-section-1').text
    vacancy_description = soup.find(name='div', class_='g-user-content')
    words_list_vacancy_description = vacancy_description.text.split()

    list_search = ['Django', 'Flask']

    for keywords in list_search:
        if keywords in words_list_vacancy_description:
            print(f'Вакансия <{name_vacancy}> содержит ключевое слово {keywords}')

            salary = soup.find(name='div', class_='vacancy-title').contents[2].text.replace('\xa0', ' ')
            name_company = (soup.find(name='div', class_='vacancy-company-redesigned').text.split('\n')[0].
                            replace('\xa0', ' '))
            city = soup.find(name='div', class_='vacancy-company-redesigned').contents[5].text.split(', ')[0]

            vacancy_dict = {
                'link': link,
                'salary': salary,
                'name_company': name_company,
                'city': city
            }

            print(vacancy_dict, '\n')
            return vacancy_dict


# 3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.
def extract_data_in_json(data):
    """
    Записывает данные в JSON
    :param data: данные которые необходимо записать в json
    :return: json
    """
    json_information = json.dumps(data)
    return json_information


while True:
    try:
        html_data = get_response()
        list_of_suitable_vacancies = job_search(html_data)
        json_info = extract_data_in_json(list_of_suitable_vacancies)
        print(json_info)
        break
    except AttributeError as error:
        print(f'Возникла ошибка <{error}>.\nВероятно страница не прогрузилась до конца. Подождите...')
        time.sleep(3)
        print('Повторная попытка сбора данных')
