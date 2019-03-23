from urllib.parse import parse_qsl
import json


# SQS - Lambda
def unpack_payload(payload):
    """ unpack SQS-Lambda formatted data """
    formatted = {}
    for key in payload:
        v = payload[key]['stringValue']
        try:
            formatted[key] = json.loads(v)
        except json.decoder.JSONDecodeError:
            formatted[key] = v
    return formatted


def unpack(record):
    return {
        'data': json.loads(record['body']),
        'params': unpack_payload(record['messageAttributes'])
    }


def sqs_handler(event, context):
    for record in event['Records']:
        record_data = unpack(record)
        data = record_data['data']
        params = record_data['params']
        # do something


# API Gateway - Lambda
def parse_lambda_body(body):
    """
    body: event['body']
    body 는 query string 형식을 가진다.
    files 가 있다면 이 형식이 깨진다.
    """
    if type(body) == str:
        return dict(parse_qsl(body))
    return body if type(body) == dict else {}


def parse_lambda_qs(qs):
    """
    qs : event['queryStringParameters']
    qs : event['multiValueQueryStringParameters']
    """
    return qs if qs is not None else {}


def api_gateway_handler(event, context):
    method = event['httpMethod']
    params = parse_lambda_qs(event['queryStringParameters'])
    # event['multiValueQueryStringParameters']
    body = parse_lambda_body(event['body'])


"""
event_with_files = {
    'body': '--fd22ddc7924e54c28e1b2ac1034417b5'
            '\r\n'
            'Content-Disposition: form-data; name="key1"'
            '\r\n\r\n'
            'value1'
            '\r\n'
            
            '--fd22ddc7924e54c28e1b2ac1034417b5'
            '\r\n'
            'Content-Disposition: form-data; name="key2"'
            '\r\n\r\n'
            'value2'
            '\r\n'
            
            '--fd22ddc7924e54c28e1b2ac1034417b5'
            '\r\n'
            'Content-Disposition: form-data; name="file1"; filename="file1"'
            '\r\n\r\n'
            '�PNG.....',
}
"""
