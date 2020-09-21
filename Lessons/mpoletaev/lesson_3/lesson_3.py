import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient


AREA_DICT = {
            'везде': [0, 'russia.'],
            'Россия': [113, 'russia.'],
            'Москва': [1, ''],
            'Санкт-Петербург': [2, 'spb.'],
            'МО': [2019, 'mo.']
        }

def get_jobs_data_list(target, vacancy_name, area='везде', no_duplicate=True):
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
        return 0

    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.83 Safari/537.36'}

    if target == 'hh':
        write_count = 0
        while True:
            if write_count % 100 == 0:
                print(f'Идет обработка запроса к "hh.ru" (уже добавлено записей: {write_count})')

            response = requests.get(url_main + '/search/vacancy', params=parameters, headers=headers)

            soup = bs(response.text, 'html.parser')

            tag_div_list = soup.find_all('div', attrs={'data-qa': ['vacancy-serp__vacancy',
                                                                   'vacancy-serp__vacancy vacancy-serp__vacancy_premium']})

            for i in range(len(tag_div_list)):
                vacancy_item = {
                    'website': 'hh.ru',
                    'salary_min': None,
                    'salary_max': None,
                    'salary_comment': None,
                    'search query': vacancy_name
                }

                tag_a = tag_div_list[i].find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})

                vacancy_item['vacancy_id'] = int(tag_a['href'].split('?')[0].split('/')[-1])

                if no_duplicate:
                    if mongo.find_one({'website': 'hh.ru', 'vacancy_id': vacancy_item['vacancy_id']}):
                        continue

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
                        vacancy_item['salary_min'] = int(text_salary.split()[1])
                    elif text_salary[0] == 'д':
                        vacancy_item['salary_max'] = int(text_salary.split()[1])
                    else:
                        tmp = text_salary.split('-')
                        vacancy_item['salary_min'] = int(tmp[0])
                        vacancy_item['salary_max'] = int(tmp[1].split()[0])

                # Запись в MongoDB
                mongo.insert_one(vacancy_item)
                write_count += 1

            if soup.find('a', attrs={'data-qa': 'pager-next'}):
                parameters['page'] += 1
            else:
                break

        return write_count
    elif target == 'superjob':
        write_count = 0

        while True:
            if write_count % 100 == 0:
                print(f'Идет обработка запроса к "superjob.ru" (уже добавлено записей: {write_count})')

            response = requests.get(url_main + '/vacancy/search/', params=parameters, headers=headers)

            soup = bs(response.text, 'html.parser')

            tag_div_list = soup.find_all('div', attrs={'class': 'Fo44F QiY08 LvoDO'})

            for i in range(len(tag_div_list)):
                vacancy_item = {
                    'website': 'superjob.ru',
                    'salary_min': None,
                    'salary_max': None,
                    'salary_currency': 'руб.',      # на superjob.ru только в рублях(?)
                    'salary_comment': None,
                    'search query': vacancy_name
                }

                tag_div_vacancy = tag_div_list[i].find('div', attrs={'class': '_3mfro PlM3e _2JVkc _3LJqf'})

                vacancy_item['vacancy_id'] = int(tag_div_vacancy.a['href'].split('-')[-1][:-5])

                if no_duplicate:
                    if mongo.find_one({'website': 'superjob.ru', 'vacancy_id': vacancy_item['vacancy_id']}):
                        continue

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
                    vacancy_item['salary_min'] = int(text_salary[2:-4])
                elif text_salary[0] == 'д':
                    vacancy_item['salary_max'] = int(text_salary[2:-4])
                else:
                    em_dash = chr(8212)
                    if text_salary.find(em_dash) == -1:
                        vacancy_item['salary_min'] = int(text_salary[:-4])
                        vacancy_item['salary_max'] = int(text_salary[:-4])
                    else:
                        tmp = text_salary[:-4].split(em_dash)
                        vacancy_item['salary_min'] = int(tmp[0])
                        vacancy_item['salary_max'] = int(tmp[1])

                # Запись в MongoDB
                mongo.insert_one(vacancy_item)
                write_count += 1

            if soup.find('a', attrs={'rel': 'next'}):
                parameters['page'] += 1
            else:
                break

        return write_count
    else:
        return 0


def print_vacancies_by_min_salary(min_salary):
    result = mongo.find({'$or': [{"salary_min": {'$gt': min_salary}}, {"salary_max": {'$gt': min_salary}}]}, {'_id': 0})

    print('\nРезультат поиска:')

    count = 0
    for item in result:
        pprint(item)
        count += 1

    print(f'Всего найдено в БД записей: {count}')


def delete_vacancies_by_id(vacancies_list):
    for id in vacancies_list:
        mongo.delete_one({'vacancy_id': id})


print('\n============= Домашняя работа 2 =============')
print('=============================================')

# Стартуем MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['db_vacancies']
mongo = db.vacancies

while True:
    print('\n\t_______ Меню _______')
    print('\t1. Добавить новые вакансии в БД.')
    print('\t2. Поиск вакансий в БД по заданной зарплате.')
    print('\t3. Удаление вакансий из БД.')
    print('\t(E)xit - для выхода из программы.')

    menu_item = ''
    while not menu_item:
        menu_item = input('\t...ваши действия: ').strip().lower()
        if menu_item not in ['1', '2', '3', 'e', 'exit']:
            print('\t\tВыберите один из пунктов меню!')
            menu_item = ''
        else:
            print()

    if menu_item == '1':
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

        hh_write_count = 0
        sj_write_count = 0
        if search_source == 1:
            hh_write_count = get_jobs_data_list('hh', search_str, search_area_dict[search_area])
            sj_write_count = get_jobs_data_list('superjob', search_str, search_area_dict[search_area])
        elif search_source == 2:
            hh_write_count = get_jobs_data_list('hh', search_str, search_area_dict[search_area])
        else:
            sj_write_count = get_jobs_data_list('superjob', search_str, search_area_dict[search_area])

        result_count = hh_write_count + sj_write_count

        # Вывод на экран
        print('\n\tРезультаты поиска:')
        print(f'Кол-во вакансий внесенных в БД: {result_count} ("hh.ru": {hh_write_count}; "superjob.ru": {sj_write_count})')

        input('\n\t\tДля продолжения нажмите любую клавишу...')

    elif menu_item == '2':
        salary_search = None
        while not salary_search:
            try:
                salary_search = int(input('Введите минимальную желаемую зарплату: ').strip())
            except:
                print('\t\tОшибка! Введите целое число!')
                salary_search = None
            else:
                if salary_search < 0:
                    print('\t\tОшибка! Введите целое неотрицательное число!')
                    salary_search = None

        print_vacancies_by_min_salary(salary_search)

        input('\n\t\tДля продолжения нажмите любую клавишу...')

    elif menu_item == '3':
        vacancies_id = None
        while not vacancies_id:
            vacancies_id = input('Введите id вакансий для удаления (можно несколько, через пробел): ').strip().split()
            if not len(vacancies_id):
                print('\t\tОшибка! Введите хотя бы одно значение!')
            else:
                for i in range(len(vacancies_id)):
                    try:
                        vacancies_id[i] = int(vacancies_id[i])
                    except:
                        print('\t\tОшибка! Идентификаторы вакансий должны быть целыми положительными числами!')
                        vacancies_id = None
                        break

                if vacancies_id:
                    delete_vacancies_by_id(vacancies_id)
    else:
        break