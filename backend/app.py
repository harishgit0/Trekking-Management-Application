from flask import Flask, request, jsonify
from application.config import Config
from application.database import db
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt
from datetime import datetime

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

jwt = JWTManager(app)


# ---------------------------APIs Construction------------------------------------

@app.route("/register",methods=["POST"])
def register_api():
    data=request.get_json()
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    full_name=data.get("full_name")
    phone=data.get("phone")
    age=data.get("age")
    gender=data.get("gender")
    address=data.get("address")


    if not username or not email or not password:
        return jsonify({"message":"All fields are required"}),400
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({
            "message":"Username already exists"
        }),400
    
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return jsonify({
            "message":"Email already exists"
        }),400
    
    hashed_password = generate_password_hash(password)
    

    if not all([full_name,phone,age,gender,address]):
        return jsonify({
            "message":"All fields are required for profile"
        }),400
    
    user=User(username=username,email=email,password=hashed_password,role="trekker")
    db.session.add(user)
    db.session.flush()  # gets user.id without committing
    
    user_profile=UserProfile(user_id=user.id,full_name=full_name,phone=phone,age=age,gender=gender,address=address)
    db.session.add(user_profile)
    db.session.commit()


    
    return jsonify({"message":"User registered successfully"}),201




@app.route("/login",methods=["POST"])
def login_api():
    data= request.get_json()

    if not data:
        return jsonify({
            "message":"No data provided"
    }),400
    username=data.get("username")
    password=data.get("password")

    if not username or not password:
        return jsonify({"message":"All fields are required"}),400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message":"User not found"}),404

    if not check_password_hash(user.password,password):
        return jsonify({"message":"Invalid password"}),401
    

    access_token = create_access_token(identity=str(user.id),additional_claims={"role": user.role})

    return jsonify({"message":"Login successful",
                    "token":access_token,
                    "user":{
                    "username":user.username,
                    "email":user.email,
                    "role":user.role}}),200


@app.route("/logout",methods=["POST"])
@jwt_required()
def logout_api():
    return jsonify({"message":"Logout successful"}),200


# -----------------------------------------------Admin APIs-----------------------------------------------------

@app.route("/admin/create_trek",methods=["POST"])
@jwt_required()
def create_trek_api():
    claim=get_jwt()
    if claim["role"]!="admin":
        return jsonify({"message":"Access denied"}),403
    
    data=request.get_json()

    if not data:
        return jsonify({"message":"No data provided"}),400
    
    trek_name=data.get("trek_name")
    location=data.get("location")
    description=data.get("description")
    difficulty=data.get("difficulty")
    duration_days=data.get("duration_days")
    total_slots=data.get("total_slots")
    start_date = data.get("start_date")
    end_date = data.get("end_date")


    if not trek_name or not location or not description or not difficulty or not duration_days or not total_slots or not start_date or not end_date:
        return jsonify({"message":"All fields are required"}),400
    
    start_date = datetime.strptime(data.get("start_date"),"%d-%m-%Y").date()

    end_date = datetime.strptime(data.get("end_date"),"%d-%m-%Y").date()

    
    if start_date > end_date:
        return jsonify({
            "message":"Start date cannot be after end date"
        }),400
    if duration_days <= 0:
        return jsonify({
            "message":"Duration must be greater than 0"
        }),400

    if total_slots <= 0:
        return jsonify({
            "message":"Total slots must be greater than 0"
        }),400

    available_slots=total_slots

    trek=Trek(trek_name=trek_name,location=location,description=description,difficulty=difficulty,duration_days=duration_days,total_slots=total_slots,available_slots=available_slots,start_date=start_date,end_date=end_date)
    db.session.add(trek)
    db.session.commit()

    return jsonify({"message":"Trek created successfully","trek_id":trek.id}),201


@app.route("/admin/delete_trek/<int:trek_id>",methods=["DELETE"])
@jwt_required()
def delete_trek_api(trek_id):
    claim=get_jwt()
    if claim["role"]!="admin":
        return jsonify({"message":"Access denied"}),403
    
    trek=Trek.query.get(trek_id)

    if not trek:
        return jsonify({"message":"Trek not found"}),404

    db.session.delete(trek)
    db.session.commit()

    return jsonify({"message":"Trek deleted successfully"}),200
# ---------------------------------------------------------------------------------------------------------





with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),   
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)