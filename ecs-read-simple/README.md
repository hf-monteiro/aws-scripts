# AWS ECS Deployment Status Checker

This script is designed to check the status of a deployment on Amazon Web Services (AWS) Elastic Container Service (ECS). It's particularly useful in Continuous Integration (CI) workflows to ensure that a deployment has successfully transitioned to a `RUNNING` state.

## Overview

The script utilizes the AWS CLI to query the ECS service for the status of tasks within a specified cluster and service. It aims to identify if at least one task has reached a `RUNNING` status, indicating a successful deployment.

## How It Works

- The script sets a maximum number of iterations (`max_iteration=5`) to check for a running task, avoiding infinite loops.
- It queries AWS ECS for tasks that are part of the specified cluster and service, filtering for those with a `RUNNING` desired status.
- If a running task is found within the maximum allowed iterations, the script reports a successful deployment. Otherwise, it indicates that the deployment is still pending.

## Usage

1. Ensure you have AWS CLI installed and configured with the necessary access permissions to query ECS tasks.
2. Set the following environment variables before running the script:
   - `AWS_ECS_CLUSTER`: The name of the ECS cluster.
   - `AWS_ECS_SERVICE`: The name of the ECS service.
3. Execute the script in your terminal or CI environment.

## Script Behavior

- The script executes up to 5 checks at 20-second intervals.
- It outputs the deployment status to the console, indicating either success or that the deployment is still pending.

This tool is invaluable for automation in deployment pipelines, providing immediate feedback on the status of ECS deployments.
