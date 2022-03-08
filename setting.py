from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
SQLite_DB_NAME = os.getenv("MYSQL_DB_NAME")
SQLite_DB_HOST = os.getenv("MYSQL_DB_HOST")
SQLite_PORY = os.getenv("MYSQL_PORY")
SQLite_USER = os.getenv("MYSQL_USER")
SQLite_PASSWORD = os.getenv("MYSQL_PASSWORD")
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
DATABASE_TABLE = os.getenv('DATABASE_TABLE')