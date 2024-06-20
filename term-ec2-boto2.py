
import os
import logging
import boto3

# commented to test without function

def terminate_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)

if __name__ == '__main__':
    terminate_instance("i-013174267b7e22924")

#Working without function 

# ec2_client = boto3.client("ec2", region_name="us-east-2")
# response = ec2_client.terminate_instances(InstanceIds=["i-0d82bd9b613835b4c"])
# print(response)

