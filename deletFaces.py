# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3


def delete_faces_from_collection(collection_id, faces):
    session = boto3.Session(profile_name="default")
    client = session.client("rekognition")
    response = client.delete_faces(CollectionId=collection_id, FaceIds=faces)

    print(str(len(response["DeletedFaces"])) + " faces deleted:")
    for faceId in response["DeletedFaces"]:
        print(faceId)
    return len(response["DeletedFaces"])


def main():
    maxResults = 2
    faces_count = 0
    tokens = True
    collection_id = "sun-reko-collection"

    session = boto3.Session(profile_name="default")
    client = session.client("rekognition")
    response = client.list_faces(CollectionId=collection_id, MaxResults=maxResults)

    print("Faces in collection " + collection_id)

    faces = []
    while tokens:
        faces = response["Faces"]

        for face in faces:
            faces_count += 1
            faces.append(face["FaceId"])

    print(faces)
    # faces_count = delete_faces_from_collection(collection_id, faces)
    # print("deleted faces count: " + str(faces_count))


if __name__ == "__main__":
    main()
