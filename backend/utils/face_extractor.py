import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def extract_faces(frame):

    face_images = []

    if frame is None:
        return face_images

    # Resize frame for faster detection
    frame_small = cv2.resize(frame, (640, 360))

    gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        face = frame_small[y:y+h, x:x+w]

        try:
            face = cv2.resize(face, (128, 128))
            face = face / 255.0
            face_images.append(face)
        except:
            continue

    return face_images