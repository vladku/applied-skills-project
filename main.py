import os
import uuid

from datetime import datetime
from flask import Flask, request, render_template, jsonify
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

@app.route('/')
def index():
    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return render_template('index.html', dateNow=date_time, all=get_all())

def get_all():
    ref = db.collection(u'messages')
    docs = ref.stream()
    d = [doc.to_dict() for doc in docs]
    return sorted(d, key=lambda x: x["data"], reverse=True)

@app.route("/api/messages", methods = ['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(get_all())
    elif request.method == 'POST':
        doc_ref = db.collection(u'messages').document(str(uuid.uuid1()))
        doc_ref.set({
            u'data': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            u'text': request.json["message"]
        })
        return doc_ref.id, 200

@app.route("/api/messages/<id>", methods = ['GET', 'DELETE'])
def user(id):
    if request.method == 'GET':
        return db.collection(u'users').document(id).to_dict()
    if request.method == 'DELETE':
        db.collection(u'users').document(id).delete()
        return {}, 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
