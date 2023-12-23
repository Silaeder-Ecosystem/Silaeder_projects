from flask import Flask, request, render_template, redirect, make_response, flash
import db as db
import jwt
import json
import parse
from flask_mail import Message, Mail
import re
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def parse_data(field):
    file = open("config.json")
    data = json.load(file)[field]

    return data

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'silaederprojects@gmail.com'  
app.config['MAIL_DEFAULT_SENDER'] = 'silaederprojects@gmail.com'  
app.config['MAIL_PASSWORD'] = parse_data("mail_password")
app.config['UPLOAD_FOLDER'] = './static/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

mail_sender = Mail(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=parse_data('mail')
    )
    mail_sender.send(msg)

def generate_confirmation_token(email):
    return jwt.encode(payload={"name": email}, key=parse_data("secret_key"))


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
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        login = request.form["email"]
        password = request.form["password"]

        if db.get_is_user_logged_in(login, password):
            token = jwt.encode(payload={"name": login}, key=parse_data("secret_key"))
            resp = make_response(redirect("/"))
            resp.set_cookie("jwt", token)
            return resp
        else:
            flash(['error', 'Wrong login or password'])
            return redirect("/login", code=302)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        form = request.form.to_dict()
        form['email'] = form['email'].lower()
        hasDigits, hasUpperCase, hasLowerCase, hasSpecialCharecters, hasSpases = False, False, False, False, True

        for i in form['password']:
            if (i.isdigit()):
                hasDigits = True
            elif (i.isupper()):
                hasUpperCase = True
            elif (i.islower()):
                hasLowerCase = True
            elif (i == ' '):
                flash(['error', 'Spaces are not allowed in'])
            else:
                hasSpecialCharecters = True 

        if not hasDigits:
            flash(['error', "Password must contain at least one digit"])
            return redirect('/register')
        
        if not hasUpperCase:
            flash(['error', "Password must contain at least one uppercase letter"])
            return redirect('/register')
        
        if not hasLowerCase:
            flash(['error', "Password must contain at least one lowercase letter"])
            return redirect('/register')
        
        if not hasSpecialCharecters:
            flash(['error', "Password must contain at least one special character"])
            return redirect('/register') 
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form["email"]):
            flash(['error','You write incorrect email'])
            return redirect("/register", code=302)
        app.logger.debug(parse.parse_csv())
        try:
            if parse.parse_csv().index(form["email"]) == -1:
                flash(['error','This is not silaeder email. Check it in Silaeder google sheet or ask administrator (@ilyastarcek)'])
                return redirect("/register", code=302)
        except:
            flash(['error','This is not silaeder email. Check it in Silaeder google sheet or ask administrator (@ilyastarcek)'])
            return redirect("/register", code=302)
        try:
            if db.create_user(form['username'], form["email"], form['password'], form['name'], form['surname']) == False:
                flash(['error','This username or email already exists'])
                return redirect("/register", code=302)
        except:
            flash(['error', 'This username or email already exists'])
            return redirect("/register", code=302)
        
        resp = make_response(redirect("/", code=302))
        flash(['success','A confirmation email has been sent via email'])
        

        etoken = generate_confirmation_token(form["username"])
        confirm_url = f'http://{parse_data("host")}/confirm/{etoken}'
        html = render_template('mail.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(form['email'], subject, html)

        return resp
        

@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    print(token)
    try:
        username = confirm_token(token)
        print(username)
    except:
        flash(['error','The confirmation link is invalid. Check your email'])
        return redirect('/', code=302)
    if db.check_not_auth_user_is_exist(username) == []:
        flash(['error','This is link for not registered account'])
        return redirect('/registration', code=302)
    token = jwt.encode(payload={"name": username}, key=parse_data("secret_key"))
    if db.check_auth_user(username):
        print(db.check_auth_user(username))
        flash(['error','Account already confirmed . Please login'])
        return redirect('/login', code=302)
    else:
        db.auth_user(username)
        flash(['success','You have confirmed your account. Thanks!'])
        resp = make_response(redirect("/", code=302))
        resp.set_cookie("jwt", token)
        return resp

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
            flash(['error', "You are not logged in"])
            return redirect('/login') 
    else:
        token = confirm_token(request.cookies.get("jwt"))
        if not token:
            flash(['error', "You are not logged in"])
            return redirect('/login') 
        form = request.form
        print()
        print()
        app.logger.debug(request.files)
        app.logger.debug(request.form)
        app.logger.debug(request.form.getlist('collaborators[]'))
        print()
        print()
        for i in ['title', 'description', 'teacher', 'topic', 'short-description', 'leader']:
            if form[i] == '':
                flash(['error', f"You don't fill {i} field"])
                return redirect("/projects/new", code=302)
        for i in request.form.getlist('collaborators[]'):
            print(i)
            if not db.check_user_is_exist(i):
                flash(['error', f"User {i} isn't finish registration or isn't exist. Please check him(her) username or ask him(her) finish registration"])
                return redirect("/projects/new", code=302)
        if 'cover' not in request.files:
            flash(['error','No file part'])
            return redirect(f"/projects/new")
        file = request.files['cover']
        if file.filename == '':
            flash(['error', 'No selected file'])
            return redirect(f"/projects/new")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id_name = filename.rsplit('.', 1)
            try:
            #if 1 == 1:
                if db.create_project(form['title'], form['description'], form['teacher'], form.getlist('team[]'), form['link-video'], form['link-image'], form["topic"],  str(db.count_of_projects()+1) + '.' + file_id_name[1], form['link-interes'], form['link-pdf']) == False:
                    flash(['error','This project already exists'])
                    return redirect("/projects/new", code=302)
            except:
                flash(['error', 'You fill not all fields'])
                return redirect("/projects/new", code=302)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(db.count_of_projects()) + '.' + file_id_name[1]))
            flash(['success','Project created'])
            return redirect("/myprojects", code=302)
        else:
            flash(['error','Uncorrect file or filename'])
            return redirect("/myprojects", code=302)

