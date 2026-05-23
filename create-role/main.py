#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Iterable

import boto3
import botocore.exceptions


def get_accounts(max_results: int = 20) -> list[dict]:
    org_client = boto3.client("organizations")
    accounts: list[dict] = []
    paginator = org_client.get_paginator("list_accounts")

    try:
        for page in paginator.paginate(PaginationConfig={"PageSize": max_results}):
            accounts.extend(page.get("Accounts", []))
    except botocore.exceptions.ClientError as error:
        print(f"Failed to get account list due to error: {error}", file=sys.stderr)
        sys.exit(1)

    return accounts


def create_policy_doc(account_num: str) -> str:
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": f"arn:aws:iam::{account_num}:root"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    )


def iam_client_from_credentials(credentials: dict):
    return boto3.client(
        "iam",
        region_name="us-east-1",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def create_role(iam_client, policy_doc: str, account_id: str, role_name: str) -> bool:
    try:
        iam_client.create_role(
            AssumeRolePolicyDocument=policy_doc,
            Path="/",
            RoleName=role_name,
        )
    except botocore.exceptions.ClientError as error:
        if error.response.get("Error", {}).get("Code") == "EntityAlreadyExists":
            print(f"Role {role_name} already exists in account {account_id}")
            return True
        print(f"Unable to create role in account {account_id} due to: {error}", file=sys.stderr)
        return False
    return True


def attach_policy(iam_client, role_name: str, policy_arn: str) -> bool:
    try:
        iam_client.attach_role_policy(PolicyArn=policy_arn, RoleName=role_name)
    except botocore.exceptions.ClientError as error:
        print(f"Unable to attach policy {policy_arn} to role {role_name} due to {error}", file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a role that can be assumed by an external AWS account."
    )
    parser.add_argument("extAccount", help="External AWS account ID allowed to assume the new role")
    parser.add_argument("roleName", help="Name of the role to create in each account")
    parser.add_argument(
        "--assume-role-name",
        default="terraform",
        help="Existing role to assume in each member account",
    )
    parser.add_argument(
        "--policy-arn",
        default="arn:aws:iam::aws:policy/ReadOnlyAccess",
        help="Policy ARN to attach to the created role",
    )
    args = parser.parse_args()

    accounts = get_accounts()
    policy_doc = create_policy_doc(args.extAccount)
    sts_client = boto3.client("sts")

    for account in accounts:
        account_id = account["Id"]
        try:
            response = sts_client.assume_role(
                RoleArn=f"arn:aws:iam::{account_id}:role/{args.assume_role_name}",
                RoleSessionName="create-cross-account-role",
            )
        except botocore.exceptions.ClientError as error:
            print(f"Unable to assume role in {account_id}: {error}", file=sys.stderr)
            continue

        iam_client = iam_client_from_credentials(response["Credentials"])
        if create_role(iam_client, policy_doc, account_id, args.roleName):
            print(f"Role {args.roleName} ready in account {account_id}")
            attach_policy(iam_client, args.roleName, args.policy_arn)


if __name__ == "__main__":
    main()
