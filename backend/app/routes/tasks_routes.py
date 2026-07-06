from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.student import StudentProfile
from app.models.company import CompanyProfile
from app.tasks.jobs import send_interview_reminders, generate_monthly_report, export_student_csv, export_company_csv

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks/send-reminders', methods=['POST'])
@jwt_required()
def trigger_reminders():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    task = send_interview_reminders.delay()
    return jsonify({'message': 'Interview reminders triggered', 'task_id': task.id}), 202

@tasks_bp.route('/api/tasks/monthly-report', methods=['POST'])
@jwt_required()
def trigger_monthly_report():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    task = generate_monthly_report.delay()
    return jsonify({'message': 'Monthly report generation triggered', 'task_id': task.id}), 202

@tasks_bp.route('/api/tasks/export/student', methods=['GET'])
@jwt_required()
def export_student():
    identity = get_jwt_identity()
    student = StudentProfile.query.filter_by(user_id=int(identity)).first()
    task = export_student_csv.delay(student.id)
    result = task.get(timeout=30)
    return Response(
        result['csv'],
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=applications_{result["student_name"]}.csv'}
    )

@tasks_bp.route('/api/tasks/export/company', methods=['GET'])
@jwt_required()
def export_company():
    identity = get_jwt_identity()
    company = CompanyProfile.query.filter_by(user_id=int(identity)).first()
    task = export_company_csv.delay(company.id)
    result = task.get(timeout=30)
    return Response(
        result['csv'],
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=applications_{result["company_name"]}.csv'}
    )

@tasks_bp.route('/api/tasks/status/<task_id>', methods=['GET'])
@jwt_required()
def task_status(task_id):
    from app.extensions import celery
    task = celery.AsyncResult(task_id)
    return jsonify({'task_id': task_id, 'status': task.status}), 200