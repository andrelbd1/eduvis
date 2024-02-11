from flask import Flask, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/eduvisPHD45'
Bootstrap(app)

# Eduvis Module
from src.controller import mod as eduvis
app.register_blueprint(eduvis)