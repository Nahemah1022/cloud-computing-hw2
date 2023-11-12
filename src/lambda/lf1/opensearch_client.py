import json
import os

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

REGION = 'us-east-2'
HOST = 'search-photos-szqe434hz3ystqqh2xqr5umx4a.us-east-2.es.amazonaws.com'
INDEX = 'photos'

def query(term, num):
    q = {'size': num, 'query': {'multi_match': {'query': term}}}

    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
    http_auth=get_awsauth(REGION, 'es'),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection)

    res = client.search(index=INDEX, body=q)

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results


def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)

def insert(document, id):
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
    http_auth=get_awsauth(REGION, 'es'),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection)

    response = client.index(
        index = INDEX,
        body = document,
        id = id,
        refresh = True
    )
    return response
    

if __name__ == '__main__':
    results = query('Dutch Freds')
    print(result)
