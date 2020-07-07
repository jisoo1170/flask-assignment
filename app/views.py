from app import app
from app.models import Board


@app.route('/')
def index():
    return "Hello"
