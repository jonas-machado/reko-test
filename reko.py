import boto3

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
cors = CORS(app, resources={r"/processImage/*": {"origins": "*"}})


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
    return jsonify({"faceMatches": faceMatches, "Images": faces})
    # return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
