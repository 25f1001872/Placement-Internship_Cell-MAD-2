from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from app.models.company import CompanyProfile
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from app.models.student import StudentProfile
from app.models.user import User
from ..extensions import db

from app.models.placement import Placement
from app.utils.cache import delete_pattern

company_bp = Blueprint('company', __name__)

def get_company_profile():
    identity = get_jwt_identity()
    return CompanyProfile.query.filter_by(user_id=int(identity)).first()

@company_bp.route('/api/company/dashboard', methods=['GET'])
@jwt_required()
def company_dashboard():
    company = get_company_profile()
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    if company.is_blacklisted:
        return jsonify({'error': 'Your company has been blacklisted by admin'}), 403
    user = User.query.get(company.user_id)
    upcoming_drives = PlacementDrive.query.filter_by(company_id=company.id, status='Active').all()
    closed_drives = PlacementDrive.query.filter_by(company_id=company.id, status='Closed').all()
    def drive_data(d):
        return {'id': d.id, 'job_title': d.job_title, 'deadline': str(d.deadline), 'status': d.status, 'approval_status': d.approval_status}
    return jsonify({
        'company_name': user.name,
        'upcoming_drives': [drive_data(d) for d in upcoming_drives],
        'closed_drives': [drive_data(d) for d in closed_drives]
    }), 200

@company_bp.route('/api/company/drives', methods=['POST'])
@jwt_required()
def create_drive():
    company = get_company_profile()
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    if company.is_blacklisted:
        return jsonify({'error': 'Your company has been blacklisted by admin'}), 403
    data = request.get_json()
    deadline = None
    if data.get('deadline'):
        deadline = datetime.strptime(data['deadline'], "%Y-%m-%d").date()
    new_drive = PlacementDrive(
        company_id=company.id,
        job_title=data.get('job_title'),
        job_description=data.get('job_description'),
        eligibility=data.get('eligibility'),
        deadline=deadline,
        skills_required=data.get('skills_required'),
        salary=data.get('salary'),
        benefits=data.get('benefits')
    )
    db.session.add(new_drive)
    db.session.commit()
    delete_pattern("drives:*")
    return jsonify({'message': 'Drive created successfully, pending admin approval'}), 201

@company_bp.route('/api/company/drives/<int:drive_id>/close', methods=['POST'])
@jwt_required()
def close_drive(drive_id):
    company = get_company_profile()
    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.company_id != company.id:
        return jsonify({'error': 'Not found or unauthorized'}), 403
    drive.status = 'Closed'
    db.session.commit()
    return jsonify({'message': 'Drive closed'}), 200

@company_bp.route('/api/company/drives/<int:drive_id>/applications', methods=['GET'])
@jwt_required()
def drive_applications(drive_id):
    company = get_company_profile()
    drive = PlacementDrive.query.get(drive_id)
    if not drive or drive.company_id != company.id:
        return jsonify({'error': 'Not found or unauthorized'}), 403
    applications = Application.query.filter_by(drive_id=drive_id).all()
    result = []
    for a in applications:
        student = StudentProfile.query.get(a.student_id)
        student_user = User.query.get(student.user_id)
        result.append({'id': a.id, 'student_id': a.student_id, 'student_name': student_user.name, 'status': a.status, 'applied_at': str(a.applied_at)})
    return jsonify({'drive': {'id': drive.id, 'job_title': drive.job_title}, 'applications': result}), 200

@company_bp.route('/api/company/applications/<int:application_id>', methods=['GET'])
@jwt_required()
def student_application(application_id):
    company = get_company_profile()
    application = Application.query.get(application_id)
    drive = PlacementDrive.query.get(application.drive_id)
    if drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    student = StudentProfile.query.get(application.student_id)
    student_user = User.query.get(student.user_id)
    return jsonify({
        'application_id': application.id,
        'status': application.status,
        'applied_at': str(application.applied_at),
        'student_name': student_user.name,
        'student_email': student_user.email,
        'education': student.education,
        'skills': student.skills,
        'experience': student.experience,
        'contact': student.contact,
        'drive_title': drive.job_title
    }), 200

@company_bp.route('/api/company/applications/<int:application_id>/status', methods=['POST'])
@jwt_required()
def update_application_status(application_id):
    company = get_company_profile()
    application = Application.query.get(application_id)
    drive = PlacementDrive.query.get(application.drive_id)
    if drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ['Applied', 'Shortlisted', 'Interview', 'Offer', 'Rejected', 'Placed']:
        return jsonify({'error': 'Invalid status'}), 400
    application.status = new_status
    if new_status == 'Placed':
        from app.models.placement import Placement
        existing_placement = Placement.query.filter_by(student_id=application.student_id, drive_id=application.drive_id).first()
        if not existing_placement:
            new_placement = Placement(
                student_id=application.student_id,
                company_id=drive.company_id,
                drive_id=application.drive_id,
                salary=drive.salary
            )
            db.session.add(new_placement)
    db.session.commit()
    return jsonify({'message': 'Status updated'}), 200

@company_bp.route('/api/company/students/<int:student_id>', methods=['GET'])
@jwt_required()
def view_student(student_id):
    company = get_company_profile()
    student = StudentProfile.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    user = User.query.get(student.user_id)
    applications = Application.query.filter_by(student_id=student.id).all()
    apps_data = []
    for a in applications:
        drive = PlacementDrive.query.get(a.drive_id)
        if drive.company_id == company.id:
            apps_data.append({'drive_id': a.drive_id, 'job_title': drive.job_title, 'status': a.status, 'applied_at': str(a.applied_at)})
    return jsonify({
        'name': user.name,
        'education': student.education,
        'skills': student.skills,
        'experience': student.experience,
        'contact': student.contact,
        'applications': apps_data
    }), 200