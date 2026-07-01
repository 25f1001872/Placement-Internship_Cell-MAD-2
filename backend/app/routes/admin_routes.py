from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from app.models.placement_drive import PlacementDrive
from app.models.application import Application
from ..extensions import db

admin_bp = Blueprint('admin', __name__)

def admin_required():
    identity = get_jwt_identity()
    if identity['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None

@admin_bp.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    error = admin_required()
    if error:
        return error
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    pending_companies = CompanyProfile.query.filter_by(approval_status='Pending').count()
    pending_drives = PlacementDrive.query.filter_by(approval_status='Pending').count()
    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_drives': total_drives,
        'total_applications': total_applications,
        'pending_companies': pending_companies,
        'pending_drives': pending_drives
    }), 200

@admin_bp.route('/api/admin/companies', methods=['GET'])
@jwt_required()
def get_companies():
    error = admin_required()
    if error:
        return error
    name = request.args.get('name')
    industry = request.args.get('industry')
    query = CompanyProfile.query
    if name:
        query = query.join(User, CompanyProfile.user_id == User.id).filter(User.name.ilike(f'%{name}%'))
    if industry:
        query = query.filter(CompanyProfile.industry.ilike(f'%{industry}%'))
    companies = query.all()
    result = []
    for c in companies:
        user = User.query.get(c.user_id)
        result.append({
            'id': c.id,
            'name': user.name,
            'industry': c.industry,
            'location': c.location,
            'website': c.website,
            'company_description': c.company_description,
            'approval_status': c.approval_status,
            'is_blacklisted': c.is_blacklisted,
            'created_at': c.created_at
        })
    return jsonify(result), 200

@admin_bp.route('/api/admin/companies/<int:id>', methods=['GET'])
@jwt_required()
def get_company(id):
    error = admin_required()
    if error:
        return error
    c = CompanyProfile.query.get(id)
    if not c:
        return jsonify({'error': 'Company not found'}), 404
    user = User.query.get(c.user_id)
    drives = PlacementDrive.query.filter_by(company_id=c.id).all()
    drives_data = [{'id': d.id, 'job_title': d.job_title, 'status': d.status, 'approval_status': d.approval_status, 'deadline': str(d.deadline)} for d in drives]
    return jsonify({
        'id': c.id,
        'name': user.name,
        'email': user.email,
        'industry': c.industry,
        'location': c.location,
        'website': c.website,
        'company_description': c.company_description,
        'approval_status': c.approval_status,
        'is_blacklisted': c.is_blacklisted,
        'created_at': c.created_at,
        'drives': drives_data
    }), 200

@admin_bp.route('/api/admin/companies/<int:id>/approve', methods=['POST'])
@jwt_required()
def approve_company(id):
    error = admin_required()
    if error:
        return error
    c = CompanyProfile.query.get(id)
    if not c:
        return jsonify({'error': 'Company not found'}), 404
    c.approval_status = 'Approved'
    db.session.commit()
    return jsonify({'message': 'Company approved'}), 200

