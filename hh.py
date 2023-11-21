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
    # print(html_data.text)
    # print(html_data.status_code)

    job_search(raw_markup=html_data)


# 2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
def job_search(raw_markup):
    """
    Из HTML-массива извлекается каждая ссылка на вакансию и передаётся в parse_link_vacancy()
    :param raw_markup: HTML-массив
    :return: Список со списками, содержащие данные по вакансиям, удовлетворяющие ключевым словам
    """

    # list_search = ['Django', 'Flask']

    soup = BeautifulSoup(raw_markup.text, features='html.parser')

    # извлекаем посты
    posts = soup.find(name='main', class_='vacancy-serp-content')
    # print(posts)
    # name_tag = posts.find_all(class_='serp-item__title')
    name_tag = posts.find_all(name='a', class_='serp-item__title')

    list_of_suitable_vacancies = []

    for vacancy in name_tag:
        name_vacancy = vacancy.text
        # print(f'name_vacancy: <{name_vacancy}>')
        # words_list = name_vacancy.split()

        link_vacancy = vacancy.get('href')
        # print(f'link_vacancy: <{link_vacancy}>')
        vacancy_data = parse_link_vacancy(link_vacancy)

        if vacancy_data is not None:
            list_of_suitable_vacancies.append(vacancy_data)
        # else:
        #     print('Нет совпадений')
        #
        # print('\n')

    # return list_of_suitable_vacancies
    print(list_of_suitable_vacancies)


def parse_link_vacancy(link):
    """
    Переходит по ссылке и ищет те вакансии, у которых в описании есть ключевые слова 'Django' и 'Flask'
    :param link: ссылка на вакансию
    :return: если условие соблюдается - список с данными о вакансии, иначе None
    """

    headers_gen = fake_headers.Headers(browser='firefox', os='win')

    html_page = requests.get(url=link, headers=headers_gen.generate())
    # print(html_page.status_code)

    soup = BeautifulSoup(html_page.text, features='html.parser')
    # print(soup)

    # извлекаем посты
    vacancy_description = soup.find(name='div', class_='g-user-content')
    # print(f'vacancy_description: <{vacancy_description.text}>')
    words_list_vacancy_description = vacancy_description.text.split()

    list_search = ['Django', 'Flask']

    answer = []

    for keywords in list_search:
        if keywords in words_list_vacancy_description:
            print(f'Вакансия содержит ключевое слово {keywords}')
            answer.append(vacancy_description.text)
        # else:
        #     print('Not in')

    if len(answer) > 0:
        return answer
    else:
        return None


# 3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.


###
html_data = get_response()
job_search(html_data)

