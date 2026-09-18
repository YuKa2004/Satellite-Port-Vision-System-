import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from part_a import get_centers

def visualize_servoing(ax, image_path, start_frame_x, start_frame_y, frame_w, frame_h, step_size=25):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    _, m_center = get_centers(image_path)
    target_abs_x, target_abs_y = m_center
    
    current_x = start_frame_x
    current_y = start_frame_y
    frames_to_plot = [(current_x, current_y)]
    
    padding = 20
    steps = 0
    
    while True:
        rel_x = target_abs_x - current_x
        rel_y = target_abs_y - current_y
        
        is_visible_x = (padding <= rel_x <= frame_w - padding)
        is_visible_y = (padding <= rel_y <= frame_h - padding)
        
        if is_visible_x and is_visible_y:
            break
            
        if not is_visible_x:
            if rel_x > frame_w - padding: current_x += step_size
            elif rel_x < padding: current_x -= step_size
                
        if not is_visible_y:
            if rel_y > frame_h - padding: current_y += step_size
            elif rel_y < padding: current_y -= step_size
                
        frames_to_plot.append((current_x, current_y))
        steps += 1
        if steps > 50: # Safety break
            break
            
    ax.imshow(img_rgb)
    
    for i, (fx, fy) in enumerate(frames_to_plot):
        if i == 0: 
            color, label = 'red', "Start"
        elif i == len(frames_to_plot) - 1: 
            color, label = 'green', "Found"
        else: 
            color, label = 'orange', ""
            
        rect = patches.Rectangle((fx, fy), frame_w, frame_h, linewidth=2, 
                                 edgecolor=color, facecolor='none', 
                                 linestyle='--' if color != 'green' else '-')
        ax.add_patch(rect)
        if label:
            ax.text(fx + 5, fy + 20, label, color=color, fontsize=10, weight='bold', 
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
    ax.scatter(target_abs_x, target_abs_y, c='magenta', s=100, marker='x')
    ax.set_title(f"Start: ({start_frame_x}, {start_frame_y}) | Total Steps: {steps}")
    ax.axis('off')

if __name__ == "__main__":
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    
    # Run the test from the 4 extreme corners of the original image
    visualize_servoing(axs[0, 0], "reference_port.png", 50, 50, 100, 100)      # Top-Left
    visualize_servoing(axs[0, 1], "reference_port.png", 450, 50, 100, 100)     # Top-Right
    visualize_servoing(axs[1, 0], "reference_port.png", 50, 450, 100, 100)     # Bottom-Left
    visualize_servoing(axs[1, 1], "reference_port.png", 450, 450, 100, 100)    # Bottom-Right
    
    plt.tight_layout()
    plt.savefig("servoing_4cases.png")
    print("Saved to servoing_4cases.png")
