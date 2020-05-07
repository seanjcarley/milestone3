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
    if list_id != ObjectId("000000000000000000000000"):
        itm_list = []
        init_list = mongo.db.lists.find_one({"_id": ObjectId(list_id)})
        itms = mongo.db.items.find({"list_id":ObjectId(list_id)})
        for m in itms:
            for n, o in m.items():
                if n == "items":
                    itm_list.append(o)
        return render_template("landing.html", lists=mongo.db.lists.find(),
            ilist=itm_list)
    else:
        init_list = mongo.db.lists.find_one({"_id": ObjectId(list_id)})
        return render_template("landing.html", lists=mongo.db.lists.find())


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
        list_dict = {}
        cat_dict = {}
        for i in list1:
            for k, v in i.items():
                if k == "categories":
                    list_dict[k] = v
                    category = v
                elif k == "_id":
                    obj = v
                else:
                    list_dict[k] = v

        cat = categories.find({"cat_name": category}, {"fields"})

        for j in cat:
            for k, v in j.items():
                if k == "fields":
                    cat_dict[k] = v

        return(list_dict, cat_dict, obj)

    the_list = set_list(now)

    return render_template("add_items.html",
        the_list=the_list[0],
        the_cat=the_list[1],
        obid = the_list[2]
        )


@app.route('/add_items/<obj>', methods=['POST', 'GET'])
def add_items(obj):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list_id = ObjectId(obj)

    imd_data = request.form
    data = imd_data.to_dict()

    items = mongo.db.items
    lists = mongo.db.lists
    categories = mongo.db.categories

    items.insert_one({"list_id": list_id, "items": data, "created": now})

    list1 = lists.find({"_id":list_id})
    list_dict = {}
    cat_dict = {}
    itm_list = []

    def set_list(created):
        for i in list1:
            for k, v in i.items():
                if k == "categories":
                    list_dict[k] = v
                    category = v
                elif k == "_id":
                    obj = v
                else:
                    list_dict[k] = v

        cat = categories.find({"cat_name": category}, {"fields"})
        for j in cat:
            for k, v in j.items():
                if k == "fields":
                    cat_dict[k] = v

        itm = items.find({"list_id": list_id})

        for m in itm:
            print(m)
            for n, o in m.items():
                if n == "_id":
                    item_id = o
                if n == "items":
                    itm_list.append(ObjectId(o))
                    print(itm_list)

        return(list_dict, cat_dict, obj, itm_list, item_id)

    the_list = set_list(now)

    return render_template("add_aitems.html",
        the_list=the_list[0],
        the_cat=the_list[1],
        obid = the_list[2],
        the_itm = the_list[3],
        itm_id = the_list[4]
        )


@app.route('/finish_items')
def finish_items():
    return redirect(url_for('home'))

@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    list_id = mongo.db.items.find_one({"list_id":ObjectId(item_id)})
    mongo.db.categories.remove({'_id': ObjectId(item_id)})
    return redirect(url_for('home', list_id))


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
