from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import git
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def home():
    return "Hello, this is the main page of the code management system."

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not (username and password):
            return jsonify({'error': 'Username and password are required!'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists!'}), 409

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred, please try again later.'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return jsonify({'message': 'Logged in successfully!'}), 200
        
        return jsonify({'error': 'Invalid username or password!'}), 401
    except SQLAlchemyError:
        return jsonify({'error': 'An error occurred, please try again later.'}), 500

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        return jsonify({'message': 'Logged out successfully!'}), 200
    else:
        return jsonify({'error': 'No active session found.'}), 400

@app.route('/submit_code', methods=['POST'])
def submit_code():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login to submit code.'}), 401
    # Assuming code submission logic goes here
    return jsonify({'message': 'Code submitted successfully!'}), 202

@app.route('/review_code', methods=['GET', 'POST'])
def review_code():
    if 'user_id' not in session:
        return jsonify({'error': 'Please login to review code.'}), 401
    # Assuming code review logic goes here
    return jsonify({'error': 'Code review functionality is not implemented yet.'}), 501

def fetch_latest_code_from_git_repository(repo_url):
    repo_directory = '/path/to/your/repo'
    try:
        git.Repo.clone_from(repo_url, repo_directory)
    except git.exc.GitError as e: # Catch git-specific errors
        return str(e)
    except Exception as e: # Catch all other exceptions
        return f"An error occurred: {str(e)}"
    return "Code fetched successfully."

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)