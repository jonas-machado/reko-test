import boto3

# Initialize the Amazon Rekognition client
session = boto3.Session(profile_name="Jonas Machado")
rekognition_client = session.client("rekognition")

# Specify the collection name
collection_id = "sun-reko-collection"

# Create the collection
response = rekognition_client.create_collection(CollectionId=collection_id)

# Print the response
print(response)
