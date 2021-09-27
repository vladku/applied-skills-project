import os

from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client(project='roi-takeoff-user79')

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route("/users")
def users():
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    return [doc.to_dict() for doc in docs]

@app.route("/users/<id>", methods = ['GET', 'POST', 'DELETE'])
def user(id):
    if request.method == 'GET':
        users_ref = db.collection(u'users')
        docs = users_ref.stream()
        return [doc.to_dict() for doc in docs]
    if request.method == 'POST':
        doc_ref = db.collection(u'users').document(u'user')
        doc_ref.set({
            u'first': u'Alan',
            u'middle': u'Mathison',
            u'last': u'Turing',
            u'born': 1912
        })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))