import json

import boto3

sqs_client = boto3.client('sqs', region_name='ap-northeast-2')


def pack_payload(payload):
    packed = {}
    for key in payload:
        packed[key] = {
            'StringValue': json.dumps(payload[key]),
            'DataType': 'String'
        }
    return packed


def send_sqs(sqs_url, data=None, params=None):
    if not data:
        data = {}
    if not params:
        params = {}

    try:
        resp = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(data),
            DelaySeconds=0,
            MessageAttributes=pack_payload(params)
        )
    except Exception as e:
        pass
