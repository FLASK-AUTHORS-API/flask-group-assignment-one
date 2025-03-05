from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(50), nullable=False, default='UGX')
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=False, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    
    # Add the user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey to users table
    
    # Define relationships
    user = db.relationship('User', backref='books')  # Relationship with User model
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('Company', backref='books')  # Relationship with Company model

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, title, price, description, pages, user_id, company_id, price_unit, genre, publication_date, isbn=None, image=None):
        super(Book, self).__init__()
        self.title = title
        self.price = price
        self.description = description
        self.user_id = user_id  # Initialize user_id
        self.pages = pages
        self.price_unit = price_unit
        self.isbn = isbn
        self.publication_date = publication_date
        self.image = image
        self.genre = genre
        self.company_id = company_id

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
