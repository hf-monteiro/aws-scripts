## ECS Task Status Checker Script

This script is designed to interact with AWS Elastic Container Service (ECS) to monitor and verify the status of specific tasks within a designated ECS cluster. It aims to ensure that tasks are running as expected and facilitates a retry mechanism to handle scenarios where tasks may not be immediately available or in the desired state.

### Prerequisites

Before running this script, ensure you have:

- AWS CLI installed and configured with appropriate permissions to list and describe ECS task definitions and tasks.
- Bash environment to execute the script.

### Configuration

Set the following variables at the beginning of the script according to your AWS ECS setup:

- `CLUSTER`: The name of the ECS cluster you are monitoring.
- `FAMILY`: The family name of your task definition (not used in the current script version but reserved for future use).

### Usage

To use the script, follow these steps:

1. **Set Executable Permissions:**

   First, ensure the script is executable by running:

   ```bash
   chmod +x check_ecs_tasks.sh
   ```

2. **Execute the Script:**

   Run the script by simply executing it in your terminal:

   ```bash
   ./check_ecs_tasks.sh
   ```

The script will:

- Retrieve the latest task definition and check its status.
- Look for the first running task ARN within the specified cluster.
- Attempt to find a running task up to 6 times if none is found initially, with a delay of 3 seconds between each retry.
- Verify if the found task is stable based on its running status and matching task definition ARN.

### Output

The script outputs the status of the task definition, the ARN of the running task if found, and whether the task is considered "STABLE" or "UNSTABLE" based on the checks performed.

### Important Notes

- The script assumes the AWS CLI is configured with sufficient permissions.
- It's designed for debugging and operational insights, not for production-grade monitoring.

For any issues or improvements, please feel free to contribute to the script or contact the maintainers.
