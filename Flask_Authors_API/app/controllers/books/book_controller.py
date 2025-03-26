from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
import validators
from app.models.companies import Company
from app.models.books import Book
from app.models.users import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity, create_refresh_token



#books blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')

#creating a book
@books.route('/create', methods=['POST'])
@jwt_required()
def createBook():
    #storing request data
    data = request.get_json() 
    title= data.get('title')
    pages= data.get('pages')
    price = data.get('price')
    price_unit = data.get('price_unit')
    description = data.get('description')
    genre= data.get('genre')
    isbn= data.get('isbn')
    publication_date = data.get('publication_date')
    image = data.get('image')
    company_id = data.get('company_id')
    user_id = get_jwt_identity()
  


    #validations of the incoming request

    if not title or not pages or not  price or not price_unit or not description or not genre or not isbn or not publication_date or not company_id :
      return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    

    if Book.query.filter_by(title=title, user_id =user_id).first() is not None:
        return jsonify({"error":"Book with this title and user id already exists."}),HTTP_409_CONFLICT
    
    if Book.query.filter_by(isbn=isbn).first() is not None:
        return jsonify({"error":"Book isbn already in use."}),HTTP_409_CONFLICT
    
    
    try:
       #creating a new book
       new_book = Book(title = title, price = price, description = description, pages = pages, 
                       user_id = user_id,company_id = company_id, price_unit = price_unit, genre = genre, 
                       publication_date = publication_date, isbn = isbn,image = image)

       db.session.add(new_book)
       db.session.commit()

       return jsonify({
           'message': title + " has been successfully created.",
           'book':{
           'id':new_book.id,
            "title":new_book.title,
            'pages':new_book.pages,
            'price': new_book.price,
            'price_unit': new_book.price_unit,
            'description':new_book.description,
            'genre':new_book.genre,
            'isbn':new_book.isbn,
            'publication_date': new_book.publication_date,
            'image': new_book.image,
            'created_at': new_book.created_at,  
            'company':{
              'id':new_book.company.id,
               "name":new_book.company.name,
               "origin":new_book.company.origin,
               "description": new_book.company.description,
               "created_at": new_book.company.created_at
            },
            'author':{
                'first_name': new_book.user.first_name,
                'last_name': new_book.user.last_name,
                'username': new_book.user.get_full_name(),  
                'email':new_book.user.email,
                'contact': new_book.user.contact,
                'type': new_book.user.user_type,
                'biography': new_book.user.biography,
                'created_at': new_book.user.created_at
            }
           }
       }),HTTP_201_CREATED
   
    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR


# Get all books from the database
@books.get('/')
def getAllBooks():
    try:
        all_books = Book.query.all()
        books_data = []

        for book in all_books:
            books_info = {
            'id':book.id,
            "title":book.title,
            'pages':book.pages,
            'price': book.price,
            'price_unit': book.price_unit,
            'description':book.description,
            'genre':book.genre,
            'isbn':book.isbn,
            'publication_date': book.publication_date,
            'image': book.image,
            'created_at': book.created_at,  
            'company':{
              'id':book.company.id,
               "name":book.company.name,
               "origin":book.company.origin,
               "description": book.company.description,
               "created_at": book.company.created_at
            },
              
            }
            books_data.append(books_info)  

        return jsonify({
            "message": "All Books successfully retrieved.",
            "total_books": len(books_data),
            "books": books_data
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# #Get book by id
@books.get('/book/<int:id>')
@jwt_required()
def getBook(id):
    try:
         book = Book.query.filter_by(id=id).first()

         if not book:
            return jsonify({"error": 'Book not found.'}), HTTP_404_NOT_FOUND
        
         return jsonify({
            "message": 'Book details successfully retrieved.',
            "book":{
            'id':book.id,
            "title":book.title,
            'pages':book.pages,
            'price': book.price,
            'price_unit': book.price_unit,
            'description':book.description,
            'genre':book.genre,
            'isbn':book.isbn,
            'publication_date': book.publication_date,
            'image': book.image,
            'created_at': book.created_at,  
            'company':{
              'id':book.company.id,
               "name":book.company.name,
               "origin":book.company.origin,
               "description": book.company.description,
               "created_at": book.company.created_at
            },
            }
            }), HTTP_200_OK
    
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# # Update Book details
@books.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def updateBookDetails(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

        # Get book by ID
        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({'error': 'Company not found.'}), HTTP_404_NOT_FOUND
        elif loggedInUser.user_type != 'admin' and book.user_id != current_user:
            return jsonify({'error': 'You are not authorized to update the book details.'}), HTTP_403_FORBIDDEN

        # Store the request data
        data = request.get_json()
        title = data.get('title', book.title)
        price = data.get('price', book.price)
        price_unit = data.get('price_unit', book.price_unit)
        description = data.get('description', book.description)
        genre = data.get('genre', book.genre)
        isbn = data.get('isbn', book.isbn)
        pages = data.get('pages', book.pages)
        publication_date = data.get('publication_date', book.publication_date)
        company_id = data.get('company_id', book.company_id)
        image = data.get('image', book.image)

     
        if isbn != book.isbn and Book.query.filter_by(isbn=isbn).first():
          return jsonify({"error":"Book ISBN already in use."}),HTTP_409_CONFLICT
    
        if title != book.title and Book.query.filter_by(title=title, user_id = current_user).first():
          return jsonify({"error":"Book Title already exists."}),HTTP_409_CONFLICT
       

        # Update book details
        book.title = title
        book.price = price
        book.price_unit = price_unit
        book.description = description
        book.genre = genre
        book.isbn = isbn
        book.pages = pages
        book.publication_date = publication_date
        book.company_id = company_id
        book.image = image
       

        db.session.commit()

        return jsonify({
            'message': f"{title}'s details have been successfully updated.",
            'book': {
            'id':book.id,
            "title":book.title,
            'pages':book.pages,
            'price': book.price,
            'price_unit': book.price_unit,
            'description':book.description,
            'genre':book.genre,
            'isbn':book.isbn,
            'publication_date': book.publication_date,
            'image': book.image,
            'created_at': book.created_at,  
            'company':{
              'id':book.company.id,
               "name":book.company.name,
               "origin":book.company.origin,
               "description": book.company.description,
               "created_at": book.company.created_at
            }
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# #delete a book
@books.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteBook(id):
   try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

        # Get book by ID
        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({'error': 'Book not found.'}), HTTP_404_NOT_FOUND
        elif loggedInUser.user_type != 'admin' and book.user_id != current_user:
            return jsonify({'error': 'You are not authorized to delete this book\'s details.'}), HTTP_403_FORBIDDEN
        else:
      
           db.session.delete(book)
           db.session.commit()


        return jsonify({
            'message': 'Book has been successfully deleted'
        })

   except Exception as e:
      return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
