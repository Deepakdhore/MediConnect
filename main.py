
import logging

from flask_login import UserMixin
from flask import Flask, redirect,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user
from flask_mail import Mail
import json

import pymysql 
pymysql.install_as_MySQLdb()

with open('config.json','r') as c:
    params=json.load(c)["params"]

 

local_server=True
app=Flask(__name__)
app.secret_key='deepak'
app.logger.setLevel(logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/demo'
db=SQLAlchemy(app)


#SMTP MAIL SERVER SETTINGS

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USER_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gamil-password']
)  

mail=Mail(app)

#global variable
app.config['current_user'] = None

#db models (table name starting Capital)
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class Employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    phone=db.Column(db.Integer)
    address=db.Column(db.String(20))
    rank=db.Column(db.Integer)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),unique=True)
    email=db.Column(db.String(40),unique=True)
    password=db.Column(db.String(1000))
    user_type=db.Column(db.String(40))

class Doctors(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    age=db.Column(db.String(40))
    specialization=db.Column(db.String(40))
    shifts=db.Column(db.String(40))
    email=db.Column(db.String(40))

class Patients(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    age=db.Column(db.String(40))
    address=db.Column(db.String(40))
    phone=db.Column(db.BigInteger)
    
class Staffs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    age=db.Column(db.String(40))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.String(40))
    illness = db.Column(db.String(40))
    date = db.Column(db.Date)
    time = db.Column(db.String(40))
    address=db.Column(db.String(40))
    phone=db.Column(db.BigInteger)
    doctor=db.Column(db.String(40))

@app.route('/')
def home():
    return render_template('index.html')
   #try:
      #  Test.query.all()
      #  return 'db Connected'
    #except:
     #   return 'db not connected'

  #  return render_template('index.html')

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        rank = request.form.get('rank')
        
        # Get the maximum ID value from the database
        max_id = db.session.query(db.func.max(Employee.id)).scalar()

        # Increment the maximum ID value to get the next ID
        next_id = max_id + 1 if max_id is not None else 1
        
        query = Employee(id=next_id, name=name, phone=phone, address=address, rank=rank)
        db.session.add(query)
        db.session.commit()
    return render_template('index.html')

@app.route('/about')
def about():
    employees = Employee.query.all()
    return render_template('about.html', employees=employees)

@app.route('/high_rank',methods=['POST','GET'])
def high_rank():
    highest_rank_employee = Employee.query.order_by(Employee.rank).first()
    return render_template('rank.html', employee=highest_rank_employee)

@app.route('/update_rank', methods=['POST'])
def update_rank():
    employee_id = request.form.get('employee_id')
    new_rank = request.form.get('new_rank')

    employee = Employee.query.get(employee_id)
    if employee:
        employee.rank = new_rank
        db.session.commit()
        return render_template('about.html')

    return redirect('/about') 

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        user_type=request.form.get("user_type")
        print(username,email,password,user_type)

        user_email=Users.query.filter_by(email=email).first()
        user_username=Users.query.filter_by( username = username).first()
        if user_email or user_username:
            print("email already exists");
            return render_template('/signup.html')
        
        new_user=Users(username=username,email=email,password=password,user_type=user_type)
    
        db.session.add(new_user);
        db.session.commit()
        
        user = Users.query.filter_by(username=username).first()
        id=user.id

        if user_type=='Patient':
            name=request.form.get('name')
            p_age=request.form.get('patientAge')
            address=request.form.get('address')
            phone=request.form.get('phone')
            print(id,name,email,password,p_age,address,phone)

            p_user=Patients(id=id,name=name,age=p_age,address=address,phone=phone)
            
            db.session.add(p_user);
            db.session.commit()
            return render_template('signin.html')

        elif user_type=='Doctor':
            d_name=request.form.get('d_name')
            d_age=request.form.get('doctorAge')
            specialization=request.form.get('specialization')
            shifts=request.form.get('shifts')
            print(id,d_name,d_age,specialization,shifts,email)
            
            doc_user=Doctors(id=id,name=d_name,age=d_age,specialization=specialization,shifts=shifts,email=email)
            
            db.session.add(doc_user)
            db.session.commit()
            return render_template('signin.html')    
        
        elif user_type=='Staff':
            s_age=request.form.get('staffAge')
            s_name=request.form.get('s_name')
            print(username,email,s_name,password,s_age)

            s_user=Staffs(id=id,name=s_name,age=s_age)
            
            db.session.add(s_user);
            db.session.commit()
            return render_template('signin.html')
        #if user_type=='Doctor':
         #   db.session.add(new_user);
          #  db.session.commit()
    return render_template('signup.html')


@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == "POST":
        username=request.form.get("Username")
        password=request.form.get("Password")
        user=Users.query.filter_by(username = username).first()
        if user:
            print("user exisits ")
            
            if user.password==password:
                if user.user_type=="Doctor":
                    app.config['current_user']=username
                    return render_template('/doctorsLogin.html',username=username)
                if user.user_type=="Patient":
                    app.config['current_user']=username
                    return render_template('/patientsLogin.html',username=username)
                if user.user_type=="Staff":
                    app.config['current_user']=username
                    return render_template('/staffsLogin.html',username=username)
            else:
                print("wrong password")
                return render_template('signin.html')
        else:
            print("please signup first")
            return render_template('/signup.html')        
            
    

    return render_template('signin.html')


@app.route('/signout')
def signout():
    return render_template('index.html')
 
@app.route('/patientsDetails')
def patientsDetails():
    shedules=Appointment.query.all()
    return render_template('patientDetails.html',shedules=shedules)


@app.route('/staffsLogin')
def staffsLogin():
    username=app.config['current_user']
    return render_template('staffsLogin.html',username=username)

@app.route('/patientsLogin')
def patientsLogin():
    username=app.config['current_user']
    return render_template('patientsLogin.html',username=username)

@app.route('/appointment')
def appointment():
    username=app.config['current_user']
    return render_template('appointment.html',username=username)

@app.route('/booking',methods=['GET','POST'])
def booking():
    if request.method == "POST":
        P_name=request.form.get("patientName")
        P_age=request.form.get("patientAge")
        illness=request.form.get("illness")
        date=request.form.get("date")
        time=request.form.get("time")
      
        current_user = app.config['current_user']
        if current_user:
            user = Users.query.filter_by(username=current_user).first()
            if user:
                user_id = user.id
                patientsD = Patients.query.filter_by(id=user_id).first()
                doctorsD = Doctors.query.filter_by(specialization=illness).all()
                filtered_doctors = [doctor for doctor in doctorsD if doctor.shifts == time]
                doctor_with_shift = next((doctor for doctor in filtered_doctors if doctor.shift == time), None)

                if doctor_with_shift:
                    patient=Appointment(id=id,name=P_name,age=P_age,illness=illness,date=date,time=time,address=patientsD.address,phone=patientsD.phone,doctor=doctor_with_shift.name)
                    db.session.add(patient)
                    db.session.commit()
                    username=app.config['current_user']
                    patient_data = {
                                    'username':username,
                                    'id': id,
                                    'name': P_name,
                                    'age': P_age,
                                    'illness': illness,
                                    'date': date,
                                    'time': time,
                                    'address': patientsD.address,
                                    'phone': patientsD.phone,
                                    'doctor': doctorsD.name
                                    }
                    print(P_name,P_age,illness,date,time)
                    return render_template('recipt.html', patient=patient_data)
                    

                else:
                    doctorsD = Doctors.query.filter_by(specialization=illness).first()
                    patient=Appointment(id=id,name=P_name,age=P_age,illness=illness,date=date,time=doctorsD.shifts,address=patientsD.address,phone=patientsD.phone,doctor=doctorsD.name)
                    db.session.add(patient)
                    db.session.commit() 
                    username=app.config['current_user'] 
                    patient_data = {
                                    'username':username,
                                    'id': id,
                                    'name': P_name,
                                    'age': P_age,
                                    'illness': illness,
                                    'date': date,
                                    'time': doctorsD.shifts,
                                    'address': patientsD.address,
                                    'phone': patientsD.phone,
                                    'doctor': doctorsD.name
                                    }
                    print(P_name,P_age,illness,date,time,time,time,time,time)
                    return render_template('recipt.html', patient=patient_data)
                
        print(P_name,P_name,P_name,P_name,P_name,P_name,P_name,P_name)
        username=app.config['current_user'] 
        return render_template('appointment.html',username=username)


                
@app.route('/recipt_actions',methods=['GET','POST'])
def recipt_actions():
    if request.method == 'POST':
        username=app.config['current_user']
        action = request.form.get('action')
        U_table=Users.query.filter_by(username=username).first()
        
        if action == 'confirm':
            mail.send_message('MediConnect',
            sender=params['gmail-user'],
            recipients=['deepakreddy060606@gmail.com'],
            body='Congragulations your appinotment has been confirmed')
            return render_template('patientsLogin.html',username=username)
            pass
        elif action == 'edit':
            return render_template("recipt.html")
    return render_template("appointment.html",username=username)
        
@app.route('/shedules',methods=['GET','POST'])
def shedules():
    username=app.config['current_user'] 
    U_table=Users.query.filter_by(username=username).first()
    d_id=U_table.id
    D_table=Doctors.query.filter_by(id=d_id).first()
    doctor_name=D_table.name
    shedules=Appointment.query.filter_by(doctor=doctor_name).all()
    return render_template("shedules.html",shedules=shedules)

@app.route('/docotrsLogin')
def docotrsLogin():
    username=app.config['current_user'] 
    return render_template('doctorsLogin.html',username=username)

@app.route('/viewDetails',methods=['GET','POST'])
def viewDetails():
    if request.method == 'POST':
        username=app.config['current_user'] 
        id = request.form.get('shedule_id')
        shedules=Appointment.query.filter_by(id=id).first()
        p_table=Patients.query.filter_by(phone=shedules.phone).first()
        patient_details={
                                    'username':username,
                                    'id': id,
                                    'gaurdian': p_table.name,
                                    'name': shedules.name,
                                    'age':shedules.age,
                                    'date': shedules.date,
                                    'time': shedules.time,
                                    'address': shedules.address,
                                    'phone':shedules.phone,
                                    'doctor': shedules.name
        }
        return render_template("veiwDetails.html",details=patient_details)

if __name__ == '__main__':
    app.run(debug=True)