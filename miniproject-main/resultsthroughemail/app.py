from email import message
from types import MethodType
from flask import Flask,render_template,request,redirect, url_for
from flask_mail import Mail,Message
import csv,smtplib, ssl
import pandas as pd
from email.message import EmailMessage

app=Flask(__name__)
mail=Mail(app)

@app.route('/')
def index():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username=request.form["username"]
        password=request.form["password"]
        if  username!= 'admin' or password != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return render_template('home.html', error=error)  
        else:    
            return render_template('login.html',username=username)  

@app.route('/sub',methods=['GET', 'POST'])
def getcsv():
    if request.method == 'POST':
       results=[]
      
       
       
       subject='Your Marks Hi {name}, your marks  are {total}'
       body= 's1={s1},s2={s2},s3={s3},s4={s4},s5={s5}'
       
       
       message = f'Subject: {subject}\n\n{body}'
       from_address = 'resultsthroughemail@gmail.com'
       password = '6305077750'
       context = ssl.create_default_context()
       with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
          server.login(from_address, password)
          datacsv=request.form['datacsv']
          with open(datacsv) as file:
              reader = csv.reader(file)
              next(reader)  # Skip header row
              for ID,NAME,BRANCH,SECTION,S1,S2,S3,S4,S5,TOTAL,STATUS,EMAIL in reader:
                   server.sendmail(from_address,EMAIL,message.format(name=NAME,total=TOTAL,s1=S1,s2=S2,s3=S3,s4=S4,s5=S5),)
       datacsv=request.form['datacsv']
       with open(datacsv) as file:
           csvfile=csv.reader(file)
           for row in csvfile:
               results.append(row)
       results=pd.DataFrame(results)
       return render_template('details.html',results=results.to_html(header=False,index=False))
     
  


if __name__=="__main__":
    app.run(debug=True)
