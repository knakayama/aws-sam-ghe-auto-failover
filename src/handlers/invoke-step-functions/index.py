from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import os

client = boto3.client('stepfunctions')


def handler(event, context):
    try:
        res = client.start_execution(
                **{
                  'input': '{"Comment": "GHE Failover Occured"}',
                  'stateMachineArn': os.environ['StateMachineArn']
                  }
                )
    except ClientError as e:
        print(e['Error']['Message'])
        return e['Error']['Message']
    else:
        print(res)
        return
