# %pip install requests
# %pip install bs4

import requests
from bs4 import BeautifulSoup
import csv

def parse(html):
    csv_header = ["Название", "Автор", "Ссылка"]
    csv_rows = []

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id = "restab")
    rows = table.css.select('tr[bgcolor="#f5f5f5"]')
    for i in range(min(len(rows), 30)):
        cell = rows[i].contents[3]
        a = cell.find('a')
        url = "https://www.elibrary.ru" + a['href']
        title = a.string
        font = cell.css.select('font[color="#00008f"]')
        author = font[0].string

        csv_rows.append([title, author, url])

        with open('result.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, quoting = csv.QUOTE_ALL)
            writer.writerow(csv_header)
            writer.writerows(csv_rows)
        
    print("ready")

search_form_data = {
    "where_fulltext": "on",
    "where_name": "on",
    "where_abstract": "on",
    "where_keywords": "on",
    "where_affiliation": "on",
    "where_references": "on",
    "type_article": "on",
    "type_disser": "on",
    "type_book": "on",
    "type_report": "on",
    "type_conf": "on",
    "type_patent": "on",
    "type_preprint": "on",
    "type_grant": "on",
    "type_dataset": "on",
    "search_freetext": "",
    "search_morph": "on",
    "search_fulltext": "",
    "search_open": "",
    "search_results": "",
    "titles_all": "",
    "authors_all": "",
    "rubrics_all": "",
    "queryboxid": "",
    "itemboxid": "",
    "begin_year": "",
    "end_year": "",
    "issues": "all",
    "orderby": "rank",
    "order": "rev",
    "changed": "1",

    "ftext": "webassembly", # поисковый запрос
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Referer": "https://www.elibrary.ru/"
}

s = requests.Session()

login = input("Введите логин: ")
password = input("Введите пароль: ")

login_form_data = {
    "rpage": "https://elibrary.ru/defaultx.asp",
    "login": login,
    "password": password
}

response = s.post("https://www.elibrary.ru/start_session.asp", files = login_form_data, headers = headers) # тут он хочет именно formdata, поэтому параметр files
print(response.status_code)

response = s.post(url = "https://www.elibrary.ru/query_results.asp", data = search_form_data, headers = headers) # а тут хавает из параметра data
if (response.status_code == 200):
    print(200)
    parse(response.text)
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(response.text)
