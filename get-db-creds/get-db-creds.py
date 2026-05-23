#!/usr/bin/env python3
import boto3
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Read database credentials metadata from AWS Secrets Manager")
    parser.add_argument("environment", nargs="?", default="dev", choices=["dev", "stage"])
    parser.add_argument("--show-password", action="store_true", help="Print the password value instead of masking it")
    args = parser.parse_args()

    enviro = args.environment.lower()

    if enviro == 'dev':
        secret = 'dev/your-aws-secret'
    elif enviro == 'stage':
        secret = 'stage/your-aws-secret'
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

    password_display = password if args.show_password else "***"
    print(f"The {enviro} database username is {user} and the password is {password_display}")

if __name__ == "__main__":
    main()