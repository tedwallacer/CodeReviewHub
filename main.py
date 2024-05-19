from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import git

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return "Hello, this is the main page of the code management system."

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists!'}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully!'}), 200
    return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!'}), 200

@app.route('/submit_code', methods=['POST'])
def submit_code():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to submit code.'}), 401
    return jsonify({'message': 'Code submitted successfully!'}), 202

@app.route('/review_code', methods=['GET', 'POST'])
def review_code():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to review code.'}), 401
    return jsonify({'message': 'Code review functionality is not implemented yet.'}), 501

def fetch_latest_code_from_git(repo_url):
    repo_dir = '/path/to/your/repo'
    try:
        git.Repo.clone_from(repo_url, repo_dir)
    except Exception as e:
        return str(e)
    return "Code fetched successfully."

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)