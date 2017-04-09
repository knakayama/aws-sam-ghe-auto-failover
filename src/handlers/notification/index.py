from __future__ import print_function
from botocore.exceptions import ClientError
import boto3
import json
import os


sns = boto3.client('sns')


def handler(event, context):
    req = {
            'TopicArn': os.environ['TopicArn'],
            'Message': json.dumps(event),
            'Subject': '[Alart] GHE Failover Occured'
            }
    try:
        res = sns.publish(**req)
    except ClientError as e:
        print(e['Error']['Message'])
        return e['Error']['Message']
    else:
        print(res)
        return
