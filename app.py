from flask import Flask

app = Flask(__name__)
app.secret_key = "monjiteam"

# Import routes from the user module
from user import routes
