import sqlite3
import pandas as pd
import re
import os

DB_PATH = "movies" + '.db'
SAVE_DB_PATH = "movies_with_type" + '.db'


def find_type(title):

    regex_g = re.compile(r'好.*雷')
    regex_b = re.compile(r'負.*雷')

    if regex_g.search(title):
        type_movie = "好雷"
    elif regex_b.search(title):
        type_movie = "負雷"
    else:
        type_movie = "其他"

    return type_movie


conn = sqlite3.connect(DB_PATH)
data = pd.read_sql("SELECT * FROM movies_0308", conn)

data["movie_type"] = data["title"].apply(lambda v: find_type(v))
type_num = data["movie_type"].value_counts().to_dict()

conn_save = sqlite3.connect(SAVE_DB_PATH)
conn_save.commit()
# 如果資料表存在，就寫入資料，否則建立資料表
data.to_sql("movies", conn_save, if_exists="replace", index=False)
