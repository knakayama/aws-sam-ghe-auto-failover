from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import os

elb = boto3.client('elb')
LOAD_BALANCER_NAME = os.environ['LoadBalancerName']


def handler(event, context):
    output = event.copy()
    try:
        res1 = elb.register_instances_with_load_balancer(
                LoadBalancerName=LOAD_BALANCER_NAME,
                Instances=[{'InstanceId': os.environ['SecondaryInstanceId']}])
    except ClientError as e:
        print(e['Error']['Message'])
        output.update({'Error': e['Error']['Message']})
        return output
    else:
        print(res1)
        output.update({'RegisterInstanceResponse': 'Success'})

    try:
        res2 = elb.deregister_instances_from_load_balancer(
                LoadBalancerName=LOAD_BALANCER_NAME,
                Instances=[{'InstanceId': os.environ['PrimaryInstanceId']}])
    except ClientError as e:
        print(e['Error']['Message'])
        output.update({'Error': e['Error']['Message']})
        return output
    else:
        print(res2)
        output.update({'DeregisterInstanceResponse': 'Success'})
        return output
