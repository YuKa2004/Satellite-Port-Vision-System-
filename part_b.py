import cv2
from part_a import get_centers

def get_reference_vector(image_path):
    # Process the original uncropped image to find the exact spacing
    g_center, m_center = get_centers(image_path)
    
    # Calculate the fixed pixel distance between the square center and circle
    dx = m_center[0] - g_center[0]
    dy = m_center[1] - g_center[1]
    
    return dx, dy

def recover_target(crop_w, crop_h, crop_g_center, ref_vector, step_size=20):
    dx, dy = ref_vector
    
    # Project where the circle SHOULD be in our cropped frame
    target_x = crop_g_center[0] + dx
    target_y = crop_g_center[1] + dy
    
    print(f"Crop Frame Size: {crop_w}x{crop_h}")
    print(f"Projected Circle Coordinate: ({target_x}, {target_y})")
    print("-" * 40)
    
    steps = 0
    # We pad by 20 pixels to ensure the whole circle is visible, not just the center point
    padding = 20 
    
    while True:
        is_visible_x = (padding <= target_x <= crop_w - padding)
        is_visible_y = (padding <= target_y <= crop_h - padding)
        
        if is_visible_x and is_visible_y:
            print(f"Step {steps}: Target is fully visible in frame!")
            break
            
        steps += 1
        command = f"Step {steps}: "
        
        # If the target is to the right of the frame, the camera must pan RIGHT.
        # Moving the camera right causes objects in the frame to shift left (x decreases).
        if not is_visible_x:
            if target_x > crop_w - padding:
                command += f"Pan RIGHT {step_size}px. "
                target_x -= step_size
            elif target_x < padding:
                command += f"Pan LEFT {step_size}px. "
                target_x += step_size
                
        # Similarly for Tilt (Y-axis points down, so higher Y means lower physically)
        if not is_visible_y:
            if target_y > crop_h - padding:
                command += f"Tilt DOWN {step_size}px. "
                target_y -= step_size
            elif target_y < padding:
                command += f"Tilt UP {step_size}px. "
                target_y += step_size
                
        print(command)

if __name__ == "__main__":
    # 1. Learn the fixed vector from the full reference image
    ref_vec = get_reference_vector("reference_port.png")
    
    # Simulate a crop where the global center of the squares is projected to be off-screen at (450, 450)
    # The crop window is 400x400
    recover_target(crop_w=400, crop_h=400, crop_g_center=(450, 450), ref_vector=ref_vec, step_size=50)
