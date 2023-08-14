import boto3

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/processImage/*": {"origins": "*"}})


@app.route("/processImage", methods=["POST"])
def process_image():
    print(request.headers)
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]

    collectionId = "sun-reko-collection"

    threshold = 70
    maxFaces = 100

    client = boto3.client("rekognition")

    response = client.search_faces_by_image(
        CollectionId=collectionId,
        Image={"Bytes": image_file.read()},
        # Image={"S3Object": {"Bucket": bucket, "Name": fileName}},
        FaceMatchThreshold=threshold,
        MaxFaces=maxFaces,
    )
    faceMatches = response["FaceMatches"]
    print("Matching faces")
    for match in faceMatches:
        print("FaceId:" + match["Face"]["FaceId"])
        print("Similarity: " + "{:.2f}".format(match["Similarity"]) + "%")
        print(match["Face"])
    return jsonify({"ok": "success"}), 200


if __name__ == "__main__":
    app.run(debug=True)
