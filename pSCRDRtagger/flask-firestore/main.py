import os
import sys
import json
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
import bcrypt
# from your_module import process_text, pos_tag, data_processing
from pydantic import BaseModel



sys.path.append('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/pSCRDRtagger')


from data_processing import table_data, save_dataframe
from text_processing import process_text
from pos_tagger import pos_tag



# Initialize Flask App
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# Initialize Firestore DB
cred = credentials.Certificate('/mnt/c/Users/hoain/Tokenizer/py/RDRPOSTagger/pSCRDRtagger/flask-firestore/key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')
users_ref = db.collection('users')

# Pydantic model for note input
class Note(BaseModel):
    note: str

@app.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user with username and password.
    Password is hashed before being stored in Firestore.
    Ensure that both username and password are provided.
    """
    data = request.get_json()

    # Check if both username and password are provided
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Check if user already exists
    if users_ref.document(username).get().exists:
        return jsonify({"message": "User already exists"}), 409

    # Hash the password and store user information
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users_ref.document(username).set({
        'username': username,
        'password': hashed_password.decode('utf8')
    })
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT if credentials are valid.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_doc = users_ref.document(username).get()

    if user_doc.exists and bcrypt.checkpw(password.encode('utf8'), user_doc.to_dict()['password'].encode('utf8')):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
    
    
@app.route('/submit', methods=['POST'])
@jwt_required()
def submit():
    username = get_jwt_identity()
    data = request.get_json()
    note_data = data.get('note')
    if not note_data:
        return jsonify({"message": "No note provided"}), 400

    # Process the note and perform POS tagging
    processed_output = process_text(note_data)
    pos_tagged = pos_tag(processed_output)
    df = table_data(pos_tagged)

    # Convert DataFrame to JSON
    json_str = df.to_json(orient='records')
    notes_json = json.loads(json_str)

    # Proceed to save the note
    save_note_to_firestore(username, note_data, notes_json)

    return jsonify({
        "user": username,
        "processed_data": notes_json
    }), 200

def save_note_to_firestore(username, note_data, processed_data):
    # Reference to user's note collection   
    user_notes_ref = db.collection('users').document(username).collection('user_notes')
    # Add note to Firestore
    user_notes_ref.add({
        'note': note_data,
        'processed_data': processed_data,
        'timestamp': firestore.SERVER_TIMESTAMP
    })


@app.route('/get_notes', methods=['GET'])
@jwt_required()
def get_notes():
    """
    Retrieve notes from Firestore for the authenticated user.
    """
    username = get_jwt_identity()
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


# Assuming these are your custom processing functions
# def process_text(text):
#     return text.upper()  # Example processing

# def pos_tag(text):
#     return [{"word": word, "tag": "NOUN"} for word in text.split()]  # Example POS tagging

# def table_data(tagged_text):
#     return {entry['word']: entry['tag'] for entry in tagged_text}  # Example conversion to table




@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="Access granted to protected resource"), 200


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
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
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents

    """
    try:
        # Check if ID was passed to URL query
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
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection

#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         todo_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"
    
@app.route('/delete_note', methods=['DELETE'])
@jwt_required()
def delete_note():
    """
    Delete a note from Firestore for the authenticated user.
    """
    username = get_jwt_identity()  # Get the username from the JWT token
    data = request.get_json()
    note_id = data.get('id')  # ID of the note to delete

    if not note_id:
        return jsonify({"error": "Missing note ID"}), 400

    try:
        # Reference to the specific note document
        note_ref = db.collection('users').document(username).collection('user_notes').document(note_id)
        # Check if the note exists
        if not note_ref.get().exists:
            return jsonify({"error": "Document does not exist"}), 404
        
        # Delete the note
        note_ref.delete()
        return jsonify({"success": True, "message": "Note deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to delete note"}), 500


    
@app.route('/delete_data', methods=['GET', 'DELETE'])
@jwt_required()
def delete_data():
    """
    Delete a document from Firestore based on the document ID and collection name provided.
    """
    data = request.get_json()
    collection_name = data.get('collection_name')
    document_id = data.get('document_id')

    if not collection_name or not document_id:
        return jsonify({"message": "Missing collection name or document ID"}), 400

    try:
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.delete()
        return jsonify({"success": True, "message": "Document deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to delete document"}), 500


port = int(os.environ.get('PORT', 8888))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)