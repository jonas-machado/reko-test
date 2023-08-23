import boto3

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import base64
import uuid
import tempfile
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/processImage", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]

    collectionId = "sun-reko-collection"

    threshold = 70
    maxFaces = 100

    client = boto3.client("rekognition")

    session = boto3.Session(profile_name="default")
    s3 = session.client("s3")

    response = client.search_faces_by_image(
        CollectionId=collectionId,
        Image={"Bytes": image_file.read()},
        # Image={"S3Object": {"Bucket": bucket, "Name": fileName}},
        FaceMatchThreshold=threshold,
        MaxFaces=maxFaces,
    )
    faceMatches = response["FaceMatches"]
    print("Matching faces")
    faces = []
    for match in faceMatches:
        print("FaceId:" + match["Face"]["FaceId"])
        print("Similarity: " + "{:.2f}".format(match["Similarity"]) + "%")
        print(match["Face"]["ExternalImageId"])
        response = s3.get_object(
            Bucket="reko-sun", Key=match["Face"]["ExternalImageId"]
        )
        print(response)
        image_data = response["Body"].read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        faces.append(image_base64)
    return jsonify({"faceMatches": faceMatches, "Images": faces})
    # return jsonify({"status": "ok"}), 200


@app.route("/listObjects", methods=["GET"])
def process_bucket():
    session = boto3.Session(profile_name="default")
    s3 = session.client("s3")
    bucket = "reko-sun"
    response = s3.list_objects(Bucket=bucket)
    print(response)
    faceMatches = response["Contents"]
    faces = []
    for match in faceMatches:
        response = s3.get_object(Bucket="reko-sun", Key=match["Key"])
        print(response)
        image_data = response["Body"].read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        faces.append(image_base64)
    return jsonify({"status": "ok", "Images": faces})


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


@app.route("/upload", methods=["POST"])
def upload_image():
    session = boto3.Session(profile_name="default")
    s3 = session.client("s3")

    collection_id = "sun-reko-collection"
    bucket_name = "reko-sun"

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    faces_indexed = []
    uploaded_files = request.files.getlist("image")

    for image in uploaded_files:
        filename = image.filename
        random_image_name = str(uuid.uuid4()) + filename
        print(random_image_name)

        # Create a temporary file to write the image content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name
            temp_file.write(image.read())

        # Upload the temporary file to S3
        s3.upload_file(temp_filename, bucket_name, random_image_name)

        # Remove the temporary file
        os.remove(temp_filename)

        indexed_faces_count = add_faces_to_collection(
            bucket_name, random_image_name, collection_id
        )
        faces_indexed.append("Faces indexed count: " + str(indexed_faces_count))

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
