from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient


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
                date = div.find('span', {'class': '_1h3Zg e5P5i _2hCDz _2ZsgW'}).text
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
                    'link': address,
                    'date': date
                })
            base_url = address + \
                       soup.find('a', {'class': 'icMQ_ bs_sM _3ze9n _3fOgw f-test-button-dalshe f-test-link-Dalshe'})[
                           'href']
        else:
            print('Ошибка')

    print(vacancies)
    client = MongoClient('localhost', 27017)
    db = client['job_db']
    collection = db["job"]
    collection.insert_many(vacancies)
    return vacancies
