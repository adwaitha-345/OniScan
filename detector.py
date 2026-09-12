import os
import cv2
import re
import base64

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-3.6-flash"

LAYER_COUNT_PROMPT = """
Look at the entire uploaded image.

The image contains one or more pieces of onion.

Your task is to determine the TOTAL NUMBER OF VISIBLY OBSERVABLE ONION LAYERS across ALL onion pieces in the image.

Important rules:

1. Inspect the ENTIRE image, not just the largest onion piece.
2. Consider every visible onion piece.
3. Count genuine visible onion-layer boundaries/rings.
4. Add the observable layers from all pieces together.
5. Do NOT count:
   - shadows
   - highlights
   - reflections
   - cracks
   - random texture
   - surface marks
   - image noise
   - color changes that are not actual onion layers
   - the outer image/background boundary
6. Do not invent hidden layers that cannot be visually observed.
7. Only count layers that can actually be seen in the image.
8. The final answer must be ONE integer representing the net total across ALL pieces.

Return ONLY the integer.

Examples:
If there are 6 visible layers in one piece and 4 visible layers in another piece, return:
10

If there are 8 visible layers total, return:
8

Do not return words, explanations, labels, punctuation, or JSON.
"""


def image_to_base64(image):
    """
    Convert OpenCV image (numpy array) to JPEG Base64 string.
    """

    success, encoded = cv2.imencode(
        ".jpg",
        image,
        [cv2.IMWRITE_JPEG_QUALITY, 95]
    )

    if not success:
        raise RuntimeError("Could not encode image as JPEG.")

    return base64.b64encode(encoded.tobytes()).decode("utf-8")


def extract_integer(text):
    """
    Extract the first integer from Gemini's response.
    """

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    match = re.search(r"\b\d+\b", text.strip())

    if not match:
        raise RuntimeError(
            f"Gemini did not return a valid integer. Response: {text}"
        )

    return int(match.group())


def detect_layers(image):
    """
    Sends the complete image to Gemini Vision and returns:

        (layer_count, result_image)

    The Flask application can continue using the same interface.
    """

    if image is None:
        raise ValueError("Input image is None.")

    # Convert OpenCV image -> Base64 JPEG
    image_b64 = image_to_base64(image)

    try:
        interaction = client.interactions.create(
            model=MODEL,
            input=[
                {
                    "type": "text",
                    "text": LAYER_COUNT_PROMPT
                },
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": "image/jpeg"
                }
            ]
        )

        response_text = interaction.output_text

        print("Gemini response:", response_text)

        count = extract_integer(response_text)

    except Exception as e:
        print("Gemini detection error:", repr(e))
        raise RuntimeError(f"Gemini detection failed: {e}")

    # Create result image so the existing Flask UI continues working.
    result = image.copy()

    

    return count, result