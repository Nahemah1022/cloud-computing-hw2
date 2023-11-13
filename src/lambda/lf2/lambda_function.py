import json
import requests
import boto3
import base64

import opensearch_client
from datetime import datetime

def lambda_handler(event, context):
    
    print(event)
    
    blackList = ["the", "show", "me", "and", "in", "on", "a", "he", "she", "we", "they", "this", "with", "photos", "photo"]
    n = 2
    # 'querystring': {'myQuery': 'ewrt'}
    
    # print('Go')
    
    # print(event['params']['querystring']['myQuery'])
    
    rawQuery = event['params']['querystring']['myQuery']
    # rawQuery = "Show me the toy and birds"
    
    tokens = rawQuery.split(" ")
    print(tokens)
    
    body = []
    
    for token in tokens:
        if token.lower() not in blackList:
            print(token)
            results = opensearch_client.query(token, n)
            for res in results:
                IMAGE_URL = f"https://b2-photo-uploads.s3.us-east-2.amazonaws.com/{res['objectKey']}"
                print(IMAGE_URL)
                print(res['labels'])
                body.append({"url": IMAGE_URL, 
                            "label":res['labels']
                })
                
    
    return {
        'statusCode': 200,
        'body': body
    }
    