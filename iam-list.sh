#!/bin/bash
#This script list all IAM user on the account and list all policies attached (policies, group policies, inline policies)
aws iam list-users --profile account-profile |grep -i username > list_users ;
cat list_users --profile account-profile |awk '{print $NF}' |tr '\"' ' ' |tr '\,' ' '|while read user; do echo "\n\n--------------Getting information for user $user-----------\n\n" ;
aws iam list-user-policies --profile account-profile --user-name $user --output yaml;
aws iam list-groups-for-user --profile account-profile --user-name $user --output yaml;
aws iam list-attached-user-policies --profile account-profile --user-name $user --output yaml; done;
