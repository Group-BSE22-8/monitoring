import os
from wsgiref import headers
import requests
from flask_restful import Resource, request

class ProxmoxClusterInfoView(Resource):
    # URL to proxmox cluster
    proxmox_url = os.getenv("PROXMOX_URL")

    def connection():
        request_body = {
            "username": os.getenv("PROXMOX_USER"),
            "password": os.getenv("PROXMOX_PASSWORD"),
        }

        proxmox_url = os.getenv("PROXMOX_URL")

        try:
            # Added header to send data in a form proxmox understands
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            # Endpoint to get back CSRFToken and Ticket used in authentication
            response = requests.post(proxmox_url + "/api2/json/access/ticket", data=request_body, headers=headers, verify=False)
            response = response.json()

            # Adding CSRFToken and Ticket to header and cookies respectively
            headers_CSRF = {'CSRFPreventionToken': response["data"]["CSRFPreventionToken"]}
            cookies = {"PVEAuthCookie": response["data"]["ticket"]}

            return {"headers": headers_CSRF, "cookies": cookies, "proxmox_url": proxmox_url}

        except Exception as e:
            print(e)
            return {"headers": None, "cookies": None}

    def get(self):
        """ Returns the cluster metrics including CPU usage, Memory usage and Disk usage """
        tokens = ProxmoxClusterInfoView.connection()
        if tokens["headers"] is not None or tokens["cookies"] is not None:
            headers, cookies = tokens["headers"], tokens["cookies"]
            try:
                raw_cluster_data = requests.get(tokens["proxmox_url"] + "/api2/json/cluster/resources?type=node", headers=headers, verify=False, cookies=cookies)
                cluster_data = raw_cluster_data.json()
                return dict(status='success', data={
                    'cluster_data': cluster_data
                }), 200
            except Exception as e:
                print(e)
                return dict(status='fail', message='Internal Server Error'), 500
        else:
            return dict(status='fail', message='Internal Server Error'), 500

    def post(self):
        """ Returns the virtual machines running under a cluster """
        tokens = ProxmoxClusterInfoView.connection()
        app_data = request.get_json()
        if tokens["headers"] is not None or tokens["cookies"] is not None:
            headers, cookies = tokens["headers"], tokens["cookies"]
            try:
                raw_vm_data = requests.get(tokens["proxmox_url"] + "/api2/json/nodes/"+app_data["node_id"]+"/qemu", headers=headers, verify=False, cookies=cookies)
                vm_data = raw_vm_data.json()
                print(vm_data)
                return dict(status='success', data={
                    'vm_data': vm_data
                }), 200
            except Exception as e:
                print(e)
                return dict(status='fail', message='Internal Server Error'), 500
        else:
            return dict(status='fail', message='Internal Server Error'), 500