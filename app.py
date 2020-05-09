#!/usr/bin/env python3

import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from datetime import datetime
import wikipedia as wiki
import env as config

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'milestone3'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


# set timestamp
def set_now():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


# find list using lists "_id"
def find_list_id(list_id):
    lst = mongo.db.lists.find({"_id": ObjectId(list_id)})
    return lst

# find item using items "_id"
def find_item_id(list_id):
    itm = mongo.db.items.find({"_id": ObjectId(list_id)})
    return lst


# find items using items "list_id"
def find_item_list(list_id):
    itm_list = mongo.db.items.find({"list_id": ObjectId(list_id)})
    return itm_list


# find all lists
def find_lists():
    lsts = mongo.db.lists.find()
    return lsts


# find all categories
def find_categories():
    cats = mongo.db.categories.find()
    return cats


# insert list to lists
def add_list(**kwargs):
    mongo.db.lists.insert_one(kwargs)


def add_item(**kwargs):
    mongo.db.items.insert_one(kwargs)


# insert item to items
def set_insert_list(**kwargs):
    for k, v in kwargs.items():
        list1 = mongo.db.lists.find({k: v})
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

    cat = mongo.db.categories.find({"cat_name": category}, {"fields"})

    for j in cat:
        for k, v in j.items():
            if k == "fields":
                cat_dict[k] = v

    return(list_dict, cat_dict, obj)


def set_insert_items(list_id):
    itm_list = []

    itm = find_item_list(list_id)

    for m in itm:
        for n, o in m.items():
            if n == "_id":
                item_id = o
            if n == "items":
                itm_list.append(o)

    return(itm_list, item_id)


@app.route('/')
@app.route('/home')
@app.route('/home/<list_id>')
def home(list_id=ObjectId("000000000000000000000000")):
    if list_id != ObjectId("000000000000000000000000"):
        dict_list = []
        init_list = find_list_id(list_id)
        itms = find_item_list(list_id)
        for m in itms:
            itm_list = {}
            for k, v in m.items():
                if k == "_id":
                    itm_list[k] = v
                elif k == "items":
                    for l, w in v.items():
                        if l == "title":
                            itm_list[l] = w
                            try:
                                title = wiki.page(w).title
                                summary = wiki.summary(w, sentences=5)
                            except:
                                title = "Error"
                                summary = "Em... Sorry! Something went wrong getting the info from Wikipedia"
                        else:
                            itm_list[l] = w
            dict_list.append(itm_list)

        return render_template("landing.html", lists=find_lists(),
                               ilist=dict_list, wiki_smry=summary, wiki_ttl=title)
    else:
        init_list = find_list_id(list_id)
        return render_template("landing.html", lists=find_lists())


@app.route('/create')
def create():
    return render_template("create_list.html", clist=find_categories())


@app.route('/insert_list', methods=['POST', 'GET'])
def insert_list():
    list_name = request.form.get("list_name")
    list_author = request.form.get("list_author")
    categories = request.form.get("categories")
    created = set_now()
    add_list(list_name=list_name, list_author=list_author,
             categories=categories, created=created)

    the_list = set_insert_list(created=set_now())

    return render_template("add_items.html",
                           the_list=the_list[0],
                           the_cat=the_list[1],
                           obid=the_list[2]
                           )


@app.route('/add_items/<obj>', methods=['POST', 'GET'])
def add_items(obj):
    list_id = ObjectId(obj)
    data = request.form.to_dict()
    add_item(list_id=list_id, items=data, created=set_now())

    the_list = set_insert_list(_id=ObjectId(obj)) + set_insert_items(obj)

    return render_template("add_aitems.html",
                           the_list=the_list[0],
                           the_cat=the_list[1],
                           obid=the_list[2],
                           the_itm=the_list[3],
                           itm_id=the_list[4]
                           )


@app.route('/add_aitems/<obj>', methods=['POST', 'GET'])
def add_aitems(obj):
    list_id = ObjectId(obj)

    the_list = set_insert_list(_id=ObjectId(obj)) + set_insert_items(obj)

    return render_template("add_aitems.html",
                           the_list=the_list[0],
                           the_cat=the_list[1],
                           obid=the_list[2],
                           the_itm=the_list[3],
                           itm_id=the_list[4]
                           )


@app.route('/finish_items')
def finish_items():
    return redirect(url_for('home'))


@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    list_id = mongo.db.items.find_one({"_id": ObjectId(item_id)}, {"list_id"})
    rtrn_id = list_id["list_id"]
    mongo.db.items.remove({'_id': ObjectId(item_id)})
    return redirect(url_for('home', list_id=rtrn_id))


@app.route('/delete_list/<list_id>')
def delete_list(list_id):
    mongo.db.items.remove({'list_id': ObjectId(list_id)})
    mongo.db.lists.remove({'_id': ObjectId(list_id)})
    return redirect(url_for('home'))


@app.route('/edit_list/<list_id>')
def edit_list(list_id):
    list_a = find_list_id(list_id)
    itms = find_item_list(list_id)

    the_list = set_insert_list(_id=ObjectId(
        list_id)) + set_insert_items(list_id)

    return render_template("edit_list.html",
                           the_list=the_list[0],
                           the_cat=the_list[1],
                           obid=the_list[2],
                           the_itm=the_list[3],
                           itm_id=the_list[4]
                           )


@app.route('/update_list/<list_id>', methods=['POST'])
def update_list(list_id):
    list_data = request.form.to_dict()
    list_data["created"] = set_now()
    print(list_data)
    mongo.db.lists.update({"_id":ObjectId(list_id)}, {"$set": list_data})

    return redirect(url_for('edit_list', list_id=list_id))


@app.route('/update_item/<list_id>/<item_id>', methods=['POST', 'GET'])
def update_item(list_id, item_id):
    item_data = request.form.to_dict()
    item_data["created"] = set_now()
    list_data["created"] = set_now()
    mongo.db.items.update({"_id":ObjectId(item_id)}, {"$set": item_data})
    mongo.db.lists.update({"_id":ObjectId(list_id)}, {"$set": list_data})

    return redirect(url_for('edit_list', list_id=list_id))


@app.route('/wiki')
def wikipedia():
    return redirect("http://www.wikipedia.org")


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080)),
        debug=True
    )
