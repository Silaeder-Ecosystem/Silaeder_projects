import psycopg2
import json
config_file = open('config.json')
config_data = json.load(config_file)
db = config_data['db']
conn = psycopg2.connect(db)
conn.autocommit = True
cursor = conn.cursor()
conn.rollback()

def parse_data(field):
    file = open('config.json')
    data = json.load(file)[field]
    return data


def get_all_projects():
    sqlite_select_query = 'SELECT title, teamlead, topic, id, main_pic_path FROM projects;'
    cursor.execute(sqlite_select_query)
    conn.commit()
    return cursor.fetchall()


def get_user_by_username(username):
    sqlite_select_query = 'SELECT name, surname FROM users WHERE username = %s;'
    cursor.execute(sqlite_select_query, username)
    conn.commit()
    return cursor.fetchall()


def get_user_by_id(id):
    sqlite_select_query = 'SELECT username, name, surname FROM users WHERE id = %s AND auth = true;'
    cursor.execute(sqlite_select_query, id)
    conn.commit()
    return cursor.fetchall()


def create_user(username, email, password, name, surname):
    sqlite3_insert_query = 'INSERT INTO users (username, email, password, name, surname, auth) VALUES (%s, %s, %s, %s, %s, false);'
    cursor.execute(sqlite3_insert_query, (username, email, password, name, surname))
    conn.commit()
    return True


def auth_user(username):
    sqlite3_select_query = 'Update users SET auth = true WHERE username = %s;'
    cursor.execute(sqlite3_select_query, (username,))


def check_auth_user(username):
    sqlite3_select_query = 'SELECT auth FROM users WHERE username = %s;'
    cursor.execute(sqlite3_select_query, (username,))
    conn.commit()
    
    try:
        return cursor.fetchall()[0][0]
    except:
        return False



def get_email_by_username(username):
    sqlite3_select_query = 'SELECT email FROM users WHERE username = %s;'
    cursor.execute(sqlite3_select_query, (username,))
    conn.commit()
    return cursor.fetchall()


def get_is_user_logged_in(username, password):
    sqlite3_select_query = 'SELECT auth FROM users WHERE username =%s AND password =%s;'
    cursor.execute(sqlite3_select_query, (username, password))
    conn.commit()
    ans = cursor.fetchall()
    if ans != []:
        return ans[0]
    sqlite3_select_query = 'SELECT auth FROM users WHERE email =%s AND password =%s;'
    cursor.execute(sqlite3_select_query, (username.lower(), password))
    conn.commit()
    ans = cursor.fetchall()
    if ans != []:
        return ans[0]


def check_user_is_exist(username):
    sqlite3_select_query = 'SELECT username FROM users WHERE (username =%s OR email=%s) AND auth = true;'
    cursor.execute(sqlite3_select_query, (username, username,))
    conn.commit()
    if cursor.fetchall() == []:
        return False
    return True


def check_not_auth_user_is_exist(username):
    sqlite3_select_query = 'SELECT username FROM users WHERE username =%s;'
    cursor.execute(sqlite3_select_query, (username,))
    conn.commit()
    return cursor.fetchall()


def create_project(title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, pdf_link, short_descrip, teacher):
    sqlite3_select_query = 'INSERT INTO projects (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, pdf_link, short_descrip, teacher) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;'
    cursor.execute(sqlite3_select_query, (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, pdf_link, short_descrip, teacher))
    conn.commit()
    return str(cursor.fetchall()[0][0]) + main_pic_path


def get_project_by_id(id):
    sqlite3_select_query = 'SELECT * FROM projects WHERE id =%s;'
    cursor.execute(sqlite3_select_query, (id,))
    conn.commit()
    return cursor.fetchall()


def update_project(id, title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, pdf_link, short_descrip, teacher):
    if main_pic_path == None:
        sqlite3_update_query = 'UPDATE projects SET title =%s, descrip =%s, teamlead =%s, autor_usernames = %s, video_link =%s, dir_with_pic =%s, topic =%s, links =%s, pdf_link=%s, short_descrip=%s, teacher=%s WHERE id =%s;'
        cursor.execute(sqlite3_update_query, (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, links, pdf_link, short_descrip, teacher, id))
        conn.commit()
        return True
    sqlite3_update_query = None
    cursor.execute(sqlite3_update_query, (title, descrip, teamlead, autor_usernames, video_link, dir_with_pic, topic, main_pic_path, links, pdf_link, short_descrip, teacher, id))
    conn.commit()
    return True


