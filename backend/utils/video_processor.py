import cv2

def extract_frames(video_path, frame_skip=10):

    frames = []

    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Skip frames to speed up processing
        if frame_count % frame_skip == 0:
            frames.append(frame)

        frame_count += 1

    cap.release()

    return frames