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
    serializer = URLSafeTimedSerializer(parse_data('secret_key'))
    return serializer.dumps(email, salt=parse_data('salt_password'))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(parse_data('secret_key'))
    try:
        email = serializer.loads(
            token,
            salt=app.config['salt_password'],
            max_age=expiration
        )
    except:
        return False
    return email

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

        #code will be here, when login.html will be done

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
                flash('This email is not valid', 'error')
                return redirect("/regestration", code=302)

            if parse.parse_csv().index(form["email"]) == -1:
                flash('This is not silaeder email. Check it from Silaeder google sheet or ask administrator (@ilyastarcek), if your email is not there', 'error')
                return redirect("/regestration", code=302)
            
            if db.create_user(form['username'], form["email"], form['password'], form['name'], form['surname']) == False:
                flash('This username or email already exists', 'error')
                return redirect("/regestratio", code=302)
            
            token = jwt.encode(payload={"name": form["username"]}, key=parse_data("secret_key"))
            
            resp = make_response(redirect("/", code=302))
            resp.set_cookie("jwt", token)

            etoken = generate_confirmation_token(form["email"])
            confirm_url = f'http://127.0.0.1:5678/confirm/{etoken}'
            html = render_template('mail.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form['email'], subject, html)


            flash('A confirmation email has been sent via email.', 'success')
            return resp
        
        else:
            flash('You write incorrect password.', 'error')
            return redirect("/regestration", code=302)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    token = jwt.encode(payload={"name": form["username"]}, key=parse_data("secret_key"))
    if db.get_user_by_username(payload['name']) != []:
        flash('Account already confirmed. Please login.', 'success')
        return redirect('/login', code=302)
    else:
        flash('You have confirmed your account. Thanks!', 'success')
        db.auth_user(payload['name'])
    return redirect('/')

app.run("0.0.0.0", port=5678, debug=True)