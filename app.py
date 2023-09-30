from flask import Flask, render_template, request
from users import main


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username + " " + password)
    main(username, password)
    return render_template("index.html")


if __name__ == "__main__":
    app.run('localhost', 5000) 