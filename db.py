# db.py
from flask import g
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        g.cursor = g.db.cursor()
    return g.db, g.cursor

def close_db(error):
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)
    if db is not None:
        db.close()
    if cursor is not None:
        cursor.close()
