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

def add_user(name,phone_no,email,password,role):
    password_hashed = pbkdf2_sha256.hash(password)
    user = User(name = name, phone_no = phone_no, email = email, password = password_hashed, role = role)
    db.session.add(user)
    db.session.commit()
    
def add_student(roll_no, name,age,gender,caste,school,pincode,admission_date,dropout_date,dropout_reason):
    student = Student(roll_no = roll_no, name = name, age = age, gender = gender, caste = caste, school = school, pincode = pincode, admission_date = admission_date, dropout_date = dropout_date, dropout_reason = dropout_reason)
    db.session.add(student)
    db.session.commit()
    
def verify(email,password):
    user = User.query.filter_by(email).first()
    return pbkdf2_sha256.verify(password, user.password)
@app.route("/")
def root():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port = 8000 )