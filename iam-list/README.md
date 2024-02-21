 # AWS IAM User and Policy Listing Script

This script is designed to list all IAM users in an AWS account and display all policies attached to each user. It includes policies directly attached to the user, policies attached through groups, and inline policies.

## Prerequisites

Before running this script, ensure you have the following:
- AWS CLI installed and configured
- Proper AWS credentials configured for the `account-profile`

## How to Use

1. **Prepare the Script**: Save the script into a file, for example, `list_iam_users.sh`.

2. **Make the Script Executable**:
    ```
    chmod +x list_iam_users.sh
    ```

3. **Run the Script**:
    ```
    ./list_iam_users.sh
    ```

The script operates by:
- Listing all IAM users in the specified account profile.
- Extracting usernames and iterating over them.
- For each user, the script lists:
  - Directly attached user policies (in YAML format).
  - Groups the user is a part of, along with group policies (in YAML format).

## Output

The output will be displayed in the terminal, structured as follows:
- A header indicating the start of information retrieval for a user.
- List of user policies in YAML format.
- List of groups the user is part of, also in YAML format.

## Note

Ensure that the `account-profile` specified in the script matches the profile name configured in your AWS CLI setup.

## Troubleshooting

- If the script fails to run, verify that AWS CLI is correctly installed and that your `account-profile` is correctly configured.
- Ensure you have the necessary permissions to list IAM users and policies.

For more detailed information on the commands used in this script, consult the [AWS CLI Documentation](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/index.html).
