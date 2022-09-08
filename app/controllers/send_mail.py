import os
from wsgiref import headers
import requests
from flask import current_app
from flask_restful import Resource, request
from app.helpers.test_email import send_cluster_email
from datetime import datetime

class SendMail(Resource):
    def get(self):
        try:
            template = "downStatus.html"
            subject = "Cluster Down"
            vm = "PVE1"
            proxmox_url = os.getenv("PROXMOX_URL")
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            app = current_app._get_current_object()
            sender = os.getenv("APP_MAIL_USERNAME")
            receiver = os.getenv("APP_MAIL_USERNAME")
            send_cluster_email(template, subject, vm, proxmox_url, time, app, sender,receiver)
            return dict(status='success', message='Success'), 200
        except Exception as e:
            print(e)

            return dict(status='fail', message='Internal Server Error'), 500