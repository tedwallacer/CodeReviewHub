from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import git

load_dotenv()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

database = SQLAlchemy(application)

class User(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    password_hash = database.Column(database.String(128), nullable=False)

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@application.route('/')
def home():
    return "Hello, this is the main page of the code management system."

@application.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists!'}), 409

    new_user = User(username=username)
    new_user.set_password_hash(password)
    database.session.add(new_user)
    database.session.commit()

    return jsonify({'message': 'User created successfully!'}), 201

@application.route('/login', methods=['POST'])
def authenticate_user():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        session['user_id'] = user.user_id
        return jsonify({'message': 'Logged in successfully!'}), 200
    return jsonify({'message': 'Invalid username or password!'}), 401

@application.route('/logout')
def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully!'}), 200

@application.route('/submit_code', methods=['POST'])
def submit_code():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to submit code.'}), 401
    return jsonify({'message': 'Code submitted successfully!'}), 202

@application.route('/review_code', methods=['GET', 'POST'])
def initiate_code_review():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to review code.'}), 401
    return jsonify({'message': 'Code review functionality is not implemented yet.'}), 501

def fetch_latest_code_from_git_repository(repo_url):
    repo_directory = '/path/to/your/repo'
    try:
        git.Repo.clone_from(repo_url, repo_directory)
    except Exception as e:
        return str(e)
    return "Code fetched successfully."

if __name__ == '__main__':
    database.create_all()
    application.run(debug=True)