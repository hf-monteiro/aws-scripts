# AWS Role Creation Script

This Python script automates the creation of AWS IAM roles and attaches a predefined policy to them. It's designed to work with multiple AWS accounts managed through AWS Organizations. The script assumes roles in each account to create a new IAM role that can be assumed by an external entity, specified by its AWS account ID.

## Prerequisites

- Python 3.x installed
- Boto3 installed (`pip install boto3`)
- AWS CLI configured with at least one profile
- Permissions to list accounts in AWS Organizations, assume roles, create roles, and attach policies in target accounts

## Usage

1. **Set up your AWS CLI and Boto3**: Ensure you have AWS CLI installed and configured with credentials that have permissions to perform the actions mentioned in prerequisites.

2. **Install dependencies**: If you haven't already, install Boto3 using pip:

3. **Run the Script**: Use the following command to run the script, replacing `<external_account_id>` with the AWS account ID of the external entity that should be allowed to assume the role, and `<role_name>` with the desired name for the IAM role to be created in each account:
```sh
./script.py <external_account_id> <role_name>

