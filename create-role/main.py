#!/usr/bin/env python3
import boto3
import botocore.exceptions
import json
import argparse


def getAccounts(token: str = "", maxResults: int = 20) -> list:
    orgClient = boto3.client("organizations")
    accounts = []
    if token != "":
        try:
            response = orgClient.list_accounts(NextToken=token, MaxResults=maxResults)
        except botocore.exceptions.ClientError as error:
            print(f"Failed to get account list due to error: {error}")
            exit(1)
        accounts.append(response["Accounts"])
        if "NextToken" in response:
                    next = response["NextToken"]
            getAccounts(token=next)
    else:
        try:
            response = orgClient.list_accounts(MaxResults=maxResults)
        except botocore.exceptions.ClientError as error:
            print(f"Failed to get account list due to error: {error}")
            exit(1)
        accounts.append(response["Accounts"])
        if "NextToken" in response:
            next = response["NextToken"]
            getAccounts(token=next)
    return accounts


def createPolicyDoc(accountNum: str) -> str:
    assume_role_doc = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": f"arn:aws:iam::{accountNum}:root"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    )

    return assume_role_doc


def createRole(
    policyDoc: str, account: str, name: str, id: str, key: str, sess: str) -> bool:
    iamClient = boto3.client(
        "iam",
        region_name="us-east-1",
        aws_access_key_id=id,
        aws_secret_access_key=key,
        aws_session_token=sess,
    )
    try:
        response = iamClient.create_role(
            AssumeRolePolicyDocument=policyDoc, Path="/", RoleName=name
        )
    except botocore.exceptions.ClientError as error:
        print(f"Unable to create role in account: {account} due to: {error}")
        return False
    return True


def attachPolicy(role: str, id: str, key: str, sess: str, policy: str) -> bool:
    iamClient = boto3.client(
        "iam",
        region_name="us-east-1",
        aws_access_key_id=id,
        aws_secret_access_key=key,
        aws_session_token=sess,
    )
    try:
        response = iamClient.attach_role_policy(PolicyArn=policy, RoleName=role)
    except botocore.exceptions.ClientError as error:
        print(f"Unable to attach policy {policy} to role {roleName} due to {error}")
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a role that can be assumed by outside entity"
    )
    parser.add_argument("extAccount", type=str)
    parser.add_argument("roleName", type=str)
    args = parser.parse_args()
    extAccount = args.extAccount
    roleName = args.roleName

    accounts = getAccounts()
    policyDoc = createPolicyDoc(extAccount)
    for a in accounts:
        for account in a:
            accountId = account["Id"]
            stsClient = boto3.client("sts")
            try:
                response = stsClient.assume_role(
                    RoleArn=f"arn:aws:iam::{accountId}:role/terraform",
                    RoleSessionName="boto",
                )
                session_id = response["Credentials"]["AccessKeyId"]
                session_key = response["Credentials"]["SecretAccessKey"]
                session_token = response["Credentials"]["SessionToken"]
                result = createRole(
                    policyDoc,
                    extAccount,
                    roleName,
                    session_id,
                    session_key,
                    session_token,
                )
                if result == True:
                    print(f"Role {roleName} created successfully in account {account}")
                policyResult = attachPolicy(
                    role=roleName,
                    policy="arn:aws:iam::aws:policy/ReadOnlyAccess",
                    id=session_id,
                    key=session_key,
                    sess=session_token,
                )
            except botocore.exceptions.ClientError as error:
                print(
                    f"Unable to assume role in {account}, please confirm that the role exists"
                )
                continue


if __name__ == "__main__":
    main()
