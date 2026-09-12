# Savalagirigiri — Onion Layer Detector

Savalagirigiri is an AI-powered web application that analyzes an image of a half-cut onion and estimates the number of visibly observable onion layers.

The project uses Python, Flask, OpenCV, and Gemini 3.6 Flash to process and analyze uploaded or camera-captured onion images.

## Features

- Upload a half-cut onion image
- Capture an onion image using the device camera
- Preview the selected image
- Automatically submit images for detection
- Analyze onion layer patterns using Gemini AI
- Estimate the number of visible onion layers
- Count layers across multiple onion pieces
- Display the detected layer count
- Handle AI detection and API errors
- Automatically clean up temporary images
- Simple web interface
- Runs locally using Flask

## Technologies Used

**Language:** Python

**Framework:** Flask

**AI Model:** Gemini 3.6 Flash

**Libraries:**
- OpenCV
- NumPy
- google-genai
- python-dotenv

**Frontend:**
- HTML
- CSS
- JavaScript

**Tools:**
- VS Code
- Git
- GitHub

## Project Structure

```text
Savalagirigiri/
│
├── app.py
├── detector.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── image.png
│   ├── onion.png
│   └── uploads/
│
└── venv/
## Implementation

The application follows this pipeline:

```text
User
  ↓
Capture Image / Upload Image
  ↓
Frontend
  ↓
Image Preview
  ↓
Automatic Submission
  ↓
Flask Backend
  ↓
Image Validation & Processing
  ↓
OpenCV
  ↓
Convert Image to Base64
  ↓
Gemini 3.6 Flash
  ↓
Analyze Visible Onion Layers
  ↓
Return Layer Count
  ↓
Display Result
