from django.template.loader import render_to_string 
from django.core.mail import EmailMultiAlternatives
from real_estate_backend import settings
from datetime import datetime
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate_backend.settings")
django.setup()

from django.template import loader

def read_html_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()
        return html_content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"Error occurred while reading the file: {e}")
        return None

def update_html(html_message, property=None, user=None, scheduled_date=None, scheduled_time=None, link=None):
    if link:
        html_message = html_message.replace("Link", f"{link}")
    else:
        html_message = html_message.replace("property_id", f"{property.property_id}")
        html_message = html_message.replace('property_name', f"{property.title}")
        html_message = html_message.replace('property_title', f"{property.title}")
        html_message = html_message.replace('property_address', f"{property.location}")
        html_message = html_message.replace('property_price', f"{property.price}")
        html_message = html_message.replace('user_id', f"{user.id}")
        html_message = html_message.replace('user_name', f"{user.first_name}")
        html_message = html_message.replace('user_email', f"{user.email}")
        html_message = html_message.replace('scheduled_date', f"{datetime.strftime(scheduled_date, '%B %d, %Y')}")
        html_message = html_message.replace('scheduled_time', f"{scheduled_time}")
    return html_message

def send_email(user, property, scheduled_date, scheduled_time):
    template_path = ('tours/index.html')
    template_content = render_to_string(template_path)
    html_message = update_html(template_content, property, user, scheduled_date, scheduled_time)

    recipient_email ='dev.maddy.1092@gmail.com'
    subject = 'User request for tour'
    body = 'The form has been submitted.'

    try:
        message = EmailMultiAlternatives(
          subject=subject,
          body=html_message,
          from_email='casa.colombia0011@gmail.com',
          to=[recipient_email, 'fateh.allam@gmail.com']
        )
        message.attach_alternative(html_message, "text/html")        
        message.send()
        return {'status': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def send_email_to_user(recepient_email, template_path=None, subject=None, body=None, link=None):
    template_path = template_path or ('tours/change_password.html')
    template_content = render_to_string(template_path)
    html_message = update_html(html_message=template_content, link=link) if link else template_content
    body = body or 'The form has been submitted.'

    try:
        message = EmailMultiAlternatives(
          subject=subject or "changing password",
          body=html_message,
          from_email='casa.colombia0011@gmail.com',
          to=[recepient_email]
        )
        message.attach_alternative(html_message, "text/html")        
        message.send()
        return {'status': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
