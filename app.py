from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)
@app.route("/")
def root():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port = 8000 )