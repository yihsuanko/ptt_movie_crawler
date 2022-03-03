import pandas as pd
import sqlite3
import ptt_crawler
 
df = pd.DataFrame(ptt_crawler.all_post)
 
conn = sqlite3.connect('test_movie.db')  #建立資料庫
cursor = conn.cursor()
# cursor.execute('CREATE TABLE Billionaire(Name, NetWorth, Country, Source, Rank)')  #建立資料表
conn.commit()

#如果資料表存在，就寫入資料，否則建立資料表
df.to_sql('test_movie', conn, if_exists='replace', index=False) 
 
#透過SQL語法讀取資料庫中的資料
us_df = pd.read_sql("SELECT * FROM test_movie WHERE author='Gotham'", conn)
print(us_df)