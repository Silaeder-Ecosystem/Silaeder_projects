# ЭТО ВЕРСИЯ С AUTH0  

from flask import Flask, request, render_template, redirect, make_response, flash, abort, url_for
import db as db
import jwt
import json
#import parse 
from flask_mail import Message, Mail
#import re
from werkzeug.utils import secure_filename
import os
#import hashlib
from authlib.integrations.flask_client import OAuth
import authlib
import auth0

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def parse_data(field):
    file = open("config.json")
    data = json.load(file)[field]

    return data

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = parse_data('mail')
app.config['MAIL_DEFAULT_SENDER'] = parse_data('mail')
app.config['MAIL_PASSWORD'] = parse_data("mail_password")
app.config['UPLOAD_FOLDER'] = './static/'

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

mail_sender = Mail(app)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=parse_data("AUTH0_CLIENT_ID"),
    client_secret=parse_data("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{parse_data("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_press(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "pdf"

'''def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=parse_data('mail')
    )
    mail_sender.send(msg)'''

#def generate_confirmation_token(email):
#    return jwt.encode(payload={"name": email}, key=parse_data("secret_key"))


def confirm_token(token):
    try:
        return jwt.decode(token, key=parse_data("secret_key"), algorithms="HS256")["name"]
    except:
    	return False


def check_jwt(token, username):
    try:
        payload = jwt.decode(token, key=parse_data("secret_key"), algorithms="HS256")
    except:
        return False
        
    if payload["name"] == username:
        return True
    else:
        return False

@app.route('/', methods=['GET'])
def main():
    if not check_jwt(request.cookies.get("jwt"), "admin"):
        return redirect('/projects')
    return "HELLO"

@app.route("/login", methods=["GET", "POST"])
def login():
    '''if request.method == "GET":
        return render_template("login.html")
    
    else:
        login = request.form["email"]
        password = request.form["password"]

        if db.get_is_user_logged_in(login, hashlib.sha256(password.encode('utf-8')).hexdigest()) and db.check_auth_user(login):
            token = jwt.encode(payload={"name": login}, key=parse_data("secret_key"))
            resp = make_response(redirect("/"))
            resp.set_cookie("jwt", token)
            flash(['success', 'Вы успешно вошли'])
            return resp
        else:
            if not db.check_auth_user(login):
                flash(['error', 'Ваш аккаунт не подтвержден. Пожалуйста, проверьте вашу почту'])
                return redirect("/login", code=302)
            else:
                flash(['error', 'Неправильный логин или пароль'])
                return redirect("/login", code=302)'''
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''if (request.method == "GET"):
        return render_template("register.html")
    else:
        form = request.form.to_dict()
        form['email'] = form['email'].lower()
        hasDigits, hasUpperCase, hasLowerCase, hasSpecialCharecters, hasSpases = False, False, False, False, True
        for i in form['username']:
            if i not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_':
                flash(['error', 'Никнейм содержит недопустимые символы'])
                return redirect('/register')

        for i in form['password']:
            if (i.isdigit()):
                hasDigits = True
            elif (i.isupper()):
                hasUpperCase = True
            elif (i.islower()):
                hasLowerCase = True
            elif (i == ' '):
                flash(['error', 'Пробелы не допускаются в пароле'])
            else:
                hasSpecialCharecters = True 

        if not hasDigits:
            flash(['error', "Пароль должен содержать хотя бы одну цифру"])
            return redirect('/register')
        
        if not hasUpperCase:
            flash(['error', "Пароль должен содержать хотя бы одну заглавную букву"])
            return redirect('/register')
        
        if not hasLowerCase:
            flash(['error', "Пароль должен содержать хотя бы одну строчную букву"])
            return redirect('/register')
        
        if not hasSpecialCharecters:
            flash(['error', "Пароль должен содержать хотя бы один специальный символ"])
            return redirect('/register') 
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form["email"]):
            flash(['error','Вы ввели неправильную почту'])
            return redirect("/register", code=302)
        app.logger.debug(parse.parse_csv())
        try:
            if parse.parse_csv().index(form["email"]) == -1:
                flash(['error','Это не почта не из Силаэдра. Проверьте его в таблице Силаэдра или спросите администратора (@ilyastarcek)'])
                return redirect("/register", code=302)
        except:
            flash(['error','Это не silaeder email. Проверьте его в таблице Силаэдра или спросите администратора (@ilyastarcek)'])
            return redirect("/register", code=302)
        try:
            if db.create_user(form['username'], form["email"], hashlib.sha256(form['password'].encode('utf-8')).hexdigest(), form['name'], form['surname']) == False:
                flash(['error','Этот никнейм или почта уже существует'])
                return redirect("/register", code=302)
        except:
            flash(['error', 'Этот никнейм или почта уже существует'])
            return redirect("/register", code=302)
        
        resp = make_response(redirect("/projects", code=302))
        flash(['success','Подтверждающее письмо было отправлено на ваш email'])
        

        etoken = generate_confirmation_token(form["username"])
        confirm_url = f'http://{parse_data("host")}/confirm/{etoken}'
        html = render_template('mail.html', confirm_url=confirm_url)
        subject = "Пожалуйста, подтвердите ваш email"
        send_email(form['email'], subject, html)

        return resp'''
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
        app.logger.debug(token)
    except authlib.integrations.base_client.errors.OAuthError as e:
        if "Please verify your email before continuing" in str(e):
            flash(['error', "Please verify your email before continuing"])
            return redirect('/')
        else:
            return str(e)
    app.logger.debug(token)
    token2 = jwt.encode(payload={"name": token['userinfo']['nickname']}, key=parse_data("secret_key"))
    resp = make_response(redirect("/projects"))
    flash(['success', 'Вы успешно вошли'])
    resp.set_cookie("jwt", token2)
    return resp

'''@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    print(token)
    try:
        username = confirm_token(token)
        print(username)
    except:
        flash(['error','Ссылка подтверждения недействительна. Проверьте вашу почту'])
        return redirect('/', code=302)
    if db.check_not_auth_user_is_exist(username) == []:
        flash(['error','Это ссылка для не зарегистрированного аккаунта'])
        return redirect('/registration', code=302)
    token = jwt.encode(payload={"name": username}, key=parse_data("secret_key"))
    if db.check_auth_user(username):
        print(db.check_auth_user(username))
        flash(['error','Аккаунт уже подтвержден. Пожалуйста, войдите'])
        return redirect('/login', code=302)
    else:
        db.auth_user(username)
        flash(['success','Вы подтвердили свой аккаунт. Спасибо!'])
        resp = make_response(redirect("/", code=302))
        resp.set_cookie("jwt", token)
        return resp'''

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect("/", code=302))
    resp.set_cookie("jwt", "")
    return resp

@app.route('/projects/new', methods=['GET', 'POST'])
def new_projects():
    if (request.method == "GET"):
        if (confirm_token(request.cookies.get("jwt")) != False):
            return render_template("create.html", user = confirm_token(request.cookies.get("jwt")))
        else:
            flash(['error', "Вы не вошли"])
            return redirect('/login') 
    else:
        token = confirm_token(request.cookies.get("jwt"))
        if not token:
            flash(['error', "Вы не вошли"])
            return redirect('/login') 
        form = request.form
        print()
        print()
        app.logger.debug(token)
        app.logger.debug(request.form)
        app.logger.debug(request.form.getlist('team[]'))
        print()
        print()
        translate = {'title': 'название', 'description': 'описание', 'teacher': 'учитель', 'topic': 'секция', 'short-description': 'краткое описание', 'leader': 'лидер'}
        for i in ['title', 'description', 'teacher', 'topic', 'short-description', 'leader']:
            if form[i] == '':
                flash(['error', f"Вы не заполнили поле {translate[i]}"])
                return redirect("/projects/new", code=302)
        if form.getlist('team[]') == []:
            flash(['error', 'Никого нет в проекте. Пожалуйста, добавьте людей в проект'])
            return redirect("/projects/new", code=302)
        if token not in form.getlist('team[]'):
            form.getlist('team[]').append(token)
        for i in request.form.getlist('team[]'):
            print(i)
            if not auth0.check_user_is_exist(i):
                flash(['error', f"Пользователь {i} не найден. Пожалуйста, проверьте его имя пользователя "])
                return redirect("/projects/new", code=302)
        if not auth0.check_user_is_exist(form['teacher']):
            flash(['error',f"Аккаунт учителя не найден. Пожалуйста, проверьте его имя пользователя"])
            return redirect(f'/projects/new', code=302)
        file = request.files['cover']
        file2 = request.files['presentation']
        if form['topic'] not in ['Математика', 'Информатика', 'Машинное обучение', 'Физика', 'Инфобез', 'Экономика', 'Биология', 'Экология', 'Медицина', 'Астрономия', 'Химия', 'Игры', 'Литература', 'История', 'Лингвистика', 'Филология', 'Обществознание', 'Английский', 'География', 'Макетирование']:
            flash(['error', 'Неправильная секция'])
            return redirect(f"/projects/new")
        if 'cover' not in request.files:
            flash(['error','Файл не загружен'])
            return redirect(f"/projects/new")
        if 'presentation' not in request.files:
            flash(['error','Презентация не загружена'])
            return redirect(f"/projects/new")
        if file.filename == '':
            flash(['error', 'Обложка не выбрана'])
            return redirect(f"/projects/new")
        if file2.filename == '':
            flash(['error', 'Презентация не выбрана'])
            return redirect(f"/projects/new")
        if not allowed_file(file.filename):
            flash(['error', 'Неправильный файл обложки'])
            return redirect(f"/projects/new")
        if not allowed_press(file2.filename):
            flash(['error', 'Неправильный файл презентации'])
            return redirect(f"/projects/new")
        filename = secure_filename(file.filename)
        filename2 = secure_filename(file2.filename)
        file_id_name = filename.rsplit('.', 1)
        file_id_name2 = filename2.rsplit('.', 1)
        #try:
        #if 1 == 1:
        proj = db.create_project(form['title'], form['description'], form['leader'], form.getlist('team[]'), form['link-video'], form['link-images'], form["topic"],  '.' + file_id_name[-1], form['link-interes'], '.' + file_id_name2[-1], form['short-description'], form['teacher'])
        if proj == False:
            flash(['error','Ошибка базы данных. Пожалуйста, свяжитесь с @ilyastarcek'])
            return redirect("/projects/new", code=302)
        #except:
            #   flash(['error', 'You fill not all fields'])
            #  return redirect("/projects/new", code=302)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], proj))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], proj.split('.')[0]+ '.pdf'))
        flash(['success','Проект создан'])
        return redirect("/myprojects", code=302)

@app.route('/projects', methods=['GET'])
def get_projects():
    ans = db.get_all_projects()
    print(ans)
    return render_template("home.html", projects = ans, user = request.cookies.get("jwt"), title = "Silaeder Projects")

@app.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    ans = db.get_project_by_id(id)
    if ans == []:
        abort(404)
    ans = list(ans[0])
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        token = 1337
    return render_template("view.html", ans = ans, user = confirm_token(request.cookies.get('jwt')), id = id, asset = db.is_user_in_project(id, token))

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', user=confirm_token(request.cookies.get('jwt')))

@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    if (request.method == 'GET'):
        token = confirm_token(request.cookies.get("jwt"))
        if not token :
            flash(['error', "Вы не вошли"])
            return redirect('/login') 
        if not db.is_user_in_project(id, token):
            flash(['error', "Вы не состоите в этом проекте"])
            return redirect('/projects/'+str(id)) 
        ans = db.get_project_by_id(id)
        ans = list(ans[0])
        print(ans)
        return render_template("edit.html", ans = ans, user = token, id = id)
    else:
        token = confirm_token(request.cookies.get("jwt"))
        if not token:
            flash(['error', "Вы не вошли"])
            return redirect('/login') 
        if not db.is_user_in_project(id, token):
            flash(['error', "Вы не состоите в этом проекте"])
            return redirect('/projects/'+str(id)) 
        form = request.form
        print()
        print()
        app.logger.debug(request.files)
        app.logger.debug(request.form)
        print()
        print()
        translate = {'title': 'название', 'description': 'описание', 'teacher': 'учитель', 'topic': 'секция', 'short-description': 'краткое описание', 'leader': 'лидер'}
        for i in ['title', 'description', 'teacher', 'topic', 'short-description', 'leader']:
            if form[i] == '':
                flash(['error',f"Вы не заполнили поле {translate[i]}"])
                return redirect("/projects/new", code=302)

        if request.form.getlist('team[]') == []:
            flash(['error', 'Никого нет в проекте. Пожалуйста, добавьте людей в проект'])
            return redirect('/projects/'+str(id)+'/edit')
        if token not in form.getlist('team[]'):
            form.getlist('team[]').append(token)
        if form['topic'] not in ['Математика', 'Информатика', 'Машинное обучение', 'Физика', 'Инфобез', 'Экономика', 'Биология', 'Экология', 'Медицина', 'Астрономия', 'Химия', 'Игры', 'Литература', 'История', 'Лингвистика', 'Филология', 'Обществознание', 'Английский', 'География', 'Макетирование']:
            flash(['error', 'Неправильная секция'])
            return redirect(f"/projects/{id}/edit")
        for i in request.form.getlist('team[]'):
            print(i)
            if not auth0.check_user_is_exist(i):
                flash(['error',f"Пользователь {i} не найден. Пожалуйста, проверьте его имя пользователя"])
                return redirect(f'/projects/{id}/edit', code=302)
        if not auth0.check_user_is_exist(form['teacher']):
            flash(['error',f"Аккаунт учителя не найден. Пожалуйста, проверьте его имя пользователя"])
            return redirect(f'/projects/{id}/edit', code=302)
        if 'cover' not in request.files:
            flash(['error','Файл не загружен'])
            return redirect(f"/projects/{id}/edit")
        if 'presentation' not in request.files:
            flash(['error','Презентация не загружена'])
            return redirect(f"/projects/{id}/edit")
        file = request.files['cover']
        file2 = request.files['presentation']
        if file.filename != '' and not allowed_file(file.filename):
            flash(['error', 'Неправильный файл обложки'])
            return redirect(f"/projects/{id}/edit")
        if file2.filename != '' and not allowed_press(file2.filename):
            flash(['error', 'Неправильный файл презентации'])
            return redirect(f"/projects/{id}/edit")
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_id_name = filename.rsplit('.', 1)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id) + '.' + file_id_name[-1]))
        else:
            filename = db.get_covername_of_project(id)
        if file2.filename != '':
            filename2 = '.'+secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id) + '.pdf'))
        else:
            filename2 = db.get_presentation_of_project(id)
        db.update_project(id, form['title'], form['description'], form['leader'], form.getlist('team[]'), form['link-video'], form['link-images'], form["topic"], filename, form['link-interes'], filename2, form['short-description'], form['teacher'])
        flash(['success',"Проект отредактирован"])
        return redirect('/myprojects')

@app.route('/myprojects', methods=['GET'])
def get_my_projects():
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        flash(['error', "Вы не вошли"])
        return redirect('/login') 
    ans = db.get_projects_by_username(token)
    print(ans)
    return render_template("projects.html", projects = ans, user = request.cookies.get("jwt"), title = "Проекты от " + token)

@app.route('/search/', methods=['GET', 'POST'])
def search_main():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        form = request.form
        app.logger.debug(form)
        if form['topic'] not in ['Математика', 'Информатика', 'Машинное обучение', 'Физика', 'Инфобез', 'Экономика', 'Биология', 'Экология', 'Медицина', 'Астрономия', 'Химия', 'Обществознание', 'Английский', 'География', 'Макетирование', 'Лингвистика', 'Филология', 'История', 'Литература', 'Игры', '']:
            flash(['error', 'Неправильная секция'])
            return redirect('/projects')
        return render_template('home.html', projects = db.search_for_projects(form['search'], form['topic']), user = request.cookies.get("jwt"), title = "Поиск проектов", query = form['search'], topic = form['topic'], search = True)
       
@app.route('/projects/<int:id>/delete')
def delete_project(id):
    if (db.delete_project(id)):
        for i in ALLOWED_EXTENSIONS:
            try:
                os.remove(f'/static/{id}.{i}')
            except:
                pass
        flash('Project deleted')
        return redirect('/projects')

@app.route('/user/<username>')
def user(username):
    return "Здесь ничего нет (в разработке)"
    ans = db.get_projects_by_username(username)
    ans2 = db.get_user_by_username(username)
    print(ans)
    return render_template("home.html", projects = ans, user = request.cookies.get("jwt"), title = "Projects by " + username, ans2 = ans2)

@app.route('/settings', methods=['GET'])
def settings():
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        flash(['error', "Вы не вошли"])
        return redirect('/login') 
    return render_template('settings.html')

@app.route('/change-username', methods=['GET', 'POST'])
def change_username():
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        flash(['error', "Вы не вошли"])
        return redirect('/login') 
    if request.method == 'GET':
        return render_template('change_username.html')
    else:
        form = request.form
        if form['username'] == '':
            flash(['error', 'Имя пользователя не заполнено'])
            return redirect('/settings')
        if auth0.check_user_is_exist(form['username']):
            flash(['error', 'Имя пользователя уже занято'])
            return redirect('/settings')
        auth0.change_username(token, form['username'])
        flash('Имя пользователя успешно обновлено')
        return redirect('/settings')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        flash(['error', "Вы не вошли"])
        return redirect('/login') 
    if request.method == 'GET':
        return render_template('change_password.html')
    else:
        form = request.form
        if form['password'] == '':
            flash(['error', 'Пароль не заполнен'])
            return redirect('/settings')
        if form['password2'] == '':
            flash(['error', 'Второй пароль не заполнен'])
            return redirect('/settings')
        hasDigits, hasUpperCase, hasLowerCase, hasSpecialCharecters, hasSpases = False, False, False, False, True

        for i in form['password']:
            if (i.isdigit()):
                hasDigits = True
            elif (i.isupper()):
                hasUpperCase = True
            elif (i.islower()):
                hasLowerCase = True
            elif (i == ' '):
                hasSpases = True
            else:
                hasSpecialCharecters = True 

        if not hasDigits:
            flash(['error', "Пароль должен содержать хотя бы одну цифру"])
        
        if not hasUpperCase:
            flash(['error', "Пароль должен содержать хотя бы одну заглавную букву"])
        
        if not hasLowerCase:
            flash(['error', "Пароль должен содержать хотя бы одну строчную букву"])
        
        if not hasSpecialCharecters:
            flash(['error', "Пароль должен содержать хотя бы один специальный символ"])

        if hasSpases:
            flash(['error', "Пароль не должен содержать пробелов"])

        if form['password'] != form['password2']:
            flash(['error', "Пароли должны совпадать"])
        
        if hasSpases or not hasDigits or not hasUpperCase or not hasLowerCase or not hasSpecialCharecters or form['password'] != form['password2']:
            return redirect('/change-password') 
        
        #if not db.update_user_data(token, form['name'], form['password']):
        #    return 'ОШИБКА: смена пароля'
        auth0.update_user_password(token['name'], form['password'])
        flash('Пароль успешно обновлен')
        return redirect('/projects')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=confirm_token(request.cookies.get('jwt'))), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', user=confirm_token(request.cookies.get('jwt'))), 500

if __name__ == "__main__":
    #db.delete_all()
    db.create_all()
    #db.create_project("Silaeder Projects", "site_for_Silaeder_projects", "ilyastarcek", ['ilyastarcek', 'Nikita Turbo'], "нет", "нет", "IST", 'image/logo.jpg', 'projects.sileder.ru', 'нет', 'site_for_Silaeder_projects', 'Olga Starunova')
    app.run("0.0.0.0", port=11701, debug=True)
    print('create all')
