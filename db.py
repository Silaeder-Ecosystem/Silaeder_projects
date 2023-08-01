import sqlite3

sqlite_connection = sqlite3.connect('db.sql', check_same_thread=False)
#sqlite_connection.autocommit(True)
cursor = sqlite_connection.cursor()

def create_all():
    sqlite_select_query = ["""CREATE TABLE IF NOT EXISTS projects(id SEREAL, autor_usernames TEXT, title TEXT, descrip TEXT, dir_with_pic TEXT, video_link TEXT, topic TEXT, teamlead TEXT);""", 
"""CREATE TABLE IF NOT EXISTS users(id SEREAL, username TEXT UNIQUE, name TEXT, surname TEXT, password TEXT, auth BOOL, email TEXT UNIQUE);"""]
    cursor.execute(sqlite_select_query[0])
    cursor.execute(sqlite_select_query[1])
    return

def get_all_projects():
    sqlite_select_query = """SELECT title, teamlead, topic FROM projects"""
    cursor.execute(sqlite_select_query)
    return cursor.fetchall()

def get_project_by_id(id):
    sqlite_select_query = """SELECT title, teamlead, topic FROM projects WHERE id = %s"""
    cursor.execute(sqlite_select_query, id)
    return cursor.fetchall()

def get_user_by_username(username):
    sqlite_select_query = """SELECT username, name, surname FROM users WHERE username = %s"""
    cursor.execute(sqlite_select_query, username)
    return cursor.fetchall()

def get_user_by_id(id):
    sqlite_select_query = """SELECT username, name, surname FROM users WHERE id = %s AND auth = true"""
    cursor.execute(sqlite_select_query, id)
    return cursor.fetchall()

def create_user(username, email, password, name, surname):
    try:
        sqlite3_insert_query = """INSERT INTO users (username, email, password, name, surname, auth) VALUES (%s, %s, %s, %s, %s, false)"""
        cursor.execute(sqlite3_insert_query, (username, email, password, name, surname))
        return True
    except:
        return False

def auth_user(username):
    sqlite3_select_query = """Update users SET auth = true WHERE username = %s"""
    cursor.execute(sqlite3_select_query, username)
    return cursor.fetchall()