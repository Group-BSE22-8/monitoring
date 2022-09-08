from flask_restful import Api
from app.controllers import (
    IndexView, PhysicalClusterStatusView, PhysicalClusterInfo, ProxmoxClusterInfoView, SendMail)


api = Api()

# Index route
api.add_resource(IndexView, '/')

# User routes
api.add_resource(PhysicalClusterStatusView, '/status', endpoint='physical_cluster_status')
api.add_resource(PhysicalClusterInfo, '/status/cluster_data')
api.add_resource(ProxmoxClusterInfoView, '/proxmox/cluster_metrics', endpoint='proxmox_info')
api.add_resource(ProxmoxClusterInfoView, '/proxmox/cluster_metrics/machine')
api.add_resource(SendMail, '/sendmail', endpoint='send_mail')

