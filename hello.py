import boto3
import uuid

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIA2XIZD3BZDXJERGZY",
    aws_secret_access_key="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",
)

bucket_name = "sun-test-photo"


local_image_path = [
    "assets/1.jpeg",
    "assets/2.jpeg",
    "assets/3.jpeg",
    "assets/4.jpeg",
    "assets/5.jpeg",
    "assets/6.jpeg",
    "assets/7.jpeg",
    "assets/8.jpeg",
    "assets/9.jpeg",
    "assets/10.jpeg",
    "assets/11.webp",
    "assets/12.webp",
]

for image in local_image_path:
    random_image_name = str(uuid.uuid4()) + ".jpg"
    s3.upload_file(image, bucket_name, random_image_name)
