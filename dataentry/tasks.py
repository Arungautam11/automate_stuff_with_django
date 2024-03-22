from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import generate_csv_file, send_email_notification
from django.conf import settings


@app.task
def celery_test_task():
    time.sleep(5) # simulation of any tasks that's going to take 10 second

    # Send an email
    mail_subject = 'This is test subject'
    message = 'This is test mail'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return 'Email sent succesfully.'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    # Notify the user by email.
    mail_subject = 'Import Data completed.'
    message = 'Your data import has been successful.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email])
    return 'Data imported successfully.'


@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    
    file_path = generate_csv_file(model_name)
    
    # Send email with the attachment
    mail_subject = 'Export Data Completed.'
    message = 'Export data has been successful. Please find the attachement below.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email], attachment=file_path)
    return 'Export data task exported successfully.'