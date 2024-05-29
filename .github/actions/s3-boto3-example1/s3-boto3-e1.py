import os
import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket():
    bucket_name = os.environ['INPUT_BUCKET']
    region = os.environ['INPUT_BUCKET-REGION']

    # Create bucket
    try:
        if region is None or region == 'us-east-1':
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        # elif region == "us-east-1":
        #      s3_client = boto3.client('s3')
        #      s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        
        with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_output:
            print(f'BucketnRegion={bucket_name} {region}', file=gh_output)

    except ClientError as e:
        logging.error(e)
        return False
    return True    
    

if __name__ == '__main__':
    create_bucket()