@app.route('/projects', methods=['GET'])
def get_projects():
    ans = db.get_all_projects()
    print(ans)
    return render_template("home.html", projects = ans, user = request.cookies.get("jwt"), title = "Silaeder Projects")

@app.route('/projects/<id>', methods=['GET'])
def get_project(id):
    ans = db.get_project_by_id(id)
    ans = list(ans[0])
    print(ans)
    token = confirm_token(request.cookies.get("jwt"))
    return render_template("view.html", ans = ans, user = token, id = id, asset = token in ans[1])

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    if (request.method == 'GET'):
        token = confirm_token(request.cookies.get("jwt"))
        if not token:
            flash(['error', "You are not logged in"])
            return redirect('/login') 
        ans = db.get_project_by_id(id)
        ans = list(ans[0])
        print(ans)
        return render_template("edit.html", ans = ans, user = token, id = id)
    else:
        token = confirm_token(request.cookies.get("jwt"))
        if not token:
            flash(['error', "You are not logged in"])
            return redirect('/login') 
        form = request.form
        print()
        print()
        app.logger.debug(request.files)
        app.logger.debug(request.form)
        app.logger.debug(request.form.getlist('collaborators[]'))
        print()
        print()
        for i in ['name', 'description', 'teacher', 'topic']:
            if form[i] == '':
                flash(['error',f"You don't fill {i} field"])
                return redirect("/projects/new", code=302)

        for i in request.form.getlist('collaborators[]'):
            print(i)
            if not db.check_user_is_exist(i):
                flash(['error',f"User {i} isn't finish registration or isn't exist. Please check him(her) username or ask him(her) finish registration"])
                return redirect(f'/projects/{id}/edit', code=302)

        if 'cover' not in request.files:
            flash(['error','No file part'])
            return redirect(f"/projects/{id}/edit")
        file = request.files['cover']
        if file.filename == '':
            db.update_project(id, form['name'], form['description'], form['teacher'], form.getlist('collaborators[]'), form['link-video'], form['link-image'], form["topic"],  str(id) + '.' + file_id_name[1], form['link-interes'], form['link-pdf'])
            flash(['success',"Project edited"])
            return redirect('/myprojects', code=200)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id_name = filename.rsplit('.', 1)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id) + '.' + file_id_name[1]))
            db.update_project(id, form['name'], form['description'], form['teacher'], form.getlist('collaborators[]'), form['link-video'], form['link-image'], form["topic"],  str(id) + '.' + file_id_name[1], form['link-interes'], form['link-pdf'])
            flash(['success',"Project edited"])
            return redirect('/myprojects', code=200)

@app.route('/myprojects', methods=['GET'])
def get_my_projects():
    token = confirm_token(request.cookies.get("jwt"))
    if not token:
        flash(['error', "You are not logged in"])
        return redirect('/login') 
    ans = db.get_projects_by_username(token)
    print(ans)
    return render_template("projects.html", projects = ans, user = request.cookies.get("jwt"), title = "Projects by " + token)

@app.route('/search/', methods=['GET', 'POST'])
def search_main():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        form = request.form
        return redirect(f'/search/{form["search"]}/')

@app.route('/search/<inp>/', methods=['GET'])
def search(inp):
    ans = db.search_for_projects(inp)
    return render_template("home.html", projects = ans, user = request.cookies.get("jwt"), inp = inp)

@app.route('/projects/<id>/delete')
def delete_project(id):
    if (db.delete_project(id)):
        for i in ALLOWED_EXTENSIONS:
            try:
                os.remove(f'/static/{id}.{i}')
            except:
                pass
        flash('Project deleted')
        return redirect('/projects', code=200)

@app.route('/user/<username>')
def user(username):
    return "Nothing here (in deploment)"
    ans = db.get_projects_by_username(username)
    ans2 = db.get_user_by_username(username)
    print(ans)
    return render_template("home.html", projects = ans, user = request.cookies.get("jwt"), title = "Projects by " + username, ans2 = ans2)

if __name__ == "__main__":
    db.delete_all()
    db.create_all()
    db.create_project("Silaeder Projects", "site_for_Silaeder_projects", "ilyastarcek", ['ilyastarcek', 'Nikita Turbo'], "нет", "нет", "IST", 'image/logo.jpg', 'projects.sileder.ru', 'нет', 'site_for_Silaeder_projects', 'Olga Starunova')
    app.run("0.0.0.0", port=11701, debug=True)
    print('create all')