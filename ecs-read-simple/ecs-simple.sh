#!/bin/bash
set -x
max_iteration=5

for i in $(seq 1 $max_iteration)
do
taskdef=$(aws ecs list-tasks --cluster $AWS_ECS_CLUSTER --family $AWS_ECS_SERVICE --desired-status RUNNING --region us-east-1 --output text --query taskArns[0])

  if [[ $taskdef != None ]]
  then
    echo "Deployment finished successfully in AWS"
    break
  else
    echo "Deployment still pending in AWS, retrying..."
    sleep 20
  fi
done
