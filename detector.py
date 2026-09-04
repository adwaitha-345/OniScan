import cv2
import numpy as np


def detect_layers(image):
    if image is None:
        return 0, image

    # =========================================================
    # 1. PREPARE IMAGE & NORMALIZE
    # =========================================================
    image = cv2.resize(image, (600, 600))
    result = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # =========================================================
    # 2. ROBUST CONTRAST ENHANCEMENT & DENOISING
    # =========================================================
    # Bilateral filter keeps layer edges crisp while smoothing texture
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Adaptive thresholding handles shadows, uneven lighting, and variable skin colors
    thresh = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 19, 5
    )

    # Clean up small salt-and-pepper noise
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # =========================================================
    # 3. NESTED CONTOUR HIERARCHY ANALYSIS
    # (Handles organic, elliptical, or off-center onion structures 
    # much better than rigid radial spokes)
    # =========================================================
    contours, hierarchy = cv2.findContours(
        opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    layer_count = 0
    if hierarchy is not None:
        hierarchy = hierarchy[0]
        valid_contours = []

        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            # Filter out tiny noise and full-frame background boundaries
            if 150 < area < 100000:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter > 0:
                    # Check circularity / elongation to ensure it's a ring-like structure
                    circularity = 4 * np.pi * (area / (perimeter * perimeter))
                    if circularity > 0.10: 
                        valid_contours.append((i, area))

        # Sort valid contours by containment depth or nesting level using hierarchy
        # A true onion layer is nested inside outer rings.
        nested_layers = 0
        for i, area in valid_contours:
            # Check if contour has a parent (meaning it's nested inside another ring)
            parent_idx = hierarchy[i][3]
            if parent_idx != -1:
                nested_layers += 1

        # Fallback to total valid rings if hierarchy tree is sparse
        layer_count = max(nested_layers, len(valid_contours))
        # Cap to a realistic biological maximum
        layer_count = min(layer_count, 15)

    

    return layer_count, result