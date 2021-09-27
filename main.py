import os

from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)

# db = firestore.Client(project='roi-takeoff-user79')
# users_ref = db.collection(u'users').document(u'user')
# docs = users_ref.get()
# print(next(docs))
# print([doc.to_dict() for doc in docs])

# Add a new document
db = firestore.Client()
doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

# Then query for documents
users_ref = db.collection(u'users')

for doc in users_ref.stream():
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route("/users")
def users():
    return {"a": 123}
    # users_ref = db.collection(u'users')
    # docs = users_ref.stream()
    # return {"result": [doc.to_dict() for doc in docs]}

# @app.route("/users/<id>", methods = ['GET', 'POST', 'DELETE'])
# def user(id):
#     if request.method == 'GET':
#         users_ref = db.collection(u'users')
#         docs = users_ref.stream()
#         return [doc.to_dict() for doc in docs]
#     if request.method == 'POST':
#         doc_ref = db.collection(u'users').document(u'user')
#         doc_ref.set({
#             u'first': u'Alan',
#             u'middle': u'Mathison',
#             u'last': u'Turing',
#             u'born': 1912
#         })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))