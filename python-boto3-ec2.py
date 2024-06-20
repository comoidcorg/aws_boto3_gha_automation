import os
import logging
import boto3

def create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    instances = ec2_client.run_instances(
        ImageId="ami-033fabdd332044f06",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="testkp",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'AppName1'
                },
            ]
        },
    ],
    )

    print(instances["Instances"][0]["InstanceId"])
    print(instances["Instances"][0]["PrivateIpAddress"])
    print(instances)

## using boto3.resoreces
# def create_ec2():
#    ec2_c = boto3.resource('ec2', region_name="us-east-2")
#    instances_2 = ec2_c.create_instances(
#        ImageId="ami-033fabdd332044f06",
#         MinCount=1,
#         MaxCount=1,
#         InstanceType="t2.micro",
#         KeyName="testkp"
#     )
   
#    #print(instances_2["Instances"][0]["InstanceId"])
#    print(instances_2)

if __name__ == '__main__':
    create_instance()
   # create_ec2()