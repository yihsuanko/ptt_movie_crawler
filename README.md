# ptt_movie_crawler

本專案將近三個月ptt電影版的標題、評論數爬下，並存入sqlite，透過fastapi來執行。

## 1. 安裝需要的package
```
pip3 install requests
pip3 install BeautifulSoup4
pip3 install pandas
pip3 install sqlalchemy
pip3 install fastapi
pip3 install uvicorn[standard]
pip3 install fastapi_pagination
```

## 2. 爬蟲 - ptt爬蟲範例
使用Chrome，按右鍵 -> 檢查，發現想要爬的標題的class＝"r-ent"。<br/>
按右上角x將檢查關閉，按上頁按鈕發現，url改變存在規律，均為index[數字].html，且每次遞減1。<br/>
因此，只要爬到最新一頁的數字，就能倒推回去。<br/>

實作範例
```python
payload = {"from": "/bbs/movie/index.html", "yes": "yes"}

pre = "https://www.ptt.cc"

url = "https://www.ptt.cc/bbs/movie/index.html"
response = requests.get(url, timeout=(2, 3))
soup = BeautifulSoup(response.text, "html.parser")
last2nd_url = soup.find_all(class_="btn")[3].get("href")
lastpage = int(re.search("index(.+)\.html", last2nd_url).group(1)) + 1  # 找到最後一頁的網址
```

使用類似的方法將其他資料爬下來。

## 3. 資料庫建立

使用免費的sqlite當作資料庫。

```python
df = pd.DataFrame(all_post)  # 將資料轉為DataFrame
conn = sqlite3.connect("movies.db")  # 建立資料庫
cursor = conn.cursor()
conn.commit()

# if_exists="append" -> 如果資料表存在，就寫入資料，否則建立資料表
df.to_sql("movies", conn, if_exists="append", index=False)
```

## 4. Fastapi 設定
基本設定

```python
from fastapi import FastAPI, Request, Depends, BackgroundTasks

app = FastAPI() # 建立一個 Fast API application

# 指定 api 路徑 (get方法)
@app.get("/")
def read_root():
    return {"Hello": "World"}

```

為了使用template，方便HTML建立
```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/statistics")  # post get
def statistics(request: Request, db: Session = Depends(get_db)):

    response = {
         "request": request,
        # 將要傳入HTML內容放在這裡
    }

    return templates.TemplateResponse("statistics.html", response)

```

## 5. HTML 美化
好用的 UI 網站 - Semantic UI : https://semantic-ui.com/ <br/>
layout.html 建立
```HTML
    <html>
    <head>
        <title>PTT 電影版爬蟲資料</title>
        <!--將Semantic UI 連結到HTML-->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
        <script src="https://code.jquery.com/jquery-3.1.1.min.js" integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>

    </head>
    <body>
        <div class="ui container">
            <br>
            <h2>
                <a style="color:black" href="/">PTT 電影版爬蟲資料</a>
            </h2>
            

            {% block content %}
            {% endblock %}
        </div>

    </body>
</html>
```

使用StaticFiles傳入照片、影片到HTML

```python
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="./static"), name="static")
```

## 6. 功能優化
1. 計算擴充好雷數
2. 蝙蝠俠好雷還是負雷比較多
