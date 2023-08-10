import boto3

session = boto3.Session(profile_name="default")
client = session.client("s3")

response = client.list_objects(Bucket="reko-sun")

for key in response["Contents"]:
    print(key["Key"])
