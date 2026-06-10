#!/usr/bin/env bash
# Lists EC2 instances with name, state, type, AZ, and private IP.
# Usage: ./ec2-inventory.sh [--region us-east-1] [--state running|stopped|all]

set -euo pipefail

REGION="${AWS_DEFAULT_REGION:-us-east-1}"
FILTER_STATE="all"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --region) REGION="$2"; shift 2 ;;
    --state)  FILTER_STATE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

FILTERS="Name=instance-state-name,Values=pending,running,stopping,stopped,shutting-down,terminated"
if [[ "$FILTER_STATE" != "all" ]]; then
  FILTERS="Name=instance-state-name,Values=${FILTER_STATE}"
fi

printf "%-30s %-20s %-15s %-18s %-15s %s\n" \
  "NAME" "INSTANCE-ID" "STATE" "TYPE" "PRIVATE-IP" "AZ"
printf '%s\n' "$(printf '%.0s-' {1..110})"

aws ec2 describe-instances \
  --region "$REGION" \
  --filters "$FILTERS" \
  --query 'Reservations[].Instances[].[
    Tags[?Key==`Name`].Value | [0] || `(no name)`,
    InstanceId,
    State.Name,
    InstanceType,
    PrivateIpAddress || `—`,
    Placement.AvailabilityZone
  ]' \
  --output text | sort -k3 | \
  while IFS=$'\t' read -r name id state type ip az; do
    printf "%-30s %-20s %-15s %-18s %-15s %s\n" \
      "${name:0:29}" "$id" "$state" "$type" "$ip" "$az"
  done
