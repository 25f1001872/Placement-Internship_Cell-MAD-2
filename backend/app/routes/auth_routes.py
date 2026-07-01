from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from app.models.user import User
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403

    if user.role == 'company':
        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        if company.approval_status == 'Pending':
            return jsonify({'error': 'Account pending admin approval'}), 403
        if company.is_blacklisted:
            return jsonify({'error': 'Account is blacklisted'}), 403

    if user.role == 'student':
        student = StudentProfile.query.filter_by(user_id=user.id).first()
        if student and student.is_blacklisted:
            return jsonify({'error': 'Account is blacklisted'}), 403

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'token': access_token, 'role': user.role, 'name': user.name}), 200

@auth_bp.route('/api/auth/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    education = data.get('education')
    skills = data.get('skills')
    experience = data.get('experience')
    contact = data.get('contact')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    new_user = User(name=name, email=email, password_hash=generate_password_hash(password), role='student')
    db.session.add(new_user)
    db.session.commit()

    new_student = StudentProfile(user_id=new_user.id, education=education, skills=skills, experience=experience, contact=contact)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Registration successful. Please login.'}), 201

@auth_bp.route('/api/auth/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    company_description = data.get('company_description')
    industry = data.get('industry')
    location = data.get('location')
    website = data.get('website')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    new_user = User(name=name, email=email, password_hash=generate_password_hash(password), role='company')
    db.session.add(new_user)
    db.session.commit()

    new_company = CompanyProfile(user_id=new_user.id, company_description=company_description, industry=industry, location=location, website=website, approval_status='Pending')
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Registered successfully. Pending admin approval.'}), 201

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200