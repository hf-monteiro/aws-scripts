# s3-audit

Audits all S3 buckets in the account for public access block status, versioning, and server-side encryption.

## Usage

```shell
pip install -r requirements.txt

# Audit all buckets
python3 s3-audit.py

# Only show buckets with public access (useful for quick security sweep)
python3 s3-audit.py --public-only

# Filter by region
python3 s3-audit.py --region us-east-1
```

## Options

| Flag | Description |
|------|-------------|
| `--region` | Only audit buckets located in this region |
| `--public-only` | Print only buckets where public access is not fully blocked |

## Required IAM permissions

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:ListAllMyBuckets",
    "s3:GetBucketLocation",
    "s3:GetBucketVersioning",
    "s3:GetEncryptionConfiguration",
    "s3:GetBucketPublicAccessBlock"
  ],
  "Resource": "*"
}
```

## Sample output

```
BUCKET                                             REGION          PUBLIC     VERSIONING   ENCRYPTION
---------------------------------------------------------------------------------------------------------
my-private-bucket                                  us-east-1       BLOCKED    ON           aws:kms
logs-archive-2024                                  us-east-1       BLOCKED    OFF          AES256
old-public-assets                                  us-west-2       OPEN       SUSPENDED    NONE       <-- PUBLIC

3 bucket(s) listed.
```
