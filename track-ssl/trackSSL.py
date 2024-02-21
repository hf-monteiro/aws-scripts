#!/usr/bin/env python
import boto3
import requests
import json
import sys
from botocore.exceptions import ClientError 
def get_api_key():
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(
            SecretId='example/track-ssl-key'
        )
    except ClientError as e:
         if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Could not find API key in Secrets Manager")
            exit(1)
         elif e.response['Error']['Code'] == 'InternalServerError':
            print("AWS Secrets Manager encountered a problem. Please try again later")
            exit(1)
         else:
            print("An unknown error occurred trying to retreive the API key. Please try again")
    secret = response['SecretString']
    apiKey = json.loads(secret)['api-key']
    return apiKey

def addHost(apiKey: str, hostName: str):
    url = f"https://app.trackssl.com/api/v1/hosts/{hostName}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        status = {"code": 0, "message": "Host already monitored"}
    elif response.status_code == 201:
        status = {"code": 0, "message": "Host added successfully"}
    elif response.status_code == 401:
        status = {"code": 1, "message": "Authorization Failure"}
    elif response.status_code == 402:
        status = {"code": 1, "message": "Failed! Account payment needed"}
    else:
        status = {"code": 2, "message": "Request status unknown"}
    return status

def main():
    if len(sys.argv) < 2:
        print("Missing required arguments")
    host = sys.argv[1]
    apiKey = get_api_key()
    status = addHost(apiKey, host)
    if status["code"] == 0:
        print(f"Success! {status['message']}")
    elif status["code"] == 1:
        print(f"Failed! {status['message']}")
    else:
        print("Unknown status")

if __name__ == "__main__":
    main()
