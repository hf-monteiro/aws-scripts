#!/usr/bin/env python3
"""
Finds EC2 security groups with ingress rules open to the internet
(0.0.0.0/0 or ::/0) and reports the affected ports and protocols.
"""

import boto3
import argparse
import sys

DANGEROUS_PORTS = {22, 3389, 5432, 3306, 1433, 27017, 6379, 9200, 11211}


def port_range(rule):
    from_port = rule.get("FromPort", -1)
    to_port = rule.get("ToPort", -1)
    if from_port == -1 and to_port == -1:
        return "ALL"
    if from_port == to_port:
        return str(from_port)
    return f"{from_port}-{to_port}"


def is_open_to_world(rule):
    for cidr in rule.get("IpRanges", []):
        if cidr.get("CidrIp") == "0.0.0.0/0":
            return True
    for cidr in rule.get("Ipv6Ranges", []):
        if cidr.get("CidrIpv6") == "::/0":
            return True
    return False


def is_sensitive(rule):
    from_port = rule.get("FromPort", -1)
    to_port = rule.get("ToPort", -1)
    if from_port == -1:
        return True
    return any(from_port <= p <= to_port for p in DANGEROUS_PORTS)


def main():
    parser = argparse.ArgumentParser(
        description="Find security groups with internet-open ingress rules"
    )
    parser.add_argument("--region", default=None, help="AWS region (default: profile region)")
    parser.add_argument("--sensitive-only", action="store_true",
                        help="Only flag rules on well-known sensitive ports")
    parser.add_argument("--vpc", help="Limit to a specific VPC ID")
    args = parser.parse_args()

    ec2 = boto3.client("ec2", region_name=args.region)

    filters = []
    if args.vpc:
        filters.append({"Name": "vpc-id", "Values": [args.vpc]})

    paginator = ec2.get_paginator("describe_security_groups")
    pages = paginator.paginate(Filters=filters)

    findings = []
    for page in pages:
        for sg in page["SecurityGroups"]:
            sg_id = sg["GroupId"]
            sg_name = sg["GroupName"]
            vpc_id = sg.get("VpcId", "—")
            name_tag = next(
                (t["Value"] for t in sg.get("Tags", []) if t["Key"] == "Name"), ""
            )
            display_name = name_tag or sg_name

            for rule in sg.get("IpPermissions", []):
                if not is_open_to_world(rule):
                    continue
                if args.sensitive_only and not is_sensitive(rule):
                    continue

                proto = rule.get("IpProtocol", "?")
                proto = "ALL" if proto == "-1" else proto.upper()
                ports = port_range(rule)
                sensitive = "*" if is_sensitive(rule) else ""
                findings.append((sg_id, display_name, vpc_id, proto, ports, sensitive))

    if not findings:
        print("No open-to-world ingress rules found.")
        sys.exit(0)

    print(f"{'SG-ID':<22} {'NAME':<30} {'VPC':<22} {'PROTO':<8} {'PORTS':<15} SENSITIVE")
    print("-" * 105)
    for sg_id, name, vpc, proto, ports, sensitive in sorted(findings, key=lambda x: x[0]):
        print(f"{sg_id:<22} {name[:29]:<30} {vpc:<22} {proto:<8} {ports:<15} {sensitive}")

    print(f"\n{len(findings)} open rule(s) found across security groups.")
    if any(f[5] for f in findings):
        print("(*) marks rules exposing sensitive ports: SSH/RDP/DB/cache/search")


if __name__ == "__main__":
    main()
