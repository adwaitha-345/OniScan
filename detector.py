import cv2
import numpy as np


def detect_layers(image):

    if image is None:
        return 0, image

    # Resize
    image = cv2.resize(image, (600, 600))
    result = image.copy()

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Smooth image
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    h, w = gray.shape

    # -----------------------------------------
    # Assume the cut onion is approximately
    # around the center of the image
    # -----------------------------------------

    cx = w // 2
    cy = h // 2

    # -----------------------------------------
    # Build radial intensity profile
    # -----------------------------------------

    max_radius = min(cx, cy) - 20

    radii = np.arange(10, max_radius)

    profile = []

    # Sample many directions around the onion
    angles = np.linspace(0, 2 * np.pi, 360, endpoint=False)

    for r in radii:

        x = (cx + r * np.cos(angles)).astype(np.int32)
        y = (cy + r * np.sin(angles)).astype(np.int32)

        values = gray[y, x]

        # Median reduces effect of noise
        profile.append(np.median(values))

    profile = np.array(profile, dtype=np.float32)

    # -----------------------------------------
    # Smooth profile
    # -----------------------------------------

    profile = cv2.GaussianBlur(
        profile.reshape(-1, 1),
        (1, 11),
        0
    ).flatten()

    # -----------------------------------------
    # Find changes between onion rings
    # -----------------------------------------

    gradient = np.abs(np.gradient(profile))

    # Smooth gradient
    gradient = cv2.GaussianBlur(
        gradient.reshape(-1, 1),
        (1, 7),
        0
    ).flatten()

    # -----------------------------------------
    # MUCH LOWER threshold
    # -----------------------------------------

    threshold = np.mean(gradient) + 0.70 * np.std(gradient)

    candidates = []

    for i in range(2, len(gradient) - 2):

        if gradient[i] > threshold:

            if (
                gradient[i] >= gradient[i - 1]
                and gradient[i] >= gradient[i + 1]
            ):
                candidates.append(i)

    # -----------------------------------------
    # Remove detections that are too close
    # -----------------------------------------

    detected_radii = []

    minimum_spacing = 18

    for index in candidates:

        radius = int(radii[index])

        if radius < 15:
            continue

        if not detected_radii:
            detected_radii.append(radius)

        elif radius - detected_radii[-1] >= minimum_spacing:
            detected_radii.append(radius)

    # -----------------------------------------
    # Limit to reasonable number
    # -----------------------------------------

    detected_radii = detected_radii[:8]

    layer_count = len(detected_radii)

    # -----------------------------------------
    # Draw detected layers
    # -----------------------------------------

    for radius in detected_radii:

        cv2.circle(
            result,
            (cx, cy),
            radius,
            (0, 255, 0),
            2
        )

    # Draw center
    cv2.circle(
        result,
        (cx, cy),
        5,
        (0, 0, 255),
        -1
    )

    # Show count
    cv2.putText(
        result,
        f"Layers: {layer_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    return layer_count, result
