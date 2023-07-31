from flask import Flask, render_template
import db as db

app = Flask(__name__)

db.create_all()

@app.route('/', methods=['GET'])
def main():
    ans = db.get_all_projects()
    return render_template("index.html", projects = ans)

app.run("0.0.0.0", port=5678, debug=True)