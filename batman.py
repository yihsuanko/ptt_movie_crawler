import sqlite3
import pandas as pd
import re
import os

DB_PATH = "movies_with_type" + '.db'


def find_type(title):

    regex_1 = re.compile(r'蝙蝠俠|黑暗騎士|Bat|羅伯派汀森', re.I)
    # regex_2 =  re.compile(r'黑暗騎士')

    if regex_1.search(title):
        type_bat = True
    # elif regex_2.search(title):
    # type_bat = True
    else:
        type_bat = False

    return type_bat


conn = sqlite3.connect(DB_PATH)
data = pd.read_sql("SELECT * FROM movies", conn)

data["bat_type"] = data["title"].apply(lambda v: find_type(v))
type_num = data["bat_type"].value_counts().to_dict()

# print(type_num)
# # filtered_data = data[data["bat_type"]==True]
# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# #     print(filtered_data)
# print(data.groupby(["bat_type", "movie_type"]).size())
