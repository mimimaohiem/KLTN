import os
import sys
import json
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from pydantic import BaseModel

# Add the path to the directory for custom modules
sys.path.append('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/pSCRDRtagger')

# Import custom modules for text processing
from data_processing_quan_ly import table_data
from text_processing import process_text
from pos_tagger import pos_tag

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/pSCRDRtagger/flask-firestore_quan_ly/key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')
users_ref = db.collection('users')

# Pydantic model for note input
class Note(BaseModel):
    note: str

@app.route('/submit', methods=['POST','PUT'])
def submit():
    """
    Process the note and perform POS tagging
    """
    username = "default_user"  # Static user since no login
    data = request.get_json()
    note_data = data.get('note')
    if not note_data:
        return jsonify({"message": "No note provided"}), 400

    processed_output = process_text(note_data)
    pos_tagged = pos_tag(processed_output)
    df = table_data(pos_tagged)

    json_str = df.to_json(orient='records')
    notes_json = json.loads(json_str)

    save_note_to_firestore(username, note_data, notes_json)

    return jsonify({
        "user": username,
        "processed_data": notes_json
    }), 200

def save_note_to_firestore(username, note_data, processed_data):
    """
    Save the note to Firestore under a specific user's note collection
    """
    user_notes_ref = db.collection('users').document(username).collection('user_notes')
    user_notes_ref.add({
        'note': note_data,
        'processed_data': processed_data,
        'timestamp': firestore.SERVER_TIMESTAMP
    })


@app.route('/get_notes', methods=['GET'])
def get_notes():
    """
    Retrieve notes from Firestore
    """
    username = "default_user"  # Static user since no login
    user_notes_ref = db.collection('users').document(username).collection('user_notes')
    notes = user_notes_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()

    notes_list = []
    for note in notes:
        note_dict = note.to_dict()
        note_dict['id'] = note.id
        notes_list.append(note_dict)

    return jsonify({
        "user": username,
        "notes": notes_list
    }), 200
 
@app.route('/add', methods=['POST'])
def create():
    """
    Add document to Firestore collection with request body
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
    """
    Fetches documents from Firestore collection as JSON
    """
    try:
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
    Update document in Firestore collection with request body
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
    Delete a document from Firestore collection
    """
    try:
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8888))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
