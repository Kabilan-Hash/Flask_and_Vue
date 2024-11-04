import time
import psycopg2
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class DataEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname='mydatabase', 
                user='postgres', 
                password='postgres', 
                host='db'
            )
            conn.close()
            break  
        except psycopg2.OperationalError:
            print("Database not ready yet. Waiting...")
            time.sleep(5)  

@app.route('/')
def index():
    return "Hello, Flask!"

@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()  
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_entry = DataEntry(name=name, email=email)

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Data added successfully!", "id": new_entry.id}), 201



@app.route('/users', methods=['GET'])
def get_users():
    users = DataEntry.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/edit/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.get_json()
    user = DataEntry.query.get_or_404(id)
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify(message='User updated successfully!')

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = DataEntry.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message='User deleted successfully!')


if __name__ == "__main__":
    wait_for_db()  
    db.create_all()  
    app.run(host='0.0.0.0', port=5000)
