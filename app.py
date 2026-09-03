from flask import Flask, render_template, request
import cv2
import os

from detector import detect_layers


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    layer_count = None
    result_image = None

    if request.method == "POST":

        file = request.files.get("image")

        if file:

            file_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(file_path)

            # Read image
            image = cv2.imread(file_path)

            # Detect onion layers
            layer_count, result = detect_layers(image)

            # Save result
            result_path = os.path.join(
                UPLOAD_FOLDER,
                "result.jpg"
            )

            cv2.imwrite(result_path, result)

            result_image = "/static/uploads/result.jpg"

    return render_template(
        "index.html",
        layer_count=layer_count,
        result_image=result_image
    )


if __name__ == "__main__":
    app.run(debug=True)