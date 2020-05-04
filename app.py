#!/usr/bin/env python3

import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from datetime import datetime
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


@app.route('/create')
def create():
    cat_list = mongo.db.categories
    return render_template("create_list.html", clist=cat_list.find())


@app.route('/insert_list', methods=['POST','GET'])
def insert_list():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lists = mongo.db.lists
    categories = mongo.db.categories
    lists.insert_one({
        "list_name": request.form.get("list_name"),
        "list_author": request.form.get("list_author"),
        "categories": request.form.get("categories"),
        "created": now
    })
    clist = lists.find({"created":now})
    list = lists.find({"created":now})
    category = categories.find()
    return render_template("add_items.html",
        the_list=list,
        the_clist=clist,
        the_cat=category)


@app.route('/add_items')
def add_items():
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
