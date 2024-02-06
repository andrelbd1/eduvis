from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/eduvisPHD45'
Bootstrap(app)

# Basic Routes #

# @app.route('/')
# def index():
# 	return redirect(url_for('eduvis.index'))

# @app.errorhandler(404)
# def not_found(error):
# 	return render_template('404.html'), 404

# Eduvis Module
from app.eduvis.views import mod as eduvisModule
app.register_blueprint(eduvisModule)
