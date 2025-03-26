from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.users import User
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity, create_refresh_token




#users blueprint
users = Blueprint('users', __name__, url_prefix='/api/v1/users')

# Retrieving all users from the database
@users.get('/')
@jwt_required()
def getAllUsers():
    try:
        all_users = User.query.all()
        users_data = []

        for user in all_users:
            user_info = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.get_full_name(),  # Call the function
                'email': user.email,
                'contact': user.contact,
                'type': user.user_type,
                'created_at': user.created_at
            }
            users_data.append(user_info)  

        return jsonify({
            "message": "All users successfully retrieved.",
            "total_users": len(users_data),
            "users": users_data
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

#Retrieving user by id
@users.get('/user/<int:id>')
@jwt_required()
def getUser(id):
    try:
        user = User.query.filter_by(id=id).first()
        books =[]
        companies = []


        if hasattr(books,'books'):
            books = [{
                    'id': book.id, 'title': book.title, 'price':book.price, 'genre': book.genre, 'price_unit': book.price_unit,
                    'publication_date': book.publication_date, 'description':book.description, 'image': book.image, 'created_at':book.created_at} for book in user.books]
            
        if hasattr(companies,'companies'):
            companies = [{
                    'id':company.id, 'name':company.name, 'origin':company.origin} for company in user.companies]
            
        return jsonify({
            "message": "User details successfully retrieved.",
            "user":{
                   'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.get_full_name(), 
                'email': user.email,
                'contact': user.contact,
                'type': user.user_type,
                'biography':user.biography,
                'created_at': user.created_at,
                'companies':companies,
                'books': books

            }
            })

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR



#retrieving all authors from the database

@users.get('/authors')
@jwt_required()
def getAllAuthors():
    try:
        all_authors = User.query.filter_by(user_type='author').all()
        authors_data = []

        for author in all_authors:
            author_info = {
                'id': author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username': author.get_full_name(),  
                'email':author.email,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies':[],
                'books': []
            }

            if hasattr(author,'books'):
                author_info['books'] = [{
                    'id': book.id, 'title': book.title, 'price':book.price, 'genre': book.genre, 'price_unit': book.price_unit,
                    'publication_date': book.publication_date, 'description':book.description, 'image': book.image, 'created_at':book.created_at} for book in author.books]
            
            if hasattr(author,'companies'):
                author_info['companies'] = [{
                    'id':company.id, 'name':company.name, 'origin':company.origin} for company in author.companies]
            authors_data.append(author_info)  

        return jsonify({
            "message": "All authors successfully retrieved.",
            "total_authors": len(authors_data),
            "authors": authors_data
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
#Retrieving author by id

@users.get('/author/<int:id>')
@jwt_required()
def getAuthor(id):
    try:
        author = User.query.filter_by(id=id).first()
        books =[]
        companies = []


        if hasattr(books,'books'):
            books = [{
                    'id': book.id, 'title': book.title, 'price':book.price, 'genre': book.genre, 'price_unit': book.price_unit,
                    'publication_date': book.publication_date, 'description':book.description, 'image': book.image, 'created_at':book.created_at} for book in author.books]
            
        if hasattr(companies,'companies'):
            companies = [{
                    'id':company.id, 'name':company.name, 'origin':company.origin} for company in author.companies]
            
        return jsonify({
            "message": "Author details successfully retrieved.",
            "author":{
            'id': author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username': author.get_full_name(),  
                'email':author.email,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies':[],
                'books': []

            }
            })

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR