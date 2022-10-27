import cv2
import numpy as np
from matplotlib import pyplot as plt
def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)
while True:
    _, trian = cap.read()
    hsv = cv2.cvtColor(trian, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    for contour in contours:
        if i == 0:
            i = 1
            continue
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(trian, [contour], 0, (0, 0, ), 5)
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            if len(approx) == 3:
                cv2.putText(trian, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))
            else:
                cv2.putText(trian, 'No', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))
    cv2.imshow("trian", trian)
    key = cv2.waitKey(1)
    if key == 27:
            break
cap.release()
cv2.destroyAllWindows()