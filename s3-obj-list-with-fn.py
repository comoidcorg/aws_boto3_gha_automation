import boto3

def my_bucket(bkt_name):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bkt_name)

    for obj in bucket.objects.all():
        print(obj.key, obj.last_modified)

if __name__ == '__main__':
    my_bucket("testb31234511")