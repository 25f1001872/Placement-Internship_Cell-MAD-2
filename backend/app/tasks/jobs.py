from app.extensions import celery, mail
from app.models.application import Application
from app.models.student import StudentProfile
from app.models.user import User
from app.models.placement_drive import PlacementDrive
from app.models.company import CompanyProfile
from app.models.placement import Placement
from app.extensions import db
from flask_mail import Message
from datetime import datetime
import csv
import io

@celery.task
def send_interview_reminders():
    applications = Application.query.filter_by(status='Interview').all()
    for a in applications:
        student = StudentProfile.query.get(a.student_id)
        user = User.query.get(student.user_id)
        drive = PlacementDrive.query.get(a.drive_id)
        msg = Message(
            subject="Interview Reminder - Placement Portal",
            recipients=[user.email],
            body=f"Dear {user.name},\n\nThis is a reminder that you have an interview scheduled for {drive.job_title}.\n\nBest of luck!\nPlacement Portal Team"
        )
        mail.send(msg)
    return f"Reminders sent to {len(applications)} students"

@celery.task
def generate_monthly_report():
    companies = CompanyProfile.query.filter_by(approval_status='Approved').all()
    reports = []
    for c in companies:
        user = User.query.get(c.user_id)
        drives = PlacementDrive.query.filter_by(company_id=c.id).all()
        total_applications = 0
        total_placed = 0
        for d in drives:
            apps = Application.query.filter_by(drive_id=d.id).all()
            total_applications += len(apps)
            total_placed += len([a for a in apps if a.status == 'Placed'])
        report_html = f"""
        <h2>Monthly Placement Report - {user.name}</h2>
        <p>Generated: {datetime.utcnow().strftime('%Y-%m-%d')}</p>
        <p>Total Drives: {len(drives)}</p>
        <p>Total Applications: {total_applications}</p>
        <p>Total Placed: {total_placed}</p>
        """
        msg = Message(
            subject=f"Monthly Placement Report - {user.name}",
            recipients=[user.email],
            html=report_html
        )
        mail.send(msg)
        reports.append(user.name)
    return f"Reports sent to {len(reports)} companies"

@celery.task
def export_student_csv(student_id):
    student = StudentProfile.query.get(student_id)
    user = User.query.get(student.user_id)
    applications = Application.query.filter_by(student_id=student_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Drive ID', 'Job Title', 'Company', 'Status', 'Applied At'])
    for a in applications:
        drive = PlacementDrive.query.get(a.drive_id)
        company = CompanyProfile.query.get(drive.company_id)
        company_user = User.query.get(company.user_id)
        writer.writerow([a.drive_id, drive.job_title, company_user.name, a.status, a.applied_at])
    return {'csv': output.getvalue(), 'student_name': user.name}

@celery.task
def export_company_csv(company_id):
    company = CompanyProfile.query.get(company_id)
    user = User.query.get(company.user_id)
    drives = PlacementDrive.query.filter_by(company_id=company_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Drive ID', 'Job Title', 'Student', 'Status', 'Applied At'])
    for d in drives:
        applications = Application.query.filter_by(drive_id=d.id).all()
        for a in applications:
            student = StudentProfile.query.get(a.student_id)
            student_user = User.query.get(student.user_id)
            writer.writerow([d.id, d.job_title, student_user.name, a.status, a.applied_at])
    return {'csv': output.getvalue(), 'company_name': user.name}