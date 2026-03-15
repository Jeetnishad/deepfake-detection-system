from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading
from predict import predict_video

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

processing_status = {
    "processing": False,
    "result": None
}


@app.route("/")
def home():
    return jsonify({"message": "Deepfake Detection API Running"})


def process_video(filepath):

    global processing_status

    try:
        processing_status["processing"] = True
        processing_status["result"] = None

        result = predict_video(filepath)

        processing_status["result"] = result

    except Exception as e:
        processing_status["result"] = {"error": str(e)}

    finally:
        processing_status["processing"] = False

        # optional cleanup (delete uploaded video)
        if os.path.exists(filepath):
            os.remove(filepath)


@app.route("/detect", methods=["POST"])
def detect():

    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files["video"]

    filename = file.filename or "uploaded_video.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    thread = threading.Thread(target=process_video, args=(filepath,))
    thread.start()

    return jsonify({"message": "Processing started"})


@app.route("/status")
def status():
    return jsonify(processing_status)


import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)