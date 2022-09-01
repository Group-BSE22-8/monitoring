from flask_restful import Api
from app.controllers import (
    IndexView, PhysicalClusterStatusView)


api = Api()

# Index route
api.add_resource(IndexView, '/')

# User routes
api.add_resource(PhysicalClusterStatusView, '/status', endpoint='physical_cluster_status')

