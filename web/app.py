import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

sample = Flask(__name__)

data = []

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["router_collection"]

@sample.route("/")
def main():
    routers = list(mycol.find({}))
    for r in routers:
        r["_id"] = str(r["_id"])
    return render_template("index.html", data=routers)

@sample.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username:
        data.append({"ip": ip, "username": username})
        router_to_add = {"ip": ip, "username": username, "password": password}
        mycol.insert_one(router_to_add)
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_router():
    doc_id = request.form.get("id")
    if doc_id:
        try:
            mycol.delete_one({"_id": ObjectId(doc_id)})
        except Exception as e:
            print("Delete failed:", e)
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)