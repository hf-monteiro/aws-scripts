# ec2-inventory

Lists all EC2 instances in a region with their name tag, instance ID, state, type, private IP, and availability zone.

## Usage

```shell
chmod +x ec2-inventory.sh

# All instances in default region
./ec2-inventory.sh

# Running instances only in a specific region
./ec2-inventory.sh --region us-west-2 --state running

# Stopped instances
./ec2-inventory.sh --state stopped
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--region` | `$AWS_DEFAULT_REGION` or `us-east-1` | AWS region to query |
| `--state` | `all` | Filter by instance state (`running`, `stopped`, `all`, etc.) |

## Required IAM permissions

```json
{
  "Effect": "Allow",
  "Action": ["ec2:DescribeInstances"],
  "Resource": "*"
}
```

## Sample output

```
NAME                           INSTANCE-ID          STATE           TYPE               PRIVATE-IP      AZ
--------------------------------------------------------------------------------------------------------------
api-server-prod                i-0abc123def456789   running         t3.medium          10.0.1.42       us-east-1a
bastion                        i-0def456abc123789   running         t3.micro           10.0.0.5        us-east-1b
worker-001                     i-0fff000aaa111bbb   stopped         m5.large           10.0.2.10       us-east-1a
```
