from datetime import datetime
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
def home(request: Request , date = "", title = "", author = "", comment = "", limit: int = 50, page_num: int = 1, db: Session = Depends(get_db)):
    """
    display the movie creener dashboard / homepage
    """
    conn = sqlite3.connect('movies.db')  #建立資料庫
    cursor = conn.cursor()
    data_length = len(pd.read_sql("SELECT * FROM movies", conn))

    # date_length = ptt_crawler.data_length
    movies= db.query(Movie)
    if date != "":
        movies = movies.filter(Movie.date.like("{}%".format(date)))
    # if date != "":
    #     date_m, date_d = date.split("/")
    #     if len(date_m) == 1:
    #         date_m = " {}".format(date_m)
    #     if len(date_d) == 1:
    #         date_d = "0{}".format(date_d)
    #     date = date_m + "/" + date_d
    #     movies = movies.filter(Movie.date == date)
    if author != "":
        movies = movies.filter(Movie.author == author)
    
    if comment != "":
        movies = movies.filter(Movie.comment > comment)

    if title != "":
        movies = movies.filter(Movie.title.like("%{}%".format(title)))

    skip = (page_num - 1) * limit
    data_length = movies.offset(skip).count()
    movies = movies.offset(skip).limit(limit)

    response = {
        "request": request, 
        "movies": movies,  
        "limit": limit,
        "page_num": page_num,
        "pagination":{}
    }

    start = (page_num - 1) * limit
    end = start + limit
    if end >= data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}&limit={limit}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"?page_num={page_num-1}&author={author}&date={date}&comment={comment}&limit={limit}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"?page_num={page_num+1}&author={author}&date={date}&comment={comment}&limit={limit}"

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

@app.get("/statistics")  # post get
def statistics(request: Request, db: Session = Depends(get_db)):

    conn = sqlite3.connect('movies.db')  #建立資料庫
    cursor = conn.cursor()
    data_length = len(pd.read_sql("SELECT * FROM movies", conn))
    author_num = len(pd.read_sql("SELECT DISTINCT author FROM movies", conn))
    good_num = len(pd.read_sql("SELECT title FROM movies WHERE title LIKE '[好雷]%'", conn))
    bad_num = len(pd.read_sql("SELECT title FROM movies WHERE title LIKE '[負雷]%'", conn))

    response = {
        "request": request,
        "data_length": data_length,
        "author_num": author_num,
        "good_num": good_num,
        "bad_num": bad_num,
    }

    return templates.TemplateResponse("statistics.html", response)

app.mount("/static", StaticFiles(directory="./static"), name="static")