import boto3

# Specify the AWS region and the security group ID to monitor
region = 'us-west-2'
security_group_id = '<your-security-group-id>'

# Create an EC2 client
ec2_client = boto3.client('ec2', region_name=region)

# Get the initial inbound and outbound security group rules
response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
initial_inbound_rules = response['SecurityGroups'][0]['IpPermissions']
initial_outbound_rules = response['SecurityGroups'][0]['IpPermissionsEgress']

# Define a function to check for security group rule changes
def check_rule_changes():
    # Get the latest inbound and outbound security group rules
    response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
    latest_inbound_rules = response['SecurityGroups'][0]['IpPermissions']
    latest_outbound_rules = response['SecurityGroups'][0]['IpPermissionsEgress']

    # Check if there are any differences between the initial and latest rules
    if (initial_inbound_rules != latest_inbound_rules or
            initial_outbound_rules != latest_outbound_rules):
        # Remediate the security group by resetting the rules to their initial state
        ec2_client.revoke_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=latest_inbound_rules
        )
        ec2_client.revoke_security_group_egress(
            GroupId=security_group_id,
            IpPermissions=latest_outbound_rules
        )
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=initial_inbound_rules
        )
        ec2_client.authorize_security_group_egress(
            GroupId=security_group_id,
            IpPermissions=initial_outbound_rules
        )
        print(f'Security group {security_group_id} has been remediated.')

# Main function
def main():
    check_rule_changes()

if __name__ == '__main__':
    main()
