import cv2
import numpy as np
import math
from scipy import ndimage

def get_centers(image_path):
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise ValueError(f"Could not load {image_path}")
        
    # --- 1. Find Global Center (Using Canny for the thin squares) ---
    edges = cv2.Canny(gray, 50, 200)
    cnts, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    square_centroids = []
    for cnt in cnts:
        if cv2.contourArea(cnt) < 100: continue
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            M = cv2.moments(cnt)
            if M['m00'] > 0:
                square_centroids.append((int(M['m10']/M['m00']), int(M['m01']/M['m00'])))
                
    global_center = np.mean(square_centroids, axis=0).astype(int)
    
    # --- 2. Find Marker Center (Using Morphology for the thick circle) ---
    # Step A: Threshold to isolate all black pixels (circle + lines)
    mask = cv2.inRange(gray, 0, 10)
    
    # Step B: Morphological Opening (Erosion followed by Dilation)
    kernel = np.ones((7, 7), np.uint8)
    opened_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Step C: Find contours of the surviving blobs
    circ_cnts, _ = cv2.findContours(opened_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not circ_cnts:
        raise ValueError("Morphology destroyed all targets! Is the circle missing?")
        
    circle_cnt = max(circ_cnts, key=cv2.contourArea)
    M = cv2.moments(circle_cnt)
    marker_center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
    
    return tuple(global_center), tuple(marker_center)

def calculate_angle(global_center, marker_center):
    dx = marker_center[0] - global_center[0]
    dy = marker_center[1] - global_center[1]
    angle_rad = math.atan2(dy, dx)
    return math.degrees(angle_rad)

def test_rotation_recovery(image_path, test_angle=60.0):
    g_center, m_center = get_centers(image_path)
    ref_angle = calculate_angle(g_center, m_center)
    print(f"Reference Angle: {ref_angle:.2f} degrees")
    
    original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    rotated_img = ndimage.rotate(original_img, test_angle, reshape=True, cval=255)
    
    temp_path = "temp_rotated.png"
    cv2.imwrite(temp_path, rotated_img)
    
    rot_g_center, rot_m_center = get_centers(temp_path)
    rot_angle = calculate_angle(rot_g_center, rot_m_center)
    print(f"\nRotated Angle: {rot_angle:.2f} degrees")
    
    recovered_angle = (rot_angle - ref_angle) % 360
    if recovered_angle != 0:
        recovered_angle = 360 - recovered_angle
        
    print(f"\nApplied Rotation:  {test_angle} degrees")
    print(f"Recovered Rotation: {recovered_angle:.2f} degrees")
    
if __name__ == "__main__":
    test_rotation_recovery("reference_port.png", test_angle=60.0)
