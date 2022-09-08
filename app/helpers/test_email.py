from flask import render_template, current_app
from app.helpers.email import send_email

def send_cluster_email(template, message, name, url, time, app, sender, to):
    html = render_template(template_name_or_list=template, name=name, url=url, time=time)
    send_email(to, message, html, sender, app)
