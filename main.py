from flask import Flask, request, render_template, redirect, make_response, flash
import db as db
import jwt
import json
#from email import send_email
from itsdangerous import URLSafeTimedSerializer
import parse
from flask_mail import Message, Mail
import re

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db.create_all()

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'silaederprojects@gmail.com'  
app.config['MAIL_DEFAULT_SENDER'] = 'silaederprojects@gmail.com'  
app.config['MAIL_PASSWORD'] = 'waduszxztipcdeyd'  

mail_sender = Mail(app)

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
    if (db.create_project("Silaeder Projectssssssssssssssss", "ILYASTARCEK", "ICT", "ILYASTARCEK, NICITATURBOBOY", "site_for_Silaeder_projects", "https://silaeder.com", "github") != True):
        print("aguzog")
    ans = db.get_all_projects()
    return render_template("index.html", ans = ans)

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
            resp = make_response(redirect("/", code=302))
            

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
    try:
        username = confirm_token(token)
        print(username)
    except:
        flash('The confirmation link is invalid or has expired. Check your email')
        return redirect('/', code=302)
    token = jwt.encode(payload={"name": username}, key=parse_data("secret_key"))
    if db.check_auth_user(username):
        print(db.check_auth_user(username))
        flash('Account already confirmed. Please login')
        return redirect('/login', code=302)
    else:
        db.auth_user(username)
        flash('You have confirmed your account. Thanks!')
        resp = make_response(redirect("/", code=302))
        resp.set_cookie("jwt", token)
        return resp

app.run("0.0.0.0", port=5678, debug=True)