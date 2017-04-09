from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import os

elb = boto3.client('elb')


def handler(event, context):
    try:
        instance_id_attached = elb.describe_load_balancers(
                LoadBalancerNames=[os.environ['LoadBalancerName']]
                )['LoadBalancerDescriptions'][0]['Instances'][0]['InstanceId']
    except ClientError as e:
        print(e['Error']['Message'])
        return {'Result1': e['Error']['Message']}
    else:
        if instance_id_attached == os.environ['PrimaryInstanceId']:
            return {'Result1': 'OK'}
        else:
            return {'Result1': 'Attached Instance Id is not expected: {}'.format(instance_id_attached)}
