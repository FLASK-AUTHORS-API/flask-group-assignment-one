from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
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

    #get all companies
    @companies.get('/')
    @jwt_required()
    def getAllCompanies():


        try:

            all_companies = Company.query.all()

            companies_data = []

            for company in all_companies:
                company_info ={
                    'id':company.id,
                    'name':company.name,
                    'description':company.description,
                    'origin':company.origin,
                    'created_at':company.created_at
                }
                companies_data.append(company_info)

            return jsonify({

                'message': 'All companies retrieved successfully',
                'total_companies': len(companies_data),
                "companies": companies_data

            })



                

                


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
    

    
 