#!/usr/bin/env python3
"""Audits S3 buckets for public access settings, versioning, and encryption."""

import boto3
import argparse
import sys
from botocore.exceptions import ClientError

STATUS = {"Enabled": "ON", "Suspended": "SUSPENDED", "disabled": "OFF"}


def get_versioning(s3, bucket):
    try:
        r = s3.get_bucket_versioning(Bucket=bucket)
        return STATUS.get(r.get("Status", "disabled"), "OFF")
    except ClientError:
        return "ERR"


def get_encryption(s3, bucket):
    try:
        r = s3.get_bucket_encryption(Bucket=bucket)
        rules = r["ServerSideEncryptionConfiguration"]["Rules"]
        algo = rules[0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
        return algo
    except ClientError as e:
        if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
            return "NONE"
        return "ERR"


def get_public_access(s3, bucket):
    try:
        r = s3.get_public_access_block(Bucket=bucket)
        cfg = r["PublicAccessBlockConfiguration"]
        all_blocked = all([
            cfg.get("BlockPublicAcls", False),
            cfg.get("IgnorePublicAcls", False),
            cfg.get("BlockPublicPolicy", False),
            cfg.get("RestrictPublicBuckets", False),
        ])
        return "BLOCKED" if all_blocked else "OPEN"
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
            return "OPEN"
        return "ERR"


def main():
    parser = argparse.ArgumentParser(description="Audit S3 buckets for security posture")
    parser.add_argument("--region", default=None, help="Limit to buckets in this region")
    parser.add_argument("--public-only", action="store_true", help="Print only buckets with public access")
    args = parser.parse_args()

    s3 = boto3.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])

    if not buckets:
        print("No buckets found.")
        sys.exit(0)

    header = f"{'BUCKET':<50} {'REGION':<15} {'PUBLIC':<10} {'VERSIONING':<12} {'ENCRYPTION'}"
    print(header)
    print("-" * 105)

    found = 0
    for b in buckets:
        name = b["Name"]
        try:
            loc = s3.get_bucket_location(Bucket=name)
            region = loc["LocationConstraint"] or "us-east-1"
        except ClientError:
            region = "ERR"

        if args.region and region != args.region:
            continue

        public = get_public_access(s3, name)
        versioning = get_versioning(s3, name)
        encryption = get_encryption(s3, name)

        if args.public_only and public != "OPEN":
            continue

        flag = " <-- PUBLIC" if public == "OPEN" else ""
        print(f"{name:<50} {region:<15} {public:<10} {versioning:<12} {encryption}{flag}")
        found += 1

    print(f"\n{found} bucket(s) listed.")


if __name__ == "__main__":
    main()
