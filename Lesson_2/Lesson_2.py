# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
# Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (отдельно минимальную и максимальную).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии
# (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
# from fake_headers import Headers # падал с ошибкой
# ERROR: Could not find a version that satisfies the requirement Headers (from versions: none)
# Не смогла зарезолвить
import re


def parse_hh(address, vacancy, pages):
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 '
                             'Safari/537.36'}
    html = requests.get(
        address + '/search/vacancy?clusters=true&enable_snippets=true&text=' + vacancy + '&showClusters=true',
        headers=headers).text
    parsed_html = bs(html, 'lxml')

    vacancies = []
    for i in range(pages):
        jobs_block = parsed_html.find('div', {'class': 'vacancy-serp'})
        jobs_list = jobs_block.findChildren(recursive=False)
        for job in jobs_list:
            job_data = {}
            req = job.find('span', {'class': 'g-user-content'})
            if req is not None:
                main_info = req.findChild()
                job_name = main_info.getText()
                job_link = main_info['href']
                salary = job.find('div', {'class': 'vacancy-serp-item__compensation'})
                if not salary:
                    salary_min = None
                    salary_max = None
                else:
                    salary = salary.getText().replace(u'\xa0', u'')
                    salaries = salary.split('-')
                    salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
                    salary_min = int(salaries[0])
                    if len(salaries) > 1:
                        salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                        salary_max = int(salaries[1])
                    else:
                        salary_max = None
                job_data['name'] = job_name
                job_data['salary_min'] = salary_min
                job_data['salary_max'] = salary_max
                job_data['link'] = job_link
                job_data['site'] = address
                vacancies.append(job_data)

        next_btn_block = parsed_html.find('a', {'class': 'bloko-button'})
        next_btn_link = next_btn_block['href']
        html = requests.get(address + next_btn_link, headers=headers).text
        parsed_html = bs(html, 'lxml')

    print(vacancies)
    return vacancies


parse_hh('https://nn.hh.ru', 'Data Scientist', 2)


def parse_sj(address, vacancy, pages):
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 '
                             'Safari/537.36'}
    base_url = address + '/vacancy/search/?keywords=' + vacancy
    vacancies = []
    session = requests.Session()
    for i in range(pages):
        request = session.get(base_url, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', {'class': '_31XDP iJCa5 f-test-vacancy-item _1fma_ _2nteL'})
            for div in divs:
                common = div.find('div', {'class': '_1h3Zg _2rfUm _2hCDz _21a7u'})
                title = common.text
                href = common.contents[0].attrs['href']
                salary = div.find('span',
                                  {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).text
                salary = salary.replace(u'\xa0', u'')
                if '—' in salary:
                    salary_min = salary.split('—')[0]
                    salary_min = re.sub(r'[^0-9]', '', salary_min)
                    salary_max = salary.split('—')[1]
                    salary_max = re.sub(r'[^0-9]', '', salary_max)
                    salary_min = int(salary_min)
                    salary_max = int(salary_max)
                elif 'от' in salary:
                    salary_min = salary[2:]
                    salary_min = re.sub(r'[^0-9]', '', salary_min)
                    salary_min = int(salary_min)
                    salary_max = None
                elif 'договорённости' in salary:
                    salary_min = None
                    salary_max = None
                elif 'до' in salary:
                    salary_min = None
                    salary_max = salary[2:]
                    salary_max = re.sub(r'[^0-9]', '', salary_max)
                    salary_max = int(salary_max)
                else:
                    salary_min = int(re.sub(r'[^0-9]', '', salary))
                    salary_max = int(re.sub(r'[^0-9]', '', salary))

                vacancies.append({
                    'title': title,
                    'href': 'https://www.superjob.ru' + href,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'link': address
                })
            base_url = address + \
                       soup.find('a', {'class': 'icMQ_ bs_sM _3ze9n _3fOgw f-test-button-dalshe f-test-link-Dalshe'})['href']
        else:
            print('Ошибка')

    print(vacancies)
    return vacancies


parse_sj('https://russia.superjob.ru', 'Python', 2)
