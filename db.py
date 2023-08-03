import sqlite3

sqlite_connection = sqlite3.connect('db.db', check_same_thread=False)
#sqlite_connection.autocommit(True)
cursor = sqlite_connection.cursor()

def create_all():
    sqlite_select_query = ["""CREATE TABLE IF NOT EXISTS projects(id SEREAL, autor_usernames TEXT, title TEXT, descrip TEXT, dir_with_pic TEXT, video_link TEXT, topic TEXT, teamlead TEXT);""", 
"""CREATE TABLE IF NOT EXISTS users(id SEREAL, username TEXT UNIQUE, name TEXT, surname TEXT, password TEXT, auth BOOL, email TEXT UNIQUE);"""]
    cursor.execute(sqlite_select_query[0])
    cursor.execute(sqlite_select_query[1])
    sqlite_connection.commit()
    return

def get_all_projects():
    sqlite_select_query = """SELECT title, teamlead, topic FROM projects"""
    cursor.execute(sqlite_select_query)
    sqlite_connection.commit()
    return cursor.fetchall()

def get_project_by_id(id):
    sqlite_select_query = """SELECT title, teamlead, topic FROM projects WHERE id = %s"""
    cursor.execute(sqlite_select_query, id)
    sqlite_connection.commit()
    return cursor.fetchall()

def get_user_by_username(username):
    sqlite_select_query = """SELECT username, name, surname FROM users WHERE username = %s"""
    cursor.execute(sqlite_select_query, username)
    sqlite_connection.commit()
    return cursor.fetchall()

def get_user_by_id(id):
    sqlite_select_query = """SELECT username, name, surname FROM users WHERE id = %s AND auth = true"""
    cursor.execute(sqlite_select_query, id)
    sqlite_connection.commit()
    return cursor.fetchall()

def create_user(username, email, password, name, surname):
    try:
        sqlite3_insert_query = """INSERT INTO users (username, email, password, name, surname, auth) VALUES (?, ?, ?, ?, ?, false)"""
        cursor.execute(sqlite3_insert_query, (username, email, password, name, surname))
        sqlite_connection.commit()
        return True
    except:
        return False

def auth_user(username):
    sqlite3_select_query = """Update users SET auth = true WHERE username = ?"""
    cursor.execute(sqlite3_select_query, (username,))
    return cursor.fetchall()

def create_project(title, teamlead, topic, autor_usernames, descrip, dir_with_pic, video_link):
    #try:
        sqlite3_insert_query = """INSERT INTO projects (autor_usernames, title, descrip, dir_with_pic, video_link, topic, teamlead) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(sqlite3_insert_query, (autor_usernames, title, descrip, dir_with_pic, video_link, topic, teamlead))
        sqlite_connection.commit()
        return True
    #except:
     #   return False
        
def check_auth_user(username):
    sqlite3_select_query = """SELECT auth FROM users WHERE username = ?"""
    cursor.execute(sqlite3_select_query, (username,))
    sqlite_connection.commit()
    try:
        if cursor.fetchall()[0][0]:
            return True
        else:
            return False
    except:
        return True

def get_email_by_username(username):
    sqlite3_select_query = """SELECT email FROM users WHERE username = ?"""
    cursor.execute(sqlite3_select_query, (username,))
    sqlite_connection.commit()
    return cursor.fetchall()

def get_is_user_logged_in(username, password):
    sqlite3_select_query = """SELECT auth FROM users WHERE username =? AND password =?"""
    cursor.execute(sqlite3_select_query, (username, password))
    sqlite_connection.commit()
    if cursor.fetchall() != []:
        return True
    else:
        return False
    
def check_user_is_exist(username):
    sqlite3_select_query = """SELECT username FROM users WHERE username =?"""
    cursor.execute(sqlite3_select_query, (username,))
    sqlite_connection.commit()
    if cursor.fetchall() == []:
        return False
    else:
        return True