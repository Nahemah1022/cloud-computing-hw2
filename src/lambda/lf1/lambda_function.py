import json
import requests
import boto3
import base64

import opensearch_client
from datetime import datetime

def lambda_handler(event, context):
    awsRegion = event['Records'][0]['awsRegion']
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    IMAGE_URL = f"https://{bucket}.s3.{awsRegion}.amazonaws.com/{key}"
    print(IMAGE_URL)
    print(IMAGE_URL)
    labels = recognize_labels(bucket, key)
    index_photo(bucket, key, IMAGE_URL, labels)
    
    # res = opensearch_client.query('Capoo', 1)
    # print(res)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def index_photo(bucket, key, image_url, labels):
    document = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": datetime.now().isoformat(),
        "labels": labels
    }
    print(document)
    opensearch_client.insert(document, image_url)
        
def recognize_labels(bucket, key):
    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    meta = s3.head_object(
        Bucket=bucket,
        Key=key,
    )
    print(meta)
    fileObject = s3.get_object(Bucket=bucket, Key=key)
    file_content = fileObject["Body"].read()
    bytes = base64.b64decode(file_content)
    detected_labels = client.detect_labels(
        Image={
            'Bytes': bytes
        },
        MaxLabels=123,
        MinConfidence=70,
    )
    res = [label['Name'] for label in detected_labels["Labels"]]
    res.extend(meta['Metadata']['customlabels'].split(','))
    return res