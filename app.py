import email
from email.message import EmailMessage
import re
from click import prompt
from flask import Flask, render_template, request
import requests
import cohere
import firebase_admin
from firebase_admin import db

co = cohere.Client('<API KEY COHERE>')
app = Flask(__name__)
cred_obj = firebase_admin.credentials.Certificate("<FIREBASE JSON>")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"<DATABASE URL>/"
	})

url = "https://api.courier.com/send"
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == 'POST':
        print("Hello there!")       


    return render_template('index.html', **locals())

@app.route('/reviews', methods=["GET", "POST"])
def reviews():
    ref = db.reference("/addbusiness")
    ref1= db.reference("/reviews")
    databasetxt= (ref.get())
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        businessemail = request.form['email']
        businessname = request.form['name']
        feedback = request.form['feedback']
        userno = "user"+str(len(ref1.get())+1)
        #userno="user2"
        txt= {
        "{}".format(userno):
          {
            "username": "{}".format(username),
            "useremail": "{}".format(useremail),
            "feedback": "{}".format(feedback),
            "businessemail": "{}".format(businessemail),
            "businessname": "{}".format(businessname)
          }
        }
        ref1.update(txt)
        #ref1.set(txt)
        print(txt) 
        payload = {
          "message": {
            "to": { 
            "email": "{}".format(businessemail)
            },
            "content":{
            "elements": [
                {
                "type": "meta",
                "title": "Someone Reviewed Your Business"
                },
                {
                    "type": "image",
                     "src": "https://raw.githubusercontent.com/cyrixninja/Eazy-Reviews/main/image/email-banner1.png"
                     },
                {
                "type": "text",
                "content": "**Customer Name :** {}".format(username)
                },
                                {
                "type": "text",
                "content": "**Customer Email :** {} ".format(useremail)
                },
                 {
                "type": "text",
                "content": "**Customer Feedback :** {} ".format(feedback)
                }
              
            ],
            "version": "2022-01-01",
            }
        }
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer pk_test_<COURIER API KEY>"
            }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)




    return render_template('reviews.html', **locals(),data=databasetxt)

@app.route('/add', methods=["GET", "POST"])
def add():
    ref = db.reference("/addbusiness")
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        email = request.form['email']
        links = request.form['links']

        userno = "user"+str(len(ref.get())+1)
        #userno="user1"
        txt= {
        "{}".format(userno):
          {
            "name": "{}".format(name),
            "about": "{}".format(desc),
            "email": "{}".format(email),
            "links": "{}".format(links)
          }
        }
        ref.update(txt)
        #ref.set(txt)
        print(txt)


    return render_template('add.html', **locals())

@app.route('/getreport', methods=["GET", "POST"])
def getreport():
    ref= db.reference("/reviews")
    if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            data= (ref.get())
            val = data.items()
            getdata = [value['feedback'] for key, value in val if(value["businessname"] == name) and (value["businessemail"] == email)]
            listToStr = '\n'.join(getdata)
            response = co.generate( 
            model='xlarge', 
            prompt='This program will summarise consumer feedback and provide you with detailed reports:\n\nReviews:\nI loved your services and would surely try your services again.\nYour Sevices were best but a bit expensive.\n\nCustomer Reviews Summarised: \nCustomers love your services. But your services are a bit expensive.\n\n--\nReviews:\nLiked your service but customer support wasn\'t helpful. \nWould try it again maybe\nYou should improve consumer services\n\n\nCustomer Reviews Summarised:\nCustomers didn\'t like your service. They will probably try it again. You guys should improve consumer services.\n\n--\nReviews:\n{}\n\nCustomer Reviews Summarised:\n'.format(listToStr), 
            max_tokens=100, 
            temperature=0.9, 
            k=0, 
            p=1, 
            frequency_penalty=0, 
            presence_penalty=0, 
            stop_sequences=["--"], 
            return_likelihoods='NONE') 
            summary= response.generations[0].text.strip("--")
            result = " ".join(line.strip() for line in summary.splitlines())
            print(result)
            payload = {
          "message": {
            "to": { 
            "email": "{}".format(email)
            },
            "content":{
            "elements": [
                {
                "type": "meta",
                "title": "Your Customer Feedback Report"
                },
                {
                    "type": "image",
                     "src": "https://raw.githubusercontent.com/cyrixninja/Eazy-Reviews/main/image/email-banner.png"
                     },
                {
                "type": "text",
                "content": "**Customer Feedback Summary :** {}".format(result)
                },
                 {
                "type": "text",
                "content": "**Customer Reviews :** {} ".format(listToStr)
                }
              
            ],
            "version": "2022-01-01",
            }
        }
        }
            headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer pk_test_<COURIER API KEY>"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            print(response.text)

       


    return render_template('getreport.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)