#!/usr/bin/env python3

import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
import env as config

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
@app.route('/home/<list_id>')
def home(list_id = ObjectId("000000000000000000000000")):
    init_list = mongo.db.lists.find_one({"_id": ObjectId(list_id)})
    return render_template("landing.html", lists=mongo.db.lists.find(),
        ilist=init_list)
    # if list_id == ObjectId("000000000000000000000000"):
    #     return render_template("landing.html", lists=mongo.db.lists.find())
    # else:
    #     return render_template("landing.html", lists=mongo.db.lists.find(),
    #         ilist=init_list)


@app.route('/signupin')
def signupin():
    return render_template("signupin.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
