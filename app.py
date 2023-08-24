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

db.create_all()

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'silaederprojects@gmail.com'  
app.config['MAIL_DEFAULT_SENDER'] = 'silaederprojects@gmail.com'  
app.config['MAIL_PASSWORD'] = 'waduszxztipcdeyd'  
app.config['UPLOAD_FOLDER'] = './static/uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

mail_sender = Mail(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if token == None:
        return False
    return jwt.decode(token, key=parse_data("secret_key"), algorithms="HS256")["name"]

def parse_data(field):
    file = open("config.json")
    data = json.load(file)[field]

    return data

def check_jwt(token, username):
    if token:
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
        login = request.form["login"]
        password = request.form["password"]

        if db.get_is_user_logged_in(login, password):
            token = jwt.encode(payload={"name": login}, key=parse_data("secret_key"))
            resp = make_response(redirect("/"))
            resp.set_cookie("jwt", token)
            return resp
        else:
            flash('Wrong login or password')
            return redirect("/login", code=302)


@app.route('/regestration', methods=['GET', 'POST'])
def register():
    if (request.method == "GET"):
        return render_template("reg.html")
    else:
        form = request.form

        hasDigits, hasUpperCase, hasLowerCase, hasSpecialCharecters, hasSpases = False, False, False, False, True

        for i in form["password"]:
            if (i.isdigit()):
                hasDigits = True
            elif (i.isupper()):
                hasUpperCase = True
            elif (i.islower()):
                hasLowerCase = True
            elif (i == ' '):
                hasSpases = False
            else:
                hasSpecialCharecters = True 

        if ( hasDigits and hasLowerCase and hasSpases and hasUpperCase and hasSpecialCharecters and form["password"] == form["password2"]):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", form["email"]):
                flash('You write incorrect email')
                return redirect("/regestration", code=302)
            try:
                if parse.parse_csv().index(form["email"]) == -1:
                    flash('This is not silaeder email. Check it in Silaeder google sheet or ask administrator (@ilyastarcek)')
                    return redirect("/regestration", code=302)
            except:
                flash('This is not silaeder email. Check it in Silaeder google sheet or ask administrator (@ilyastarcek)')
                return redirect("/regestration", code=302)
            if db.create_user(form['username'], form["email"], form['password'], form['name'], form['surname']) == False:
                flash('This username or email already exists')
                return redirect("/regestration", code=302)
            
            flash('A confirmation email has been sent via email')
            resp = make_response(redirect("/", code=200))
            

            etoken = generate_confirmation_token(form["username"])
            confirm_url = f'http://127.0.0.1:5678/confirm/{etoken}'
            html = render_template('mail.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form['email'], subject, html)

            return resp
        
        else:
            flash('You write incorrect password')
            return redirect("/regestration", code=302)

@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    print(token)
    #try:
    username = confirm_token(token)
    print(username)
    '''except:
        flash('The confirmation link is invalid or has expired. Check your email')
        return redirect('/', code=302)'''
    if not db.check_not_auth_user_is_exist(username):
        flash('This is link for not registered')
        return redirect('/regestration', code=302)
    token = jwt.encode(payload={"name": username}, key=parse_data("secret_key"))
    if db.check_auth_user(username):
        print(db.check_auth_user(username))
        flash('Account already confirmed . Please login')
        return redirect('/login', code=302)
    else:
        db.auth_user(username)
        flash('You have confirmed your account. Thanks!')
        resp = make_response(redirect("/projects", code=302))
        resp.set_cookie("jwt", token)
        return resp

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect("/projects", code=200))
    resp.set_cookie("jwt", "")
    return resp

@app.route('/myprojects/new', methods=['GET', 'POST'])
def new_projects():
    if (request.method == "GET"):
        if confirm_token(request.cookies.get("jwt")):
            flash('You are not logged in')
            return render_template("login.html")
        return render_template("new_project.html")
    else:
        form = request.form
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            for i in form['colaborators']:
                if not db.check_user_is_exist(i):
                    flash(f'User {i} is not registered or conformered account. Please ask him finish register or delete his account from this project')
                    return redirect('/myprojects', code=302)
            try:
                if db.create_project(form['title'], form['description'], form['teamlead'], form['colaborators'], form['video_url'], form['images_link'], form["topic"], filename, form['links']) == False:
                    flash('This project already exists')
                    return redirect("/myprojects/new", code=302)
            except:
                flash('You fill not all fields')
                return redirect("/myprojects/new", code=302)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Project created')
            return redirect("/myprojects", code=200)

@app.route('/projects', methods=['GET'])
def get_projects():
    if (db.create_project("Silaeder Projectssssssssssssssss", "ilyastarcek", "ICT", ['ilyastarcek', 'NICITATURBOBOY'], "site_for_Silaeder_projects", "https://silaeder.com", "github", 'icon.jpg', '') != True):
        print("aguzog")
    ans = db.get_all_projects()
    return render_template("index.html", ans = ans)

@app.route('/projects/<id>', methods=['GET'])
def get_project(id):
    ans = db.get_project_by_id(id)
    try:
        username = confirm_email(request.cookies.get('jwt'))
        user = db.is_user_in_project(id, username)
    except:
        user = False
    return render_template("project.html", ans = ans, user = user)

@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    if request.method == "GET":
        if confirm_token(request.cookies.get("jwt")):
            flash('You are not logged in')
            return render_template("login.html")
        ans = db.get_project_by_id(id)
        return render_template("edit_project.html", ans = ans)
    else:
        if confirm_token(request.cookies.get("jwt")):
            flash('You are not logged in')
            return render_template("login.html")
        form = request.form
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.update_project(id, form['title'], form['description'], form['teamlead'], form['team'], form['video_url'], form['images_link'], form["topic"], filename, form['links'])
            return redirect("/myprojects", code=200)

@app.route('/projects/<id>/delete', methods=['POST'])
def delete_project(id):
    if confirm_token(request.cookies.get("jwt")):
        flash('You are not logged in')
        return render_template("login.html")
    if db.is_user_teamlead(id, confirm_token(request.cookies.get("jwt"))):
        db.delete_project(id)
        flash('Project deleted')
        return redirect("/myprojects", code=302)
    else:
        flash('You are not owner of this project. Ask teamlead of this project to delete it')
        return redirect("/myprojects", code=302)

@app.route('/myprojects', methods=['GET'])
def get_my_projects():
    ans = db.get_projects_by_username(confirm_token(request.cookies.get("jwt")))
    return render_template("myprojects.html", ans = ans)
     
app.run("0.0.0.0", port=5000, debug=True)