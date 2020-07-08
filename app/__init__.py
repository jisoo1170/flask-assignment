from flask import Flask
from mongoengine import connect

connect('tutorial')
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


from app import views

app.run(debug=True)