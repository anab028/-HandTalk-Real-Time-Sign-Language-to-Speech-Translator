import mediapipe as mp
import cv2

class HandGestureRecognizer:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(image_rgb)

        gesture = ""
        fingers = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )

                # Thumb (check horizontal)
                if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x < \
                   hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_IP].x:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers (check vertical)
                tips = [mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP,
                        mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP,
                        mp.solutions.hands.HandLandmark.RING_FINGER_TIP,
                        mp.solutions.hands.HandLandmark.PINKY_TIP]
                for tip in tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = sum(fingers)

                # Improved gesture logic
                if fingers == [0, 1, 0, 0, 0]:
                    gesture = "Hello"
                elif fingers == [0, 1, 1, 0, 0]:
                    gesture = "Peace"
                elif total_fingers == 0:
                    gesture = ""
                elif total_fingers == 5:
                    gesture = "Hi"
                elif fingers == [1, 0, 0, 0, 0]:
                    gesture = "Thumbs Up"
                elif fingers == [0, 0, 0, 0, 1]:
                    gesture = "Pinky"
                elif fingers == [1, 1, 0, 0, 1]:
                    gesture = "I Love You"
                else:
                    gesture = ""

        return gesture
