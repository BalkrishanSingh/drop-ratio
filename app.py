from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)

class User(db.Model):
    
    sno = db.Column(db.Integer)
    name = db.Column(db.String(128),nullable = False)
    phone_no = db.Column(db.Integer(),nullable = False, unique= True, primary_key = True)
    email = db.Column(db.String(256), nullable = False, unique= True)
    password = db.Column(db.VARBINARY, nullable = False)
    school = db.Column(db.String(256))
    role = db.Column(db.String(128),nullable= False)
    
class School(db.Model):
    
    sno = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(256),nullable = False)
    affiliation = db.Column(db.String(64))
    dropout_number = db.Column(db.Integer)
class Student(db.Model):
    
    roll_no:int = db.Column(db.Integer, primary_key = True)
    name:str = db.Column(db.String(256), nullable = False)
    age:int = db.Column(db.Integer, nullable = False)
    gender:str = db.Column(db.String(1), nullable= False)
    caste:str = db.Column(db.String(128))
    school:str = db.Column(db.String(256), nullable = False)
    pincode:int = db.Column(db.Integer, nullable = False)
    admission_date = db.Column(db.DateTime,nullable = False)
    dropout_date = db.Column(db.DateTime)
    dropout_reason:str = db.Column(db.String(512))

def add_user(user_data):
    """user_data = {"name":request.form["name"], "phone_no" : request.form["phone_no"], "email" : request.form["email"], password : request.form["password"] ,"school" : request.form["school"] ,"role" : request.form["role"] }"""
    
    user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    
def add_student(student_data:dict):
    """student_data = {"roll_no" :request.form["roll_no"], "name" : request.form["name"], "age" : request.form["age"], "gender" : request.form["gender"], "caste" : request.form["caste"], "school" : request.form["school"], "pincode" : request.form["pincode"], "admission_date" : request.form["admission_date"], "dropout_date" : request.form["dropout_date"], "dropout_reason" : request.form["dropout_reason"]"""
    student = Student(**student_data)
    db.session.add(student)
    db.session.commit()
    
def update_student(roll_no:int,student_data:dict):
    Student.query.filter_by(roll_no).update(student_data)
    db.session.commit()
    
def update_user(phone_no:int ,user_data:dict):
    User.query.filter_by(phone_no).update(user_data)
    db.session.commit()
    
def verify(email:str, password:str):
    user = User.query.filter_by(email).first()
    return pbkdf2_sha256.verify(password, user.password)

def update_dropouts(sno:int,school_name:str):
    dropouts = len(Student.query.fliter_by(school_name).all())
    School.query.filter_by(sno).update(dict(dropout_number = dropouts))
    db.session.commit()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/head/<string:school>")
def head(school):
    students = Student.query.filter_by(school = school).all()
    return render_template("head.html",students = students)

@app.route("/admin")
def admin():
    schools = School.query.all()
    for i in schools:
        update_dropouts(i[0],i[1])
    schools = School.query.all()
    return render_template("admin.html",schools = schools)

if __name__ == "__main__":
    app.run(debug=True,port = 8000 )