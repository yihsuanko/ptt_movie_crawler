from datetime import datetime
import models
# import ptt_crawler
import pandas as pd
import sqlite3
import re
from urllib import request
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from pydantic import BaseModel
from models import Movie
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.staticfiles import StaticFiles
from sqlalchemy import desc
from batman import find_type

DB_PATH = "movies_with_type" + '.db'

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # 建立一個 Fast API application

templates = Jinja2Templates(directory="templates")


class MovieRequest(BaseModel):
    title: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")  # 指定 api 路徑 (get方法)
def home(request: Request, good_com="", bad_com="", date="", title="", author="", comment="", limit: int = 50, page_num: int = 1, db: Session = Depends(get_db)):
    """
    display the movie creener dashboard / homepage
    """
    conn = sqlite3.connect(DB_PATH)  # 建立資料庫
    cursor = conn.cursor()
    data_length = len(pd.read_sql("SELECT * FROM movies", conn))

    movies = db.query(Movie)
    if date != "":
        movies = movies.filter(Movie.date.like("{}%".format(date)))
    if author != "":
        movies = movies.filter(Movie.author == author)

    if comment != "":
        movies = movies.filter(Movie.comment > comment)

    if title != "":
        movies = movies.filter(Movie.title.like("%{}%".format(title)))

    if good_com:
        movies = movies.filter(Movie.movie_type == "好雷")

    if bad_com:
        movies = movies.filter(Movie.movie_type == "負雷")


    skip = (page_num - 1) * limit
    data_length = movies.offset(skip).count()
    movies = movies.order_by(desc("date")).offset(skip).limit(limit)

    response = {
        "request": request,
        "movies": movies,
        "limit": limit,
        "author": author,
        "comment": comment,
        "title": title,
        "date": date,
        "good_com": good_com,
        "bad_com": bad_com,
        "page_num": page_num,
        "pagination": {}
    }

    start = (page_num - 1) * limit
    end = start + limit
    if end >= data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}&limit={limit}&good_com={good_com}&bad_com={bad_com}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}&limit={limit}&good_com={good_com}&bad_com={bad_com}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"?page_num={page_num+1}&author={author}&date={date}&comment={comment}&limit={limit}&good_com={good_com}&bad_com={bad_com}"

    return templates.TemplateResponse("home.html", response)

# @app.post("/movie")
# def create_movie(movie_request: MovieRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     """
#     create movie data and store it in the database
#     """
#     movie = Movie()
#     movie.title = movie_request.title

#     db.add(movie)
#     db.commit()

#     # background_tasks.add_task(fetch_movie_data, movie.id)

#     return{
#         "code":"success",
#         "message": "movie created"
#     }


@app.get("/statistics")
def statistics(request: Request):

    conn = sqlite3.connect(DB_PATH)  # 建立資料庫
    data = pd.read_sql("SELECT * FROM movies", conn)
    type_num = data["movie_type"].value_counts().to_dict()

    data_length = data["link"].count()
    author_num = len(pd.unique(data['author']))
    good_num = type_num["好雷"]
    bad_num = type_num["負雷"]

    response = {
        "request": request,
        "data_length": data_length,
        "author_num": author_num,
        "good_num": good_num,
        "bad_num": bad_num,
    }

    return templates.TemplateResponse("statistics.html", response)

@app.get("/batman")
  
def statistics(request: Request):

    conn = sqlite3.connect(DB_PATH)  # 建立資料庫
    data = pd.read_sql("SELECT * FROM movies", conn)
    data["bat_type"] = data["title"].apply(lambda v: find_type(v))

    data_length = data["bat_type"].value_counts()[True]
    good_num = data[data.movie_type == '好雷']["bat_type"].value_counts()[True]
    bad_num = data[data.movie_type == '負雷']["bat_type"].value_counts()[True]

    response = {
        "request": request,
        "data_length": data_length,
        "good_num": good_num,
        "bad_num": bad_num,
    }

    return templates.TemplateResponse("batman.html", response)

app.mount("/static", StaticFiles(directory="./static"), name="static")