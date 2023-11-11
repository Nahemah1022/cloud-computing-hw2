import json
import requests
import boto3

import opensearch_client
from datetime import datetime

def lambda_handler(event, context):
    awsRegion = event['Records'][0]['awsRegion']
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    IMAGE_URL = f"https://{bucket}.s3.{awsRegion}.amazonaws.com/{key}"
    print(IMAGE_URL)
    labels = [label['Name'] for label in recognize_labels(bucket, key)["Labels"]]
    # print(labels)
    # index_photo(bucket, key, IMAGE_URL, labels)
    
    # res = opensearch_client.query('Nature', 1)
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
    response = opensearch_client.insert(document, image_url)
    print(response)
        
def recognize_labels(bucket, key):
    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    fileObject = s3.get_object(Bucket=bucket, Key=key)
    file_content = fileObject["Body"].read()
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            },
        },
        MaxLabels=123,
        MinConfidence=70,
    )
    return response