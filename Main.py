import numpy as np
import cv2

# ========== COMPLETE CANNY EDGE DETECTION ==========
def canny_edge_detection(image, low_threshold=50, high_threshold=150):
    # STEP 1: Noise Reduction - Gaussian Blur
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
    # STEP 2: Gradient Calculation - Sobel Operators
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    grad_direction = np.arctan2(grad_y, grad_x)
    
    # STEP 3: Non-Maximum Suppression
    M, N = grad_magnitude.shape
    suppressed = np.zeros((M, N), dtype=np.float32)
    angle = grad_direction * 180. / np.pi
    angle[angle < 0] += 180
    
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            q, r = 255, 255
            
            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                q, r = grad_magnitude[i, j + 1], grad_magnitude[i, j - 1]
            elif (22.5 <= angle[i, j] < 67.5):
                q, r = grad_magnitude[i + 1, j - 1], grad_magnitude[i - 1, j + 1]
            elif (67.5 <= angle[i, j] < 112.5):
                q, r = grad_magnitude[i + 1, j], grad_magnitude[i - 1, j]
            elif (112.5 <= angle[i, j] < 157.5):
                q, r = grad_magnitude[i - 1, j - 1], grad_magnitude[i + 1, j + 1]
            
            if grad_magnitude[i, j] >= q and grad_magnitude[i, j] >= r:
                suppressed[i, j] = grad_magnitude[i, j]
    
    # STEP 4: Double Threshold
    strong = 255
    weak = 75
    strong_edges = np.zeros_like(suppressed, dtype=np.uint8)
    weak_edges = np.zeros_like(suppressed, dtype=np.uint8)
    
    strong_edges[suppressed >= high_threshold] = strong
    weak_edges[(suppressed >= low_threshold) & (suppressed < high_threshold)] = weak
    
    # STEP 5: Edge Tracking by Hysteresis
    result = np.copy(strong_edges)
    
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            if weak_edges[i, j] == weak:
                if ((result[i+1, j-1] == strong) or (result[i+1, j] == strong) or 
                    (result[i+1, j+1] == strong) or (result[i, j-1] == strong) or 
                    (result[i, j+1] == strong) or (result[i-1, j-1] == strong) or 
                    (result[i-1, j] == strong) or (result[i-1, j+1] == strong)):
                    result[i, j] = strong
    
    return result


# ========== MAIN CAMERA APPLICATION ==========
def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Press 'q' to quit")
    print("Press '+' to increase high threshold")
    print("Press '-' to decrease high threshold")
    
    low_threshold = 10
    high_threshold = 150
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = canny_edge_detection(gray, low_threshold, high_threshold)
        
        # Display side by side
        display_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        display_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        combined = np.hstack((display_frame, display_edges))
        
        # Add threshold info
        text = f"Low: {low_threshold} | High: {high_threshold}"
        cv2.putText(combined, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Original | Canny Edges', combined)
        
        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+'):
            high_threshold = min(255, high_threshold + 10)
            print(f"High threshold: {high_threshold}")
        elif key == ord('-'):
            high_threshold = max(low_threshold + 10, high_threshold - 10)
            print(f"High threshold: {high_threshold}")
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()