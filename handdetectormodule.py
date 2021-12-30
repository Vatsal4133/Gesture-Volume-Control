import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode = False, maxHands = 2, modComp = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modComp = modComp
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mph = mp.solutions.hands
        self.mpD = mp.solutions.drawing_utils
        self.cap = self.mph.Hands(self.mode, self.maxHands, self.modComp,
                                  self.detectionCon, self.trackCon)

    def findHands(self , image, draw = True):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.cap.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpD.draw_landmarks(image, handLms, self.mph.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w ,c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 5, (0,255,255), cv2.FILLED)

        return lmList


def main():
    curTime = 0
    preTime = 0
    hand = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, image = hand.read()
        image = detector.findHands(image)
        lmList = detector.findPosition(image)
        if len(lmList)!= 0:
            print(lmList[4])
        curTime = time.time()
        fps = 1 / (curTime - preTime)
        preTime = curTime

        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2)
        cv2.imshow("IMAGE", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

if __name__ == "__main__":
    main()