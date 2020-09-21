import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd


AREA_DICT = {
            'везде': [0, 'russia.'],
            'Россия': [113, 'russia.'],
            'Москва': [1, ''],
            'Санкт-Петербург': [2, 'spb.'],
            'МО': [2019, 'mo.']
        }

def get_jobs_data_list(target, vacancy_name, area='везде'):
    if target == 'hh':
        url_main = 'https://hh.ru'

        parameters = {
            'area': AREA_DICT[area][0],
            'text': vacancy_name,
            'page': 0           # пагинация с 0
        }
    elif target == 'superjob':
        url_main = f'https://{AREA_DICT[area][1]}superjob.ru'

        parameters = {
            'keywords': vacancy_name,
            'page': 1           # пагинация с 1
        }
        if area == 'Москва':
            parameters['geo[t][0]'] = 4
    else:
        return None

    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.83 Safari/537.36'}

    if target == 'hh':
        vacancy_list = []
        while True:
            response = requests.get(url_main + '/search/vacancy', params=parameters, headers=headers)

            soup = bs(response.text, 'html.parser')

            tag_div_list = soup.find_all('div', attrs={'data-qa': ['vacancy-serp__vacancy',
                                                                   'vacancy-serp__vacancy vacancy-serp__vacancy_premium']})

            for i in range(len(tag_div_list)):
                vacancy_item = {
                    'website': 'hh.ru',
                    'salary_min': None,
                    'salary_max': None,
                    'salary_comment': None
                }

                tag_a = tag_div_list[i].find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})

                vacancy_item['vacancy_name'] = tag_a.text
                vacancy_item['vacancy_url'] = tag_a['href']

                tag_a = tag_div_list[i].find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                if tag_a:
                    vacancy_item['employer_name'] = tag_a.text
                    vacancy_item['employer_url'] = url_main + tag_a['href']
                else:
                    vacancy_item['employer_name'] = None
                    vacancy_item['employer_url'] = None

                vacancy_item['location'] = tag_div_list[i].find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text

                try:
                    text_salary = tag_div_list[i].find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                except AttributeError:
                    vacancy_item['salary_currency'] = None
                else:
                    text_salary = text_salary.replace('\xa0', '')

                    vacancy_item['salary_currency'] = text_salary.split()[-1]

                    if text_salary[0] == 'о':
                        vacancy_item['salary_min'] = text_salary.split()[1]
                    elif text_salary[0] == 'д':
                        vacancy_item['salary_max'] = text_salary.split()[1]
                    else:
                        tmp = text_salary.split('-')
                        vacancy_item['salary_min'] = tmp[0]
                        vacancy_item['salary_max'] = tmp[1].split()[0]

                vacancy_list.append(vacancy_item)

            if soup.find('a', attrs={'data-qa': 'pager-next'}):
                parameters['page'] += 1
            else:
                break

        return vacancy_list
    elif target == 'superjob':
        vacancy_list = []

        while True:
            response = requests.get(url_main + '/vacancy/search/', params=parameters, headers=headers)

            soup = bs(response.text, 'html.parser')

            tag_div_list = soup.find_all('div', attrs={'class': 'Fo44F QiY08 LvoDO'})

            for i in range(len(tag_div_list)):
                vacancy_item = {
                    'website': 'superjob.ru',
                    'salary_min': None,
                    'salary_max': None,
                    'salary_currency': 'руб.',      # на superjob.ru только в рублях(?)
                    'salary_comment': None
                }

                tag_div_vacancy = tag_div_list[i].find('div', attrs={'class': '_3mfro PlM3e _2JVkc _3LJqf'})

                vacancy_item['vacancy_name'] = tag_div_vacancy.a.text
                vacancy_item['vacancy_url'] = url_main + tag_div_vacancy.a['href']

                tag_div_employer = tag_div_list[i].find('div', attrs={'class': '_3_eyK _3P0J7 _9_FPy'})

                tag_a = tag_div_employer.a

                if tag_a:
                    vacancy_item['employer_name'] = tag_a.text
                    vacancy_item['employer_url'] = url_main + tag_a['href']
                else:
                    vacancy_item['employer_name'] = None
                    vacancy_item['employer_url'] = None

                vacancy_item['location'] = tag_div_employer.find(lambda tag: tag.name == 'span' and not tag.attrs).text

                text_salary = tag_div_list[i].find('span', attrs={'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text

                text_salary = text_salary.replace('\xa0', '')

                if text_salary[0] == 'П':
                    vacancy_item['salary_comment'] = text_salary
                    vacancy_item['salary_currency'] = None
                elif text_salary[0] == 'о':
                    vacancy_item['salary_min'] = text_salary[2:-4]
                elif text_salary[0] == 'д':
                    vacancy_item['salary_max'] = text_salary[2:-4]
                else:
                    em_dash = chr(8212)
                    if text_salary.find(em_dash) == -1:
                        vacancy_item['salary_min'] = text_salary[:-4]
                        vacancy_item['salary_max'] = text_salary[:-4]
                    else:
                        tmp = text_salary[:-4].split(em_dash)
                        vacancy_item['salary_min'] = tmp[0]
                        vacancy_item['salary_max'] = tmp[1]

                vacancy_list.append(vacancy_item)

            if soup.find('a', attrs={'rel': 'next'}):
                parameters['page'] += 1
            else:
                break

        return vacancy_list
    else:
        return None



print('\n============= Домашняя работа 2 =============')
print('=============================================\n')

search_str = ''
while not search_str:
    search_str = input('Желаемая вакансия: ').strip()

search_area = None
while not search_area:
    try:
        search_area = \
            int(input('Регион поиска (везде - 1, Россия - 2, Москва - 3, С.-Петербург - 4, Моск. область - 5): ').strip())
    except:
        print('\t\tОшибка! Введите целое число от 1 до 5!')
    else:
        if search_area not in [1, 2, 3, 4, 5]:
            print('\t\tОшибка! Введите целое число от 1 до 5!')
            search_area = None

search_source = None
while not search_source:
    try:
        search_source = int(input('Источник данных (везде - 1, "hh.ru" - 2, "superjob.ru" - 3): ').strip())
    except:
        print('\t\tОшибка! Введите целое число от 1 до 3!')
    else:
        if search_source not in [1, 2, 3]:
            print('\t\tОшибка! Введите целое число от 1 до 3!')
            search_source = None

# Можно было легко обойтись без этого промежуточного словаря, но для тестирования нагляднее
search_area_dict = {
    1: 'везде',
    2: 'Россия',
    3: 'Москва',
    4: 'Санкт-Петербург',
    5: 'МО'
}

hh_vacancies = []
sj_vacancies = []
if search_source == 1:
    hh_vacancies = get_jobs_data_list('hh', search_str, search_area_dict[search_area])
    sj_vacancies = get_jobs_data_list('superjob', search_str, search_area_dict[search_area])
elif search_source == 2:
    hh_vacancies = get_jobs_data_list('hh', search_str, search_area_dict[search_area])
else:
    sj_vacancies = get_jobs_data_list('superjob', search_str, search_area_dict[search_area])

result_list = hh_vacancies + sj_vacancies

# Вывод на экран
print('\n\tРезультаты поиска:')
print(f'Кол-во вакансий: {len(result_list)}')
print('Список вакансий: ')
pprint(result_list)

result_file = f'{search_str}_{search_area_dict[search_area]}_{search_source}.csv'
print(f'\nРезультат также записан в файл "{result_file}"')

# Преобразование результата к DataFrame и сохранение в .csv
columns = list(result_list[0].keys())
result_dict = dict.fromkeys(columns)
for key in columns:
    result_dict[key] = []
for item in result_list:
    for key in columns:
        result_dict[key].append(item[key])

result_df = pd.DataFrame(result_dict)

result_df.to_csv(result_file, sep=';')