import os
import sys


from flask import Flask
from gunicorn.app.wsgiapp import run

app = Flask(__name__)


# Set command-line arguments for Gunicorn
sys.argv = [
    'gunicorn',  # Simulate calling gunicorn
    'main:app',  # Your Flask app
    '-b', '0.0.0.0:5000'  # Bind to port 5000
]


@app.route("/")
def hello_world():
    #name = os.environ.get("NAME", "World")
    #return "Hello {}!".format(name)
    # Put your logic here
    return "Done", 200 #return nicely the response to the request


@app.route("/health")
def health():
    #name = os.environ.get("NAME", "World")
    #return "Hello {}!".format(name)
    # Put your logic here
    return "OK", 200 #return nicely the response to the request

if __name__ == "__main__":
    run()
