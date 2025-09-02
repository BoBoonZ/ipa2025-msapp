from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

import os

sample = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]
mystatus = mydb["interface_status"]


@sample.route("/")
def main():
    return render_template("index.html", data=mycol.find())


@sample.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        x = mycol.insert_one({
            "ip": ip,
            "username": username,
            "password": password
        })
        print(x)
    return redirect("/")


@sample.route("/delete/<idx>", methods=["POST"])
def delete_comment(idx):
    try:
        if idx:
            myquery = {'_id': ObjectId(idx)}
            x = mycol.delete_one(myquery)
            print(x.deleted_count, " documents deleted.")
    except Exception:
        pass
    return redirect(url_for("main"))


@sample.route("/router/<id>", methods=["GET"])
def get_router(id):
    result = mystatus.find({"router_ip": id})
    return render_template("router.html", id=id, data=result)


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)

