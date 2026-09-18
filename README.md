# Satellite Port Vision System 🛰️

This repository contains a full Computer Vision pipeline built to simulate a spacecraft interacting with a satellite port. The solution relies strictly on classical Computer Vision techniques (OpenCV)—including Morphological filtering, Image Moments, and Perspective Geometry (Homography)—bypassing the need for 3D graphics engines or deep learning models.

## Problem Statement

The system is designed to process a 2D image of a "satellite port" consisting of concentric squares (the port boundary) and a solid circular marker (an orientation vector). 

The pipeline solves four core spatial challenges:
1. **Rotation Angle Recovery**: Calculate the exact rotation angle of an arriving spacecraft. The system extracts the spatial vector between the geometric center of the port (found via Canny edge detection) and the circular marker (isolated via Morphological Opening).
2. **Visual Servoing (PTZ Camera Tracking)**: Given an arbitrarily cropped view of the port where the marker is completely off-screen, the system mathematically calculates the "phantom" target coordinate and outputs discrete Pan and Tilt camera commands to step the camera until the target is visible.
3. **Synthetic 3D Perspective**: Without using a 3D rendering engine, the pipeline mathematically generates a synthetic view of the port as if a camera had physically moved to the right and is looking back at the port from a 22.5° angle at a distance of 100cm (using Pinhole projection and 2D Homography).
4. **Inverse Orbital Servoing**: Starting strictly from the slanted 22.5° perspective image, the system computes the relative Inverse Homography matrices required to physically step the camera along an orbital arc, un-warping the image incrementally until it returns to a perfect 0° frontal view.

---

## File Structure

```text
.
├── part_a.py                 # (Core) Hybrid extraction pipeline. Uses Canny edges for squares and Morphological Opening to isolate the circular marker, calculating the rotational vector.
├── part_b.py                 # Computes relative coordinate offsets to issue step-by-step Pan/Tilt camera commands.
├── visualize_b.py            # A Matplotlib visual simulator that animates the camera frame iteratively hunting for the marker.
├── part_c.py                 # Computes 3D pinhole projections and uses 4-point Homography to warp the 2D image into a synthetic 3D perspective.
├── part_d.py                 # Implements inverse orbital servoing by composing relative Homography matrices to incrementally step the camera back to 0 degrees.
├── reference_port.png        # The input source image of the satellite port.
└── outputs/                  # Generated visualization artifacts:
    ├── servoing_4cases.png   # Output of the visual servoing algorithm starting from 4 extreme corners.
    ├── part_c_result.png     # The generated 22.5-degree perspective warp.
    └── part_d_servoing.png   # The frame-by-frame sequence of the camera orbiting back to center.
```

## Setup & Usage

1. Clone this repository and ensure the dependencies are installed:
   ```bash
   pip install opencv-python numpy matplotlib scipy
   ```
2. Run any of the individual scripts to see the console output and generate the corresponding visualization plot:
   ```bash
   python part_a.py
   python visualize_b.py
   python part_c.py
   python part_d.py
   ```
