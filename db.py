import sqlite3

sqlite_connection = sqlite3.connect('db.db', check_same_thread=False)
#sqlite_connection.autocommit(True)
cursor = sqlite_connection.cursor()

def create_all():
    sqlite_select_query = ["""CREATE TABLE IF NOT EXISTS projects(id SEREAL, autor_usernames TEXT ARRAY, title TEXT, descrip TEXT, dir_with_pic TEXT, video_link TEXT, topic TEXT, teamlead TEXT, main_pic_path TEXT, links TEXT);""", 
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
    
def create_project(title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links):
    try:
        sqlite3_select_query = """INSERT INTO projects (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links) VALUES (?,?,?,?,?,?,?,?)"""
        cursor.execute(sqlite3_select_query, (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links))
        sqlite_connection.commit()
        return True
    except:
        return False
    
def get_project_by_id(id):
    sqlite3_select_query = """SELECT * FROM projects WHERE id =?"""
    cursor.execute(sqlite3_select_query, (id,))
    sqlite_connection.commit()
    return cursor.fetchall()

def update_project(id, title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links):
    try:
        sqlite3_update_query = """UPDATE projects SET title =?, descrip =?, teamlead =?, autor_usernames =?, video_link =?, dir_with_pic =?, topic =?, main_pic_path =?, links =? WHERE id =?"""
        cursor.execute(sqlite3_update_query, (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, id))
        sqlite_connection.commit()
        return True
    except:
        return False
    
def get_all_usernames():
    sqlite3_select_query = """SELECT username FROM users"""
    cursor.execute(sqlite3_select_query)
    sqlite_connection.commit()
    return cursor.fetchall()

def get_user_id_by_username(username):
    sqlite3_select_query = """SELECT id FROM users WHERE username =?"""
    cursor.execute(sqlite3_select_query, (username,))
    sqlite_connection.commit()
    return cursor.fetchall()

def get_projects_by_username(username):
    sqlite3_select_query = """SELECT * FROM projects WHERE array_contains(autor_usernames, ?) != NULL ORDER BY id"""
    cursor.execute(sqlite3_select_query, (username,))
    sqlite_connection.commit()
    return cursor.fetchall()

def delete_project(id):
    try:
        sqlite3_delete_query = """DELETE FROM projects WHERE id =?"""
        cursor.execute(sqlite3_delete_query, (id,))
        sqlite_connection.commit()
        return True
    except:
        return False
    
def delete_user(id):
    try:
        sqlite3_delete_query = """DELETE FROM users WHERE id =?"""
        cursor.execute(sqlite3_delete_query, (id,))
        sqlite_connection.commit()
        return True
    except:
        return False
    
def delete_all():
    try:
        sqlite3_delete_query = """DELETE FROM projects"""
        cursor.execute(sqlite3_delete_query)
        sqlite_connection.commit()
        sqlite3_delete_query = """DELETE FROM users"""
        cursor.execute(sqlite3_delete_query)
        sqlite_connection.commit()
        return True
    except:
        return False
    
