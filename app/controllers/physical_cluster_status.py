import os
import json
from flask_restful import Resource
from app.helpers.status import get_physical_cluster_status
from app.models.log import ClusterLog


class PhysicalClusterStatusView(Resource):
    # Saving cluster logs
    def saveClusterLog(cluster_id, status):

        new_log = ClusterLog(
            cluster_id=cluster_id,
            status=status,
        )

        saved = new_log.save()

        if not saved:
            return dict(status='fail', message='Internal Server Error'), 500

        return dict(status='success', message='Log saved'), 201

    def get(self):
        # Get physical cluster status
        clusters = json.loads(os.getenv('TEST_CLUSTERS', None))

        physical_cluster_status = get_physical_cluster_status(clusters)

        try:
            for cluster in physical_cluster_status['data']:
                PhysicalClusterStatusView.saveClusterLog(cluster['cluster_name'], cluster['status'])

        except Exception as e:
            print(e)

        return dict(status='success', data={
            'physical_cluster_status': physical_cluster_status
        }), 200
