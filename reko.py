import boto3

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import base64
import uuid
import tempfile

from handleDB import Reference

# SQL imports

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

import os
from dotenv import load_dotenv

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()

dialect = os.getenv("DIALECT")
driver = os.getenv("DRIVER")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database_name = os.getenv("DATABASE_NAME")

# Replace with your database details
DATABASE_URI = (
    dialect
    + "+"
    + driver
    + "://"
    + username
    + ":"
    + password
    + "@"
    + host
    + ":"
    + port
    + "/"
    + database_name
)

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URI)


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
        image_data = response["Body"].read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        faces.append(image_base64)
    return jsonify({"faceMatches": faceMatches, "Images": faces}), 200


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
    return jsonify({"status": "ok", "Images": faces}), 200


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

    client = boto3.client("rekognition")

    collection_id = "sun-reko-collection"
    bucket_name = "reko-sun"
    
    threshold = 70
    maxFaces = 100

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

        # Remove the temporary file

        response = client.search_faces_by_image(
            CollectionId=collection_id,
            Image={"Bytes": image.read()},
            # Image={"S3Object": {"Bucket": bucket, "Name": fileName}},
            FaceMatchThreshold=threshold,
            MaxFaces=maxFaces,
        )
            
        faceMatches = response["FaceMatches"]

        for match in faceMatches:
            print("FaceId:" + match["Face"]["FaceId"])
            print("Similarity: " + "{:.2f}".format(match["Similarity"]) + "%")
            print(match["Face"]["ExternalImageId"])
            image_id = match["Face"]["ExternalImageId"]
            stmt = select(Reference).where(Reference.image == image_id)
            result = session.scalars(stmt)

            for user_image in result:
                print(user_image)

            image_data = response["Body"].read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            s3.upload_file(temp_filename, bucket_name, random_image_name)
            #faces.append(image_base64)

        os.remove(temp_filename)


    return jsonify({"status": "ok"}), 200


@app.route("/reference", methods=["POST"])
def reference_client():
    session = boto3.Session(profile_name="default")
    s3 = session.client("s3")

    fullname = request.form["name"]
    email = request.form["email"]
    instagram = request.form["instagram"]
    country = int(request.form["country"])
    tel = int(request.form["tel"])

    collection_id = "sun-reko-collection"
    bucket_name = "reko-sun"

    uploaded_image = request.files["image"]

    filename = uploaded_image.filename
    random_image_name = str(uuid.uuid4()) + filename

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        uploaded_image.save(temp_filename)

    root, extension = os.path.splitext(filename)

    s3.upload_file(temp_filename, bucket_name, "register/" + fullname + extension)

    indexed_faces_count = add_faces_to_collection(
        bucket_name, random_image_name, collection_id
    )

    print(uploaded_image)
    with Session(engine) as session:
        reference = Reference(
            fullname=fullname,
            email=email,
            instagram=instagram,
            country=country,
            tel=tel,
            image=fullname + extension,
        )
        session.add(reference)
        session.commit()

    os.remove(temp_filename)

    return jsonify({"status": "ok"}), 200


@app.route("/login", methods=["POST"])
def login_client():
    email = request.json["email"]
    session = Session(engine)
    stmt = select(Reference).where(Reference.email == email)
    for user in session.scalars(stmt):
        if user:
            print(f"{user}")
            return jsonify({"auth": True}), 200
    return jsonify({"auth": False}), 403


if __name__ == "__main__":
    app.run(debug=True)
