from flask import Flask
from backend.routes import *

app = Flask(__name__, template_folder='templates')

# Add other configurations if needed
