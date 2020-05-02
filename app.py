#!/usr/bin/env python3

import os
from flask import Flask, render_template, redirect, request, url_for
# from flask_pymongo import PyMongo, pymongo
# from bson.objectid import ObjectId
# import env as config

app = Flask(__name__)

# app.config[] = ''
# app.config[] = ''

# mongo = PyMongo(app)

# @app.route('/')
# def hello():
#     return 'Hello world ...again!'

@app.route('/')
@app.route('/home')
def home():
    return render_template("landing.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
