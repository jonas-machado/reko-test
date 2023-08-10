# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3


def add_faces_to_collection(bucket, photo, collection_id):
    session = boto3.Session(profile_name="default")
    client = session.client("rekognition")

    response = client.index_faces(
        CollectionId=collection_id,
        Image={"S3Object": {"Bucket": bucket, "Name": photo}},
        ExternalImageId=photo,
        MaxFaces=1,
        QualityFilter="AUTO",
        DetectionAttributes=["ALL"],
    )

    print("Results for " + photo)
    print("Faces indexed:")
    for faceRecord in response["FaceRecords"]:
        print("  Face ID: " + faceRecord["Face"]["FaceId"])
        print("  Location: {}".format(faceRecord["Face"]["BoundingBox"]))

    print("Faces not indexed:")
    for unindexedFace in response["UnindexedFaces"]:
        print(" Location: {}".format(unindexedFace["FaceDetail"]["BoundingBox"]))
        print(" Reasons:")
        for reason in unindexedFace["Reasons"]:
            print("   " + reason)
    return len(response["FaceRecords"])


def main():
    collection_id = "sun-reko-collection"
    bucket = "reko-sun"
    photo = "021718ce-68da-4417-a0cb-719639e1e365.jpg"
    session = boto3.Session(profile_name="default")
    client = session.client("s3")

    response = client.list_objects(Bucket="reko-sun")

    for key in response["Contents"]:
        print(key["Key"])

        indexed_faces_count = add_faces_to_collection(bucket, key["Key"], collection_id)
        print("Faces indexed count: " + str(indexed_faces_count))


if __name__ == "__main__":
    main()
