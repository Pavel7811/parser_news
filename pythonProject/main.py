

import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient

def insert_document(collection, data):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id
# Imports and previous code truncated for brevity

def find_document(collection, elements, multiple=True):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)

client = MongoClient('localhost', 27017)

# Connect to our database
db = client['admin']
series_collection = db['parsing_news']

client = MongoClient('localhost', 27017)

# Connect to our database
db = client['admin']
r = requests.get("https://vpravda.ru/articles/")

filteredNews = []
filterTimes = []
allNews = []
allhref = []
filterHref = []
alltimes = []
allNewsText = []
allNewsText2 = []
NewsText = []

AllHref = []
AllNews = []

inp = input("Введите 1 для парсинга и 2 для просмотра базы данных ")
if inp == str(1):
    for i in range(10):
        print(i)
        if i != 0:
            r = requests.get("https://vpravda.ru/articles/?page=" + str(i))

        soup = BS(r.text, "html.parser")
        allNews = soup.findAll('span', class_='field-content')
        AllNews = allNews
        alltimes = soup.findAll('div', class_='views-field views-field-field-article-date')
        allhref = soup.findAll('a', class_='field-content')
        for link in allNews:
            link = link.find('a').get('href')
            AllHref.append(link)
            filterHref.append(link)
        for l in filterHref:

            a = requests.get("https://vpravda.ru" + l)
            soup = BS(a.text, "html.parser")
            allNewsText.append(soup.findAll('div', class_='field-items')[2])
            allNewsText2.append(soup.findAll('div', class_='field-items')[3])
        for t, t1 in zip(allNewsText, allNewsText2):
            NewsText.append(t.text + "\n" + t1.text)
        for data in allNews:

            filteredNews.append(data.text)
        for d in alltimes:
            filterTimes.append(d.text)

        allNews.clear()
        filterHref.clear()
        print('Закончил обработку ' + str(i+1) + "-й страницы.")

    for d1, d2, d3, d4 in zip(filteredNews, filterTimes, AllHref, NewsText):
        new_show = {
            "NameNews": d1,
            "TimeDate": d2,
            "Href": d3,
            "NewsText": d4
        }
        insert_document(series_collection, new_show)
        print("Добавляю в базу данных")
else:
    if inp == str(2):
        result = find_document(series_collection, {})
        for i in result:
            print(i)
            print('\n')
            print('--------------------')

