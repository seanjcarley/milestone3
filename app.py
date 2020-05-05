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

    def set_list(created):
        list1 = lists.find({"created":created})
        for_list = []
        for_item = []
        for_id = []
        for i in list1:
            for k, v in i.items():
                if k != "categories":
                    for_list.append(v)
                elif k == "_id":
                    for_id.append(v)
                else:
                    for_list.append(v)
                    category = categories.find({"cat_name": v})
                    for j in category:
                        for l, w in j.items():
                            if l == "fields":
                                for a in w:
                                    for_item.append(a)
        return(for_list, for_item, for_id)

    the_list = set_list(now)

    return render_template("add_items.html",
        the_list=the_list[0],
        the_cat=the_list[1],
        id=the_list[2])


@app.route('/add_items', methods=['POST'])
def add_items():
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
