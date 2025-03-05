from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_403_FORBIDDEN,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_404_NOT_FOUND,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.companies import Company
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity, create_refresh_token




#company blueprint
companies = Blueprint('companies', __name__, url_prefix='/api/v1/companies')

#creating companies

@companies.route('/create', methods=['POST'])
@jwt_required(get_jwt_identity)
def createCompany():
    data = request.json
    origin= data.get('origin')
    description = data.get('description')
    user_id = data.get('user_id')
    name = data.get('name')
    


    #validations of the incoming request

    if not name or not origin or not description:
        return jsonify({"error":"All fields are required"}),HTTP_400_BAD_REQUEST
    

    if Company.query.filter_by(name=name).first() is not None:
        return jsonify({"error":"Company name already exists."}),HTTP_409_CONFLICT
    
    
    try:
      

       #creating a new company
       new_company = Company(name=name,origin = origin, description=description, user_id=user_id)
       db.session.add(new_company)
       db.session.commit()



       return jsonify({
           'message': name + " has been successfully created as an " + new_company.user_type,
           'user':{
               'id':new_company.id,
               "name":new_company.name,
               "origin":new_company.origin,
               "description": new_company.description
              
           }
       }),HTTP_201_CREATED

    except Exception as e:   
        db.session.rollback() 
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

 # delete a company
@companies.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteCompany(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = user.query.filter_by(id=current_user).first()
        # get company by id
        company = Company.query.filter_by(id=id).first()
        if not company:
            return jsonify({"error": "Company not found"}), 404
        elif loggedInUser.user_type != 'admin' and company.user_id == current_user:
            return jsonify({"error": "You are not authorized to delete this"}), 403
        else:
            # delete associated books
            for book in company.books:
                db.session.delete(book)
            db.session.delete(company)
            db.session.commit()
            return jsonify({'message': "Company deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
