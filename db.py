import sqlite3

sqlite_connection = sqlite3.connect('db.db')
cursor = sqlite_connection.cursor()

def create_all():
    sqlite_select_query = """CREATE TABLE IF NOT EXISTS projects(id SEREAL, autor_usernames TEXT, name TEXT, descrip TEXT, dir_with_pic TEXT, video_link TEXT, topic TEXT, teamlead TEXT);
CREATE TABLE IF NOT EXISTS users(id SEREAL, username TEXT UNIQUE, name TEXT, surname TEXT);"""
    cursor.execute(sqlite_select_query)
    return

def get_all_projects():
    sqlite_select_query = """SELECT title, teamlead, topic FROM projects"""
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()

