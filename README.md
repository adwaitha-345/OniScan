# 🧅 OniScan — Onion Layer Detector

OniScan is a computer vision-based web application that analyzes an image of a half-cut onion and estimates the number of visible onion layers.

The project uses Python, Flask, OpenCV, and NumPy to process the uploaded image and identify concentric ring patterns.

## ✨ Features

- 🧅 Upload a half-cut onion image
- 🔍 Analyze onion ring patterns
- 📊 Estimate the number of visible layers
- 🟢 Display detected layers on the processed image
- 🌐 Simple web interface
- ⚡ Runs locally using Flask

## 🛠️ Technologies Used

- **Python**
- **Flask** — Web application framework
- **OpenCV** — Image processing and computer vision
- **NumPy** — Numerical and image-data processing
- **HTML/CSS** — Frontend interface

## 📁 Project Structure

```text
OniScan/
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
│   └── uploads/
│
└── venv/