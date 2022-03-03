import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

payload = {
'from': '/bbs/movie/index.html',
'yes': 'yes'
}

pre = 'https://www.ptt.cc'

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url, timeout=(2, 3))
soup = BeautifulSoup(response.text, 'html.parser')
last2nd_url = soup.find_all(class_='btn')[3].get('href')
# print(last2nd_url)

lastpage = int(re.search('index(.+)\.html', last2nd_url).group(1)) + 1

all_post = []

for i in range(lastpage, lastpage-5, -1):
    
    url = 'https://www.ptt.cc/bbs/movie/index{}.html'.format(i)
    
    # response = requests.get(url, timeout=(2, 3))
    
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18',data=payload)  # 繞過18禁
    res = rs.get(url, timeout=(2, 3))
    soup = BeautifulSoup(res.text, "html.parser")
    for entry in soup.select('.r-ent'):
        title = entry.select('.title')[0].text
        author = entry.select('.author')[0].text
        date = entry.select('.date')[0].text
        try:
            link = pre + entry.find(class_='title').a['href']
            all_post.append({'author':author, 
                        'link':link,
                        'title':title.strip(), 
                        'date':date})
        except:
            # print("The link has been removed")
            pass

def crawler(url):
    payload = {
    'from': '/bbs/movie/index.html',
    'yes': 'yes'
    }

    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18',data=payload)  # 繞過18禁
    res = rs.get(url, timeout=(2, 3))
    soup = BeautifulSoup(res.text, 'html.parser')
    push = len(soup.select('.push'))

    return push

# all_post = pd.read_csv('all_post.csv')
df = pd.DataFrame(all_post)
comment=[]
for i in df["link"]:
    comment.append(crawler(i))

df['comment'] = comment

conn = sqlite3.connect('movies.db')  #建立資料庫
cursor = conn.cursor()
# cursor.execute('CREATE TABLE Billionaire(Name, NetWorth, Country, Source, Rank)')  #建立資料表
conn.commit()

#如果資料表存在，就寫入資料，否則建立資料表
df.to_sql('movies', conn, if_exists='replace', index=False) 
data_length = len(pd.read_sql("SELECT * FROM movie", conn))
# #透過SQL語法讀取資料庫中的資料
# # us_df = pd.read_sql("SELECT * FROM test_movie WHERE author='Gotham'", conn)
# # print(us_df)