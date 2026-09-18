import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def generate_synthetic_view(image_path, distance_cm=100.0, angle_deg=22.5, f=1000.0):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    # 1. Define the 4 corners of our original flat image (Source Points)
    src_pts = np.float32([
        [0, 0],     # Top-Left
        [w, 0],     # Top-Right
        [0, h],     # Bottom-Left
        [w, h]      # Bottom-Right
    ])
    
    # 2. 3D Rotation Physics
    # The physical port is a 40cm x 40cm square. 
    # Center is (0,0), so edges are 20cm away from the center.
    theta = math.radians(angle_deg)
    half_size = 20.0 
    
    # If the camera moves to the right, the right edge of the port is closer to the lens (-Z)
    # and the left edge of the port is further away from the lens (+Z).
    Z_left = distance_cm + half_size * math.sin(theta)
    Z_right = distance_cm - half_size * math.sin(theta)
    
    X_left = -half_size * math.cos(theta)
    X_right = half_size * math.cos(theta)
    
    Y_top = -half_size
    Y_bottom = half_size
    
    # 3. Pinhole Camera Projection (X_screen = f * X / Z)
    # Top-Left & Bottom-Left
    x_tl = (f * X_left) / Z_left
    y_tl = (f * Y_top) / Z_left
    x_bl = (f * X_left) / Z_left
    y_bl = (f * Y_bottom) / Z_left
    
    # Top-Right & Bottom-Right
    x_tr = (f * X_right) / Z_right
    y_tr = (f * Y_top) / Z_right
    x_br = (f * X_right) / Z_right
    y_br = (f * Y_bottom) / Z_right
    
    # Shift the origin from the center (0,0) to the top-left of our image frame (w/2, h/2)
    dst_pts = np.float32([
        [x_tl + w/2, y_tl + h/2],
        [x_tr + w/2, y_tr + h/2],
        [x_bl + w/2, y_bl + h/2],
        [x_br + w/2, y_br + h/2]
    ])
    
    # 4. Generate Homography and Warp
    H = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped_img = cv2.warpPerspective(img, H, (w, h), borderValue=(255, 255, 255))
    cv2.imwrite("synthetic_perspective.png", warped_img)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Original Frontal View")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB))
    plt.title(f"Synthetic View (Right {angle_deg}°)")
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig("part_c_result.png")
    print("Comparison saved to part_c_result.png")

if __name__ == "__main__":
    generate_synthetic_view("reference_port.png")
