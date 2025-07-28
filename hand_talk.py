import cv2
from hand_gesture_recognizer import HandGestureRecognizer
from utils.text_to_speech import speak

cap = cv2.VideoCapture(0)
recognizer = HandGestureRecognizer()
last_spoken = None
display_text = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gesture = recognizer.detect(frame)

    # Speak and update text only if gesture is new and not empty
    if gesture and gesture != last_spoken:
        speak(gesture)
        last_spoken = gesture
        display_text = gesture
    elif gesture == "":
        last_spoken = None
        display_text = ""

    # Display the recognized text on the frame
    if display_text:
        cv2.putText(frame, display_text, (50, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 0), 4, cv2.LINE_AA)

    cv2.imshow("HandTalk - Real-Time Sign Language", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
