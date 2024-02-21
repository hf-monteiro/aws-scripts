#!/usr/bin/env python3
import boto3
import sys
import json

def main():
    if len(sys.argv) <= 1:
        enviro = "dev"
    if len(sys.argv) == 2:
        enviro = sys.argv[1]

    enviro = enviro.lower()

    if enviro == 'dev':
        secret = 'dev/your-aws-secret'
    elif enviro == 'stage':
        secret = 'stage/your-aws-secret'
    else:
        print(f"{sys.argv[1]} is not a valid environment")
        exit(1)

    client = boto3.client('secretsmanager')

    try:
        rawResponse = client.get_secret_value(
        SecretId = secret
    )
    except client.exceptions.ClientError as e:
        print(f"Could not find {secret} please ensure that you are authenticated to the correct AWS account")
        exit(1)

    response = json.loads(rawResponse["SecretString"])

    user = response["GLOBAL_DATASOURCE_USERNAME"]
    password = response["GLOBAL_DATASOURCE_PASSWORD"]

    print(f"The {enviro} database username is {user} and the password is {password}")

if __name__ == "__main__":
    main()