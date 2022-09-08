import os
import json
from flask_restful import Resource, request
from app.helpers.status import get_physical_cluster_status
from app.models.log import ClusterLog
from app.schemas.logs import ClusterLogsSchema
from app.schemas.logs import StatusSchema

def clusterLogFunction():
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

    def post(self):
        # Get physical cluster status
        cluster_schema = ClusterLogsSchema(many=True)
        status_schema = StatusSchema()
        cluster_data = request.get_json()

        validated_update_data, errors = status_schema.load(cluster_data)

        if errors:
           return dict(status='fail', message=errors), 400

        clusters = json.loads(os.getenv('TEST_CLUSTERS', None))

        physical_cluster_status = get_physical_cluster_status(clusters)

        try:
            # for cluster in physical_cluster_status['data']:
            #     PhysicalClusterStatusView.saveClusterLog(cluster['cluster_name'], cluster['status'])
       
            clusters_logs = ClusterLog.find_all(cluster_id = validated_update_data['cluster_id'])

            validated_cluster_data, errors = cluster_schema.dumps(clusters_logs)

            if errors:
                return dict(status='fail', message='Internal Server Error'), 500

            clusters_data_list = json.loads(validated_cluster_data)
            cluster_count = len(clusters_data_list)

            return dict(status='Success',
                        data=dict(logs=clusters_data_list)), 200

        except Exception as e:
            print(e)

        #return dict(status='success', data={
        #    'physical_cluster_status': physical_cluster_status
        #}), 200

class PhysicalClusterInfo(Resource):
    def get(self):

        cluster_schema = ClusterLogsSchema(many=True)
        clusters_logs = ClusterLog.find_all()

        validated_cluster_data, errors = cluster_schema.dumps(clusters_logs)

        if errors:
            return dict(status='fail', message='Internal Server Error'), 500

        clusters = json.loads(os.getenv('TEST_CLUSTERS', None))

        clusters_data_list = json.loads(validated_cluster_data)
        cluster_count = len(clusters_data_list)

        return dict(status='Success',
                    data=dict(logs=json.loads(validated_cluster_data), clusters = clusters, metadata=dict(cluster_count=cluster_count))), 200