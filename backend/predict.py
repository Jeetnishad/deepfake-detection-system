import numpy as np
import tensorflow as tf

from utils.video_processor import extract_frames
from utils.face_extractor import extract_faces

# model initially None
model: tf.keras.Model | None = None


def load_model():
    global model

    if model is None:
        print("Loading deepfake model...")
        model = tf.keras.models.load_model(
            "deepfake_model.h5",
            compile=False
        )
        print("Model loaded successfully")


def predict_video(video_path):

    global model

    # ensure model is loaded
    if model is None:
        load_model()

    frames = extract_frames(video_path)

    fake_count = 0
    real_count = 0
    face_found = False
    all_faces = []

    # collect faces
    for frame in frames:

        faces = extract_faces(frame)

        for face in faces:
            face_found = True
            face = face / 255.0
            all_faces.append(face)

    if not face_found:
        return {
            "result": "NO FACE DETECTED",
            "confidence": 0,
            "fake_frames": 0,
            "real_frames": 0
        }

    # convert to numpy array
    all_faces = np.array(all_faces)

    # prediction
    predictions = model.predict(all_faces, batch_size=32, verbose=0)

    for pred in predictions:

        if pred[0] > 0.7:
            fake_count += 1
        else:
            real_count += 1

    total_frames = fake_count + real_count

    confidence = int((max(fake_count, real_count) / total_frames) * 100)

    if fake_count > real_count:
        label = "DEEPFAKE VIDEO"
    else:
        label = "REAL VIDEO"

    return {
        "result": label,
        "confidence": confidence,
        "fake_frames": fake_count,
        "real_frames": real_count
    }