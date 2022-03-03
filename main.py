import models
# import ptt_crawler
import pandas as pd
import sqlite3
from re import template
from urllib import request
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import Movie
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)

app = FastAPI() # 建立一個 Fast API application

templates = Jinja2Templates(directory="templates")

class MovieRequest(BaseModel):
    title: str

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/") # 指定 api 路徑 (get方法)
def home(request: Request, date = "", title = "", author = "", comment = "", limit: int = 50, page_num: int = 1, db: Session = Depends(get_db)):
    """
    display the movie creener dashboard / homepage
    """
    conn = sqlite3.connect('movies.db')  #建立資料庫
    cursor = conn.cursor()
    data_length = len(pd.read_sql("SELECT * FROM movies", conn))

    # date_length = ptt_crawler.data_length
    movies= db.query(Movie)
    # if title != "":
    #     movies = movies.filter(title in Movie.title)

    if author != "":
        movies = movies.filter(Movie.author == author)
    
    if comment != "":
        movies = movies.filter(Movie.comment > comment)

    skip = (page_num - 1) * limit
    data_length = movies.offset(skip).count()
    print(data_length)
    movies = movies.offset(skip).limit(limit)

    response = {
        "request": request, 
        "movies": movies, 
        "page_num": page_num,
        "pagination":{}
    }

    start = (page_num - 1) * limit
    end = start + limit
    if end >= data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"?page_num={page_num+1}&author={author}&date={date}&comment={comment}"
    
    # if ma200:
    #     movie = movie.filter(Movie.price > Movie.ma200)
    
    # movies = movies.all()

    return templates.TemplateResponse("home.html", response)

# def fetch_movie_data(id: int):
#     db = SessionLocal()
    
#     df = pd.DataFrame(ptt_crawler.all_post)
#     conn = sqlite3.connect('movie.db')  #建立資料庫
#     cursor = conn.cursor()
#     conn.commit()

#     #如果資料表存在，就寫入資料，否則建立資料表
#     df.to_sql('movie', conn, if_exists='replace', index=False) 
#     # db.commit()

@app.post("/movie")  # post get
def create_movie(movie_request: MovieRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    create movie data and store it in the database
    """
    movie = Movie()
    movie.title = movie_request.title

    db.add(movie)
    db.commit()

    # background_tasks.add_task(fetch_movie_data, movie.id)

    return{
        "code":"success",
        "message": "movie created"
    }

@app.get("/statistics")  # post get
def statistics(request: Request, db: Session = Depends(get_db)):


    return{
        "code":"success",
        "message": "movie created"
    }
