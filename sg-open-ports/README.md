# sg-open-ports

Scans EC2 security groups for ingress rules open to the entire internet (`0.0.0.0/0` or `::/0`). Flags rules that expose sensitive ports like SSH (22), RDP (3389), common databases, and cache/search services.

## Usage

```shell
pip install -r requirements.txt

# Scan all security groups in the default region
python3 sg-open-ports.py

# Only flag sensitive ports (SSH, RDP, DB, cache, search)
python3 sg-open-ports.py --sensitive-only

# Limit to a specific region and VPC
python3 sg-open-ports.py --region eu-west-1 --vpc vpc-0abc1234def567890
```

## Options

| Flag | Description |
|------|-------------|
| `--region` | AWS region to scan (defaults to profile/env region) |
| `--sensitive-only` | Only report rules on well-known risky ports |
| `--vpc` | Limit scan to a specific VPC ID |

## Sensitive ports flagged

| Port | Service |
|------|---------|
| 22 | SSH |
| 3389 | RDP |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 1433 | MSSQL |
| 27017 | MongoDB |
| 6379 | Redis |
| 9200 | Elasticsearch |
| 11211 | Memcached |

## Required IAM permissions

```json
{
  "Effect": "Allow",
  "Action": ["ec2:DescribeSecurityGroups"],
  "Resource": "*"
}
```

## Sample output

```
SG-ID                  NAME                           VPC                    PROTO    PORTS           SENSITIVE
---------------------------------------------------------------------------------------------------------
sg-0abc123def456789    default                        vpc-0aaa1111bbb2222c   TCP      22              *
sg-0def456abc123789    web-alb-sg                     vpc-0aaa1111bbb2222c   TCP      80-443
sg-0fff000aaa111bbb    legacy-api                     vpc-0ccc3333ddd4444e   ALL      ALL             *

3 open rule(s) found across security groups.
(*) marks rules exposing sensitive ports: SSH/RDP/DB/cache/search
```
