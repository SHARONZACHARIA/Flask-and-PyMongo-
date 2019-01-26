from flask import Flask,render_template,request,url_for,flash,session,redirect,json,jsonify
import os
from pymongo import MongoClient
from bson import ObjectId 
import datetime


app = Flask(__name__)  
app.static_folder ='static'
app.secret_key='secret_key'

client = MongoClient("mongodb://127.0.0.1:27017") #host uri  
#db = client.mymessagedb   #Select the database  
#msg = db.messages
#notes = db.note


@app.route("/")
@app.route("/home")
def home():
    return render_template("login.html")


@app.route("/login",methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form.get("uname")
        password = request.form.get("pass")
     
        t= todos1= msg.find({"uname":name,"password":password}).count()
        if t > 0 :
            session['username'] = name
            return render_template("home.html" ,username = session['username'])
            
        else:
            flash("wrong username or password")
            return render_template("login.html")
         

    else:
        return "something went wrong...."

@app.route('/register')
def register():
    return render_template("register.html")

@app.route("/show" ,methods=['POST'])
def show():
    if request.method=='POST':
        redirect('show')
        return  render_template("result.html",test=notes.find({"author":session['username']}),name=session['username'])


@app.route("/register_user",methods=['POST'])
def register_user():
    if request.method == 'POST' :
        name = request.form.get("uname")
        password = request.form.get("pass")
        email = request.form.get("email")
        if name =="" or password =="" or email =="":
            flash("all fields are necessary")
            return render_template("register.html")
        else:

            t= todos1= msg.find({"uname":name}).count()
            if t > 0 :
                flash("user already exists")
                return render_template("register.html")
           
            
            else:
            
                id = msg.insert_one({"uname":name,"password":password,"email":email})
                print(id)
                if id is not None:
                    return "user added"
                else:
                    return render_template("login.html")

@app.route("/save_note",methods=['POST'])
def save_form():
    if request.method == 'POST':
        notes.insert_one({
            "time":str(datetime.datetime.now()),
            "author":session['username'],
            "note":request.form.get("note")
        })

       
        flash("note uploaded.....")
    return render_template("home.html")
    

@app.route("/logout",methods=['POST'])
def logout():
    if request.method =='POST':
        session.pop('username',None)
        return render_template("login.html")

@app.route("/api")
def api():
    output =[]
    for user_details in notes.find():
        output.append({"time":user_details['time'],"author":user_details['author'],'note':user_details['note']})
    return jsonify({'result':output})
    

@app.route("/api_users")
def api_users():
    output =[]
    for user_details in msg.find():
        output.append({"uname":user_details['uname'],'email':user_details['email']})
    return jsonify({'result':output})

if __name__ == "__main__":  
  
    app.run()  