@admin_bp.route('/api/admin/companies/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_company(id):
    error = admin_required()
    if error:
        return error
    c = CompanyProfile.query.get(id)
    if not c:
        return jsonify({'error': 'Company not found'}), 404
    c.approval_status = 'Rejected'
    db.session.commit()
    return jsonify({'message': 'Company rejected'}), 200

@admin_bp.route('/api/admin/companies/<int:id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_company(id):
    error = admin_required()
    if error:
        return error
    c = CompanyProfile.query.get(id)
    if not c:
        return jsonify({'error': 'Company not found'}), 404
    c.is_blacklisted = not c.is_blacklisted
    db.session.commit()
    return jsonify({'message': 'Company blacklist status updated'}), 200

@admin_bp.route('/api/admin/students', methods=['GET'])
@jwt_required()
def get_students():
    error = admin_required()
    if error:
        return error
    name = request.args.get('name')
    student_id = request.args.get('id')
    contact = request.args.get('contact')
    query = StudentProfile.query
    if name:
        query = query.join(User, StudentProfile.user_id == User.id).filter(User.name.ilike(f'%{name}%'))
    if student_id:
        query = query.filter(StudentProfile.id == student_id)
    if contact:
        query = query.filter(StudentProfile.contact.ilike(f'%{contact}%'))
    students = query.all()
    result = []
    for s in students:
        user = User.query.get(s.user_id)
        result.append({
            'id': s.id,
            'name': user.name,
            'email': user.email,
            'education': s.education,
            'skills': s.skills,
            'experience': s.experience,
            'contact': s.contact,
            'is_blacklisted': s.is_blacklisted,
            'created_at': s.created_at
        })
    return jsonify(result), 200

@admin_bp.route('/api/admin/students/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    error = admin_required()
    if error:
        return error
    s = StudentProfile.query.get(id)
    if not s:
        return jsonify({'error': 'Student not found'}), 404
    user = User.query.get(s.user_id)
    applications = Application.query.filter_by(student_id=s.id).all()
    apps_data = [{'id': a.id, 'drive_id': a.drive_id, 'status': a.status, 'applied_at': str(a.applied_at)} for a in applications]
    return jsonify({
        'id': s.id,
        'name': user.name,
        'email': user.email,
        'education': s.education,
        'skills': s.skills,
        'experience': s.experience,
        'contact': s.contact,
        'is_blacklisted': s.is_blacklisted,
        'created_at': s.created_at,
        'applications': apps_data
    }), 200

@admin_bp.route('/api/admin/students/<int:id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_student(id):
    error = admin_required()
    if error:
        return error
    s = StudentProfile.query.get(id)
    if not s:
        return jsonify({'error': 'Student not found'}), 404
    s.is_blacklisted = not s.is_blacklisted
    db.session.commit()
    return jsonify({'message': 'Student blacklist status updated'}), 200

@admin_bp.route('/api/admin/drives', methods=['GET'])
@jwt_required()
def get_drives():
    error = admin_required()
    if error:
        return error
    drives = PlacementDrive.query.all()
    result = []
    for d in drives:
        company = CompanyProfile.query.get(d.company_id)
        company_user = User.query.get(company.user_id)
        result.append({
            'id': d.id,
            'company_id': d.company_id,
            'company_name': company_user.name,
            'job_title': d.job_title,
            'skills_required': d.skills_required,
            'salary': d.salary,
            'deadline': str(d.deadline),
            'status': d.status,
            'approval_status': d.approval_status,
            'created_at': d.created_at
        })
    return jsonify(result), 200

@admin_bp.route('/api/admin/drives/<int:id>', methods=['GET'])
@jwt_required()
def get_drive(id):
    error = admin_required()
    if error:
        return error
    d = PlacementDrive.query.get(id)
    if not d:
        return jsonify({'error': 'Drive not found'}), 404
    company = CompanyProfile.query.get(d.company_id)
    company_user = User.query.get(company.user_id)
    applications = Application.query.filter_by(drive_id=d.id).all()
    apps_data = []
    for a in applications:
        student = StudentProfile.query.get(a.student_id)
        student_user = User.query.get(student.user_id)
        apps_data.append({'id': a.id, 'student_id': a.student_id, 'student_name': student_user.name, 'status': a.status, 'applied_at': str(a.applied_at)})
    return jsonify({
        'id': d.id,
        'company_name': company_user.name,
        'job_title': d.job_title,
        'job_description': d.job_description,
        'skills_required': d.skills_required,
        'eligibility': d.eligibility,
        'salary': d.salary,
        'benefits': d.benefits,
        'deadline': str(d.deadline),
        'status': d.status,
        'approval_status': d.approval_status,
        'created_at': d.created_at,
        'applications': apps_data
    }), 200

@admin_bp.route('/api/admin/drives/<int:id>/approve', methods=['POST'])
@jwt_required()
def approve_drive(id):
    error = admin_required()
    if error:
        return error
    d = PlacementDrive.query.get(id)
    if not d:
        return jsonify({'error': 'Drive not found'}), 404
    d.approval_status = 'Approved'
    db.session.commit()
    return jsonify({'message': 'Drive approved'}), 200

@admin_bp.route('/api/admin/drives/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_drive(id):
    error = admin_required()
    if error:
        return error
    d = PlacementDrive.query.get(id)
    if not d:
        return jsonify({'error': 'Drive not found'}), 404
    d.approval_status = 'Rejected'
    db.session.commit()
    return jsonify({'message': 'Drive rejected'}), 200

@admin_bp.route('/api/admin/drives/<int:id>/close', methods=['POST'])
@jwt_required()
def close_drive(id):
    error = admin_required()
    if error:
        return error
    d = PlacementDrive.query.get(id)
    if not d:
        return jsonify({'error': 'Drive not found'}), 404
    d.status = 'Closed'
    db.session.commit()
    return jsonify({'message': 'Drive closed'}), 200

@admin_bp.route('/api/admin/applications', methods=['GET'])
@jwt_required()
def get_applications():
    error = admin_required()
    if error:
        return error
    applications = Application.query.all()
    result = []
    for a in applications:
        student = StudentProfile.query.get(a.student_id)
        student_user = User.query.get(student.user_id)
        drive = PlacementDrive.query.get(a.drive_id)
        company = CompanyProfile.query.get(drive.company_id)
        company_user = User.query.get(company.user_id)
        result.append({
            'id': a.id,
            'student_name': student_user.name,
            'company_name': company_user.name,
            'job_title': drive.job_title,
            'status': a.status,
            'applied_at': str(a.applied_at)
        })
    return jsonify(result), 200