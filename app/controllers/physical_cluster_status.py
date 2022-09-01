import os
import json
from flask_restful import Resource
from app.helpers.status import get_physical_cluster_status

class PhysicalClusterStatusView(Resource):
    def get(self):
        # Get physical cluster status
        clusters = json.loads(os.getenv('CLUSTERS', None))

        physical_cluster_status = get_physical_cluster_status(clusters)

        return dict(status='success', data={
            'physical_cluster_status': physical_cluster_status
        }), 200