from flask import Flask, request, render_template, redirect, make_response, flash
import db as db
import jwt
import json
#from email import send_email
from itsdangerous import URLSafeTimedSerializer
import parse
from flask_mail import Message

app = Flask(__name__)

db.create_all()

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=parse_data('mail')
    )
    to.send(msg)

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
    if (db.create_project("Silaeder_Projects", "ILYASTARCEK", "ICT", "ILYASTARCEK, NICITATURBOBOY", "site_for_Silaeder_projects", "https://silaeder.com", "github") != True):
        print("aguzog")
    ans = db.get_all_projects()
    print(ans)
    return render_template("index.html", ans = ans)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        login = request.form["login"]
        password = request.form["password"]

        #code will be here, when login.html will be done

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == "GET"):
        pass
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

        if (len(form["password"]) >= 8 and len(form["password"]) <= 20 and hasDigits and hasLowerCase and hasSpases and hasUpperCase and hasSpecialCharecters and parse.parse_csv().find(form["email"]) == -1):
            if db.create_user(form['username'], form["email"], form['password'], form['name'], form['surname']) == False:
                return redirect("/registration", error="username or  already exists" , code=302)
            #check if username already exists and email already exists
            token = jwt.encode(payload={"name": form["username"]}, key=parse_data("secret_key"))
            
            resp = make_response(redirect("/", code=302))
            resp.set_cookie("jwt", token)

            etoken = generate_confirmation_token(form["email"])
            confirm_url = f'/confirm/{etoken}'
            html = render_template('user/activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form['email'], subject, html)


            flash('A confirmation email has been sent via email.', 'success')
            return resp
        
        else:
            return redirect("/registration", code=302)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    payload = jwt.decode(token, key=parse_data("secret_key"), algorithms="HS256")
    if db.get_user_by_username(payload['name']) != []:
        flash('Account already confirmed. Please login.', 'success')
        return redirect('/login', code=302)
    else:
        flash('You have confirmed your account. Thanks!', 'success')
        db.auth_user(payload['name'])
    return redirect('/')

app.run("0.0.0.0", port=5678, debug=True)