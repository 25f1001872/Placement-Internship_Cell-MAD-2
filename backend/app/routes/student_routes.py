from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.user import User
from ..extensions import db

from app.utils.cache import get_cache, set_cache

student_bp = Blueprint('student', __name__)

def get_student_profile():
    identity = get_jwt_identity()
    return StudentProfile.query.filter_by(user_id=int(identity)).first()

@student_bp.route('/api/student/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    student = get_student_profile()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    if student.is_blacklisted:
        return jsonify({'error': 'Your profile has been blacklisted by admin'}), 403
    user = User.query.get(student.user_id)
    companies = CompanyProfile.query.filter_by(approval_status='Approved', is_blacklisted=False).all()
    applied_drives = Application.query.filter_by(student_id=student.id).all()
    companies_data = []
    for c in companies:
        company_user = User.query.get(c.user_id)
        companies_data.append({'id': c.id, 'name': company_user.name, 'industry': c.industry, 'location': c.location})
    applied_data = []
    for a in applied_drives:
        drive = PlacementDrive.query.get(a.drive_id)
        applied_data.append({'id': a.id, 'drive_id': a.drive_id, 'job_title': drive.job_title, 'status': a.status, 'applied_at': str(a.applied_at)})
    return jsonify({
        'student_name': user.name,
        'companies': companies_data,
        'applied_drives': applied_data
    }), 200

@student_bp.route('/api/student/drives', methods=['GET'])
@jwt_required()
def get_drives():
    company = request.args.get('company')
    position = request.args.get('position')
    skills = request.args.get('skills')
    cache_key = f"drives:{company}:{position}:{skills}"
    cached = get_cache(cache_key)
    if cached:
        return jsonify(cached), 200
    query = PlacementDrive.query.filter_by(approval_status='Approved', status='Active')
    if position:
        query = query.filter(PlacementDrive.job_title.ilike(f'%{position}%'))
    if skills:
        query = query.filter(PlacementDrive.skills_required.ilike(f'%{skills}%'))
    drives = query.all()
    result = []
    for d in drives:
        company_profile = CompanyProfile.query.get(d.company_id)
        company_user = User.query.get(company_profile.user_id)
        if company and company.lower() not in company_user.name.lower():
            continue
        result.append({
            'id': d.id,
            'company_name': company_user.name,
            'job_title': d.job_title,
            'skills_required': d.skills_required,
            'salary': d.salary,
            'deadline': str(d.deadline),
            'status': d.status
        })
    set_cache(cache_key, result, ttl=300)
    return jsonify(result), 200

@student_bp.route('/api/student/drives/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_drive(drive_id):
    student = get_student_profile()
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({'error': 'Drive not found'}), 404
    company = CompanyProfile.query.get(drive.company_id)
    company_user = User.query.get(company.user_id)
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    return jsonify({
        'id': drive.id,
        'company_name': company_user.name,
        'job_title': drive.job_title,
        'job_description': drive.job_description,
        'skills_required': drive.skills_required,
        'eligibility': drive.eligibility,
        'salary': drive.salary,
        'benefits': drive.benefits,
        'deadline': str(drive.deadline),
        'status': drive.status,
        'already_applied': existing is not None
    }), 200

@student_bp.route('/api/student/drives/<int:drive_id>/apply', methods=['POST'])
@jwt_required()
def apply(drive_id):
    student = get_student_profile()
    if student.is_blacklisted:
        return jsonify({'error': 'Your profile has been blacklisted'}), 403
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({'error': 'You have already applied to this drive'}), 409
    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.status != 'Active':
        return jsonify({'error': 'Drive is not active'}), 400
    new_application = Application(student_id=student.id, drive_id=drive_id)
    db.session.add(new_application)
    db.session.commit()
    return jsonify({'message': 'Application submitted successfully'}), 201

@student_bp.route('/api/student/applications', methods=['GET'])
@jwt_required()
def applications_history():
    student = get_student_profile()
    applications = Application.query.filter_by(student_id=student.id).all()
    result = []
    for a in applications:
        drive = PlacementDrive.query.get(a.drive_id)
        company = CompanyProfile.query.get(drive.company_id)
        company_user = User.query.get(company.user_id)
        result.append({
            'id': a.id,
            'drive_id': a.drive_id,
            'job_title': drive.job_title,
            'company_name': company_user.name,
            'status': a.status,
            'applied_at': str(a.applied_at)
        })
    return jsonify(result), 200

@student_bp.route('/api/student/profile', methods=['GET'])
@jwt_required()
def get_profile():
    student = get_student_profile()
    user = User.query.get(student.user_id)
    return jsonify({
        'name': user.name,
        'email': user.email,
        'education': student.education,
        'skills': student.skills,
        'experience': student.experience,
        'contact': student.contact
    }), 200

@student_bp.route('/api/student/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    student = get_student_profile()
    data = request.get_json()
    student.education = data.get('education', student.education)
    student.skills = data.get('skills', student.skills)
    student.experience = data.get('experience', student.experience)
    student.contact = data.get('contact', student.contact)
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200