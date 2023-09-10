from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)

class User(db):
    sno = db.Column(db.Integer)
    name = db.Column(db.String(128),nullable = False)
    phone_no = db.Column(db.Integer(10),nullable = False, unique= True, primary_key = True)
    email = db.Column(db.String(256), nullable = False, unique= True)
    password = db.Column(db.VARBINARY, nullable = False)
    role = db.Column(db.String(128),nullable= False)
    
class Student(db):
    roll_no = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(1), nullable= False)
    caste = db.Column(db.String(128))
    school = db.Column(db.String(256), nullable = False)
    pincode = db.Column(db.Integer, nullable = False)
    admission_date = db.Column(db.DateTime,nullable = False)
    dropout_date = db.Column(db.DateTime)
    dropout_reason = db.Column(db.String(512))
    
@app.route("/")
def root():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port = 8000 )