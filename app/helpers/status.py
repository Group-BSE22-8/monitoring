
from imp import reload
import os
from time import clock_settime

import requests
from yaml import scan


def get_status(success, failed, partial=0):

    if partial > 0:
        return 'partial'
    elif failed == 0:
        if success == 0:
            return 'failed'
        else:
            return 'success'
    elif success == 0:
        return 'failed'
    else:
        return 'partial'


def check_url_status(url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code != 200 and response.status_code != 201:
            return {
                'status': 'failed',
                'data': {
                    'status_code': response.status_code,
                    'message': response.reason
                }
            }

        return {'status': 'success',
                'data': {
                    'status_code': response.status_code,
                    'message': response.reason
                    }
                }
    except Exception as e:
        return {
            'status': 'error',
            'data': {
                'status_code': response.status_code,
                'message': str(e)
            }
        }

def get_physical_cluster_status(clusters):
    clusters_status = []
    success = 0
    failed = 0
    partial = 0
    for index, cluster in enumerate(clusters):
        status = check_url_status(cluster['url'])
        clusters_status.append({
            'cluster_name': cluster['name'],
            'status': status['status'],
            'cluster_status': status['data']
        })
        success += 1 if status['status'] == 'success' else 0
        failed += 1 if status['status'] == 'failed' else 0
        partial += 1 if status['status'] == 'partial' else 0

    return {'status': get_status(success, failed, partial),
            'data': clusters_status}