# 1.Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД.


from pymongo import MongoClient
import re
from Get_Vacancies import parse_sj
import datetime as dt

client = MongoClient('localhost', 27017)
db = client['job_db']
collection = db["job"]
vacancies = parse_sj('https://russia.superjob.ru', 'Python', 2)
collection.insert_many(vacancies)
inserted_data = collection.find({}).limit(3)

print(inserted_data)


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
def get_vacancy_by_salary():
    salary = input('Please enter the minimum salary')
    for row in collection.find({'salary_min': {'$gt': int(salary)}}):
        print(row)


get_vacancy_by_salary()


# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
def insert_new_vacancies(vac_list):
    month = {'января': '01',
             'февраля': '02',
             'марта': '03',
             'апреля': '04',
             'мая': '05',
             'июня': '06',
             'июля': '07',
             'августа': '08',
             'сетября': '09',
             'октября': '10',
             'ноября': '11',
             'декабря': '12'}

    def is_date_fresh(str_date):
        week_ago_date = dt.date.today() - dt.timedelta(days=7)
        date_dic = str_date.split()
        parsed_day = date_dic[0]
        parsed_month = str(month.get(date_dic[1]))
        year_today = str(dt.date.today().year)
        collected_date = parsed_day + '-' + parsed_month + '-' + year_today
        converted_date = dt.datetime.strptime(collected_date, "%d-%m-%Y").date()
        if converted_date >= week_ago_date:
            return True
        else:
            return False

    for row in vac_list:
        date = row['date']
        is_date_vchera = date == 'Вчера'
        is_date_today = re.match(r"[0-9]{2}:[0-9]{2}", date)
        if is_date_vchera or is_date_today or is_date_fresh(date):
            collection.insert_one(row)
            # print(row)


insert_new_vacancies(vacancies)
