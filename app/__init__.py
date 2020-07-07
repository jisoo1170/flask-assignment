from flask import Flask
from mongoengine import connect

connect('tutorial')
app = Flask(__name__)


from app import views

app.run(debug=True)