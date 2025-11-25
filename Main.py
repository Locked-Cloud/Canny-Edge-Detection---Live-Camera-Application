import cv2
import numpy as np
from skimage.color import rgb2gray

#SOBEL 
def sobel(frame):
    gray = rgb2gray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    gradient_magnitude *= 255.0 / gradient_magnitude.max()
    
    return gradient_magnitude.astype(np.uint8)
# CANNY
def Canny_edge_detection(frame, low_threshold=30, high_threshold=60):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    gx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)

    mag = np.hypot(gx, gy)
    mag = (mag / mag.max()) * 255
    ang = np.degrees(np.arctan2(gy, gx))
    ang[ang < 0] += 180

    M, N = mag.shape
    Z = np.zeros((M, N), dtype=np.float32)

    # Non-Max Suppression 
    for i in range(1, M-1):
        for j in range(1, N-1):
            angle = ang[i, j]

            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                q, r = mag[i, j+1], mag[i, j-1]
            elif 22.5 <= angle < 67.5:
                q, r = mag[i+1, j-1], mag[i-1, j+1]
            elif 67.5 <= angle < 112.5:
                q, r = mag[i+1, j], mag[i-1, j]
            else:
                q, r = mag[i-1, j-1], mag[i+1, j+1]

            if mag[i, j] >= q and mag[i, j] >= r:
                Z[i, j] = mag[i, j]

    # Double Threshold using + / - values 
    strong, weak = 255, 75
    res = np.zeros_like(Z, dtype=np.uint8)

    res[Z >= high_threshold] = strong
    res[(Z < high_threshold) & (Z >= low_threshold)] = weak

    #Hysteresis 
    result = res.copy()
    for i in range(1, M-1):
        for j in range(1, N-1):
            if result[i, j] == weak:
                if strong in result[i-1:i+2, j-1:j+2]:
                    result[i, j] = strong
                else:
                    result[i, j] = 0

    return result

#MAIN
cap = cv2.VideoCapture(0)
mode = None

high_threshold = 60
low_threshold = 30

cv2.namedWindow("Live Camera")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    key = cv2.waitKey(1) & 0xFF

    # ---- Change modes ----
    if key == ord('s'):
        mode = 'sobel'
    elif key == ord('c'):
        mode = 'canny'
    elif key == ord('n'):
        mode = None
    elif key == ord('q'):
        break

    #Change Canny Threshold
    if key == ord('+'):
        high_threshold = min(255, high_threshold + 10)
        print(f"High threshold: {high_threshold}")

    elif key == ord('-'):
        high_threshold = max(low_threshold + 10, high_threshold - 10)
        print(f"High threshold: {high_threshold}")

    #MODE
    if mode == 'sobel':
        output = sobel(frame)

    elif mode == 'canny':
        output = Canny_edge_detection(frame, low_threshold, high_threshold)

    else:
        output = frame

    cv2.imshow("Live Camera", output)

cap.release()
cv2.destroyAllWindows()