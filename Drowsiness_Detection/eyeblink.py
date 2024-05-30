from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2 
import time

mixer.init()
mixer.music.load("music.wav")

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def draw_text(frame, text, position, color=(255, 255, 255), font_scale=1, thickness=2):
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

def color_feedback(ear, frame):
    color = (0, 255, 0)  # Default color: green (not drowsy)
    if ear < 0.2:
        color = (0, 0, 255)  # Red: indicating high drowsiness
    elif ear < 0.3:
        color = (0, 165, 255)  # Orange: indicating moderate drowsiness
    cv2.rectangle(frame, (0, 0), (200, 30), color, -1)
    cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

def voice_alert():
    # Add your voice alert mechanism here
    pass

threshold_adjustment_factor = 0.02
max_threshold = 0.5
min_threshold = 0.1

def adjust_threshold(current_threshold, action):
    if action == 'increase':
        return min(current_threshold + threshold_adjustment_factor, max_threshold)
    elif action == 'decrease':
        return max(current_threshold - threshold_adjustment_factor, min_threshold)
    else:
        return current_threshold

drowsiness_history = []

def add_timestamp_to_history():
    drowsiness_history.append(time.strftime("%Y-%m-%d %H:%M:%S"))

thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = cv2.VideoCapture(0)
flag = 0 
drowsy_count = 0
drowsy_threshold = 0.25

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        color_feedback(ear, frame)

        if ear < drowsy_threshold:
            flag += 1
            if flag >= frame_check:
                drowsy_count += 1
                add_timestamp_to_history()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame, "****************ALERT!****************", (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
                cv2.putText(frame, f"Drowsiness detected at: {timestamp}", (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                mixer.music.play()
                voice_alert()
                
                # Capture and save the photo
                cv2.imwrite("alert_photo.jpg", frame)
        else:
            flag = 0

    draw_text(frame, f"Drowsy Count: {drowsy_count}", (10, 90))

    draw_text(frame, "Press 'i' to increase threshold, 'd' to decrease.", (10, 200))
    draw_text(frame, f"Current Threshold: {drowsy_threshold:.2f}", (10, 230))

    history_text = "Drowsiness History:\n"
    for i, timestamp in enumerate(drowsiness_history[-5:]):
        history_text += f"{i+1}. {timestamp}\n"
    cv2.putText(frame, history_text, (10, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Drowsiness Detection", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("i"):
        drowsy_threshold = adjust_threshold(drowsy_threshold, 'increase')
    elif key == ord("d"):
        drowsy_threshold = adjust_threshold(drowsy_threshold, 'decrease')

cv2.destroyAllWindows()
cap.release() 
