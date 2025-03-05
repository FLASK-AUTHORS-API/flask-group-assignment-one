from app.extensions import db, bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

# users blueprint
users = Blueprint('users', __name__, url_prefix='api/users')

# User model 
from app.models import User, Author, Book, Company

# getting all users from database
@users.get('/users')
@jwt_required()
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# getting all authors endpoint
@users.get('/authors')
@jwt_required()
def get_all_authors():
    authors = Author.query.all()
    return jsonify([author.to_dict() for author in authors])

# getting all books endpoint
@users.get('/books')
@jwt_required()
def get_all_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# getting all companies endpoint
@users.get('/companies')
@jwt_required()
def get_all_companies():
    companies = Company.query.all()
    return jsonify([company.to_dict() for company in companies])

# create a new user
@users.post('/users')
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