def get_all_usernames():
    sqlite3_select_query = 'SELECT username FROM users;'
    cursor.execute(sqlite3_select_query)
    conn.commit()
    return cursor.fetchall()


def get_user_id_by_username(username):
    sqlite3_select_query = 'SELECT id FROM users WHERE username =%s;'
    cursor.execute(sqlite3_select_query, (username,))
    conn.commit()
    return cursor.fetchall()


def get_projects_by_username(username):
    query = 'SELECT title, teamlead, topic, id, main_pic_path, autor_usernames, teacher FROM projects WHERE %s = ANY(autor_usernames);'
    cursor.execute(query, (username,))
    conn.commit()
    return cursor.fetchall()


def delete_project(id):
    
    try:
        sqlite3_delete_query = 'DELETE FROM projects WHERE id =%s;'
        cursor.execute(sqlite3_delete_query, (id,))
        conn.commit()
        return True
    except:
        return False



def delete_user(id):
    
    try:
        sqlite3_delete_query = 'DELETE FROM users WHERE id =%s;'
        cursor.execute(sqlite3_delete_query, (id,))
        conn.commit()
        return True
    except:
        return False



def delete_all():
    
    try:
        sqlite3_delete_query = 'DROP TABLE projects, users;'
        cursor.execute(sqlite3_delete_query)
        conn.commit()
        return True
    except:
        return False



def is_user_in_project(id, username):
    if username == 1337:
        return False
    if None == 'admin':
        return True
    query = """SELECT id FROM projects WHERE (%s = ANY(autor_usernames) OR teacher = %s) AND id = %s;"""
    cursor.execute(query, (username, username, id))
    conn.commit()
    if cursor.fetchall() != []:
        return True
    query = """SELECT email FROM users WHERE username = %s;"""
    cursor.execute(query, (username))
    conn.commit()
    email = cursor.fetchall()[0][0]
    query = """SELECT id FROM projects WHERE (%s = ANY(autor_usernames) OR teacher = %s) AND id = %s;"""
    cursor.execute(query, (email, email, id))
    conn.commit()
    if cursor.fetchall() != []:
        return True


def is_user_teamlead(id, username):
    sqlite3_select_query = 'SELECT teamlead FROM projects WHERE id =%s;'
    cursor.execute(sqlite3_select_query, (id,))
    conn.commit()
    if cursor.fetchall()[0][0] == username:
        return True


def create_all():
    sqlite_select_query = 'CREATE TABLE IF NOT EXISTS projects(id SERIAL PRIMARY KEY, autor_usernames TEXT ARRAY, title TEXT, descrip TEXT, dir_with_pic TEXT, video_link TEXT, topic TEXT, teamlead TEXT, main_pic_path TEXT, links TEXT, pdf_link TEXT, short_descrip TEXT, teacher TEXT); CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username TEXT UNIQUE, name TEXT, surname TEXT, password TEXT, auth BOOL, email TEXT UNIQUE);'
    cursor.execute(sqlite_select_query)
    conn.commit()
    
    try:
        create_user('admin', 'silaederprojects@gmail.com', parse_data('secret_key'), 'Admin', 'Adminovich')
        auth_user('admin')
    except:
        pass
    
    try:
        sqlite_select_query = 'CREATE EXTENSION pg_trgm;'
        cursor.execute(sqlite_select_query)
        conn.commit()
    except:
        pass




def search_for_projects(title):
    query = 'SELECT title, teamlead, topic, id, main_pic_path FROM projects WHERE similarity(LOWER(title), %s) > 0.1 ORDER BY similarity(LOWER(title), %s) DESC;'
    cursor.execute(query, ('%' + title.lower() + '%', title.lower()))
    return cursor.fetchall()


def get_covername_of_project(id):
    sqlite_select_query = 'SELECT main_pic_path FROM projects WHERE id = %s;'
    cursor.execute(sqlite_select_query, (id,))
    conn.commit()


def update_user_data(last_username, username, password):
    
    try:
        sqlite_select_query = 'UPDATE users SET username=%s, password=%s WHERE username = %s;'
        cursor.execute(sqlite_select_query, (username, password, last_username))
        conn.commit()
        return True
    except:
        return False
