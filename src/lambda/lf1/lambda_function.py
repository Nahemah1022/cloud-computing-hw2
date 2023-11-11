import json

def lambda_handler(event, context):
    awsRegion = event['Records'][0]['awsRegion']
    bucket = event['Records'][0]['s3']['bucket']['name']
    path = event['Records'][0]['s3']['object']['key']
    IMAGE_URL = f"https://{bucket}.s3.{awsRegion}.amazonaws.com/{path}"
    print(IMAGE_URL)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
