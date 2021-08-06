# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
# pip install PyGithub requests

import requests
import pandas as pd

header = {
    "Accept": "application/vnd.github.v3+json"
}

url = "https://api.github.com/users/coryphanta/repos"

response = requests.get(url, headers=header).json()
pd.DataFrame(response).to_json("repos.json")

print(response)

# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

url = 'https://api.github.com/user'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
          'login':'testGB123',
          'password':'uAcH9QWNN5XXaFy',
          'authenticity_token':'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',
          'commit':'Sign in',
          'utf8':'%E2%9C%93'
}

response = requests.post(url)
pd.DataFrame(response).to_json("auth.json")

print(response)