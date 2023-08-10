import boto3
import uuid

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIA2XIZD3BZDXJERGZY",
    aws_secret_access_key="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",
)

bucket_name = "reko-sun"


local_image_path = "assets/test.png"
print(local_image_path)

random_image_name = str(uuid.uuid4()) + ".jpg"
s3.upload_file(local_image_path, bucket_name, random_image_name)

# for image in local_image_path:
#     random_image_name = str(uuid.uuid4()) + ".jpg"
#     s3.upload_file(image, bucket_name, random_image_name)
