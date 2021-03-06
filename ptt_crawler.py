import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import logging
import datetime

def crawler(url):
        logger.debug("Started: {}".format(url))

        payload = {"from": "/bbs/movie/index.html", "yes": "yes"}
        rs = requests.session()
        res = rs.post("https://www.ptt.cc/ask/over18", data=payload)  # 繞過18禁
        res = rs.get(url, timeout=(2, 3))
        soup = BeautifulSoup(res.text, "html.parser")
        push = len(soup.select(".push"))
        if len(soup.select(".article-meta-value")) < 4:
            date = date_temp
        else:
            date = soup.select(".article-meta-value")[3].text
            date_container = date.split(" ")
            while '' in date_container:
                date_container.remove('')

            dts = date_container[4]  +"-"+ str(monthtonum[date_container[1]]) +"-"+ date_container[2] +" "+ date_container[3]
            date = datetime.datetime.strptime(dts,"%Y-%m-%d %H:%M:%S")
            logger.debug("date: {}".format(dts))

        logger.debug("Finished")

        return date, push

if __name__ == '__main__':
    
    # 設定logging
    logger = logging.getLogger()  # 設置root logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用FileHandler輸出到file
    fh = logging.FileHandler('log_movies5.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 使用StreamHandler輸出到console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # 使用兩個Handler
    logger.addHandler(ch)
    logger.addHandler(fh)

    # 開始爬蟲
    payload = {"from": "/bbs/movie/index.html", "yes": "yes"}

    pre = "https://www.ptt.cc"

    url = "https://www.ptt.cc/bbs/movie/index.html"
    response = requests.get(url, timeout=(2, 3))
    soup = BeautifulSoup(response.text, "html.parser")
    last2nd_url = soup.find_all(class_="btn")[3].get("href")
    # print(last2nd_url)

    lastpage = int(re.search("index(.+)\.html", last2nd_url).group(1)) + 1

    all_post = []

    for i in range(lastpage - 100, lastpage - 210, -1):  # 210
        logger.debug("Started: {}".format(i))

        url = "https://www.ptt.cc/bbs/movie/index{}.html".format(i)
        rs = requests.session()
        res = rs.post("https://www.ptt.cc/ask/over18", data=payload)  # 繞過18禁
        res = rs.get(url, timeout=(2, 3))
        soup = BeautifulSoup(res.text, "html.parser")

        
        for entry in soup.select(".r-ent"):
            title = entry.select(".title")[0].text
            author = entry.select(".author")[0].text
            # date = entry.select(".date")[0].text
            try:
                link = pre + entry.find(class_="title").a["href"]
                all_post.append(
                    {"author": author, "link": link, "title": title.strip()} #, "date": date}
                )
            except:
                # print("The link has been removed")
                pass

    logger.debug("Finished")

    monthtonum = {
        "Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12
    }


    # all_post = pd.read_csv('all_post.csv')
    df = pd.DataFrame(all_post)
    comment = []
    date = []
    for i in df["link"]:
        date_temp , comment_temp = crawler(i)
        date.append(date_temp)
        comment.append(comment_temp)

    df["date"] = date
    df["comment"] = comment

    conn = sqlite3.connect("movies.db")  # 建立資料庫
    cursor = conn.cursor()
    # cursor.execute('CREATE TABLE Billionaire(Name, NetWorth, Country, Source, Rank)')  #建立資料表
    conn.commit()

    # 如果資料表存在，就寫入資料，否則建立資料表
    df.to_sql("movies_0308", conn, if_exists="append", index=False)
    # data_length = len(pd.read_sql("SELECT * FROM movies", conn))
    # #透過SQL語法讀取資料庫中的資料
    # # us_df = pd.read_sql("SELECT * FROM test_movie WHERE author='Gotham'", conn)
    # # print(us_df)
