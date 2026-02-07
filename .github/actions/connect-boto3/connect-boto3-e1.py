import os
import time
import logging
import boto3
from botocore.exceptions import ClientError


def create_connect_and_admin():
    alias = os.environ['INPUT_CONNECT_ALIAS']
    region = os.environ['INPUT_CONNECT_REGION']
    admin_user = os.environ['INPUT_ADMIN_USERNAME']
    admin_password = os.environ['INPUT_ADMIN_PASSWORD']

    connect = boto3.client('connect', region_name=region)

    try:
        # 1. Create Connect instance
        response = connect.create_instance(
            IdentityManagementType='CONNECT_MANAGED',
            InstanceAlias=alias,
            InboundCallsEnabled=True,
            OutboundCallsEnabled=True
        )
        instance_id = response['Id']

        # 2. Wait until ACTIVE (no native waiter → manual poll)
        while True:
            status = connect.describe_instance(InstanceId=instance_id)['Instance']['InstanceStatus']
            if status == 'ACTIVE':
                break
            time.sleep(15)

        # 3. Get access URL
        access_url = connect.describe_instance(
            InstanceId=instance_id
        )['Instance']['AccessUrl']

        # 4. Get Admin security profile
        profiles = connect.list_security_profiles(InstanceId=instance_id)
        admin_profile_id = next(
            p['Id'] for p in profiles['SecurityProfileSummaryList']
            if p['Name'] == 'Admin'
        )

        # 5. Get default routing profile
        routing_profiles = connect.list_routing_profiles(InstanceId=instance_id)
        routing_profile_id = routing_profiles['RoutingProfileSummaryList'][0]['Id']

        # 6. Create admin user
        connect.create_user(
            InstanceId=instance_id,
            Username=admin_user,
            Password=admin_password,
            IdentityInfo={
                'FirstName': 'Admin',
                'LastName': 'User'
            },
            PhoneConfig={
                'PhoneType': 'SOFT_PHONE',
                'AutoAccept': True
            },
            SecurityProfileIds=[admin_profile_id],
            RoutingProfileId=routing_profile_id
        )

        # 7. GitHub outputs
        with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_output:
            print(f'ConnectInstanceId={instance_id}', file=gh_output)
            print(f'ConnectAccessUrl={access_url}', file=gh_output)
            print(f'AdminUsername={admin_user}', file=gh_output)

    except ClientError as e:
        logging.error(e)
        return False

    return True


if __name__ == '__main__':
    create_connect_and_admin()
