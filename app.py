from flask import Flask, render_template, request

import cv2
import os
import uuid
import time
import threading

from detector import detect_layers


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# UPLOAD FOLDER
# ============================================================

UPLOAD_FOLDER = "static/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# Temporary files are deleted after 1 minute.
FILE_LIFETIME = 60


# ============================================================
# CLEANUP FUNCTION
# ============================================================

def cleanup_old_files():
    """
    Delete temporary upload/result images older than
    FILE_LIFETIME seconds.
    """

    while True:

        current_time = time.time()

        try:

            for filename in os.listdir(
                UPLOAD_FOLDER
            ):

                filepath = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                if not os.path.isfile(
                    filepath
                ):
                    continue

                file_age = (
                    current_time
                    - os.path.getmtime(filepath)
                )

                if file_age > FILE_LIFETIME:

                    try:

                        os.remove(
                            filepath
                        )

                        print(
                            "Deleted temporary file:",
                            filename
                        )

                    except OSError:
                        pass

        except OSError:
            pass

        time.sleep(10)


# ============================================================
# HOME PAGE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    count = None
    output_image = None

    # ========================================================
    # GET
    # ========================================================

    if request.method == "GET":

        return render_template(
            "index.html",
            count=count,
            image=output_image
        )

    # ========================================================
    # CHECK IMAGE FIELD
    # ========================================================

    if "image" not in request.files:

        return render_template(
            "index.html",
            error="No image selected."
        )

    file = request.files["image"]

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )

    # ========================================================
    # CREATE TEMPORARY FILENAME
    # ========================================================

    extension = os.path.splitext(
        file.filename
    )[1]

    if not extension:
        extension = ".jpg"

    filename = (
        "upload_"
        + str(uuid.uuid4())
        + extension
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    # ========================================================
    # SAVE UPLOADED IMAGE
    # ========================================================

    try:

        file.save(
            filepath
        )

    except Exception as error:

        print(
            "Upload save error:",
            repr(error)
        )

        return render_template(
            "index.html",
            error="Could not save the uploaded image."
        )

    # ========================================================
    # READ IMAGE
    # ========================================================

    image = cv2.imread(
        filepath
    )

    if image is None:

        try:
            os.remove(filepath)
        except OSError:
            pass

        return render_template(
            "index.html",
            error="Could not read the image."
        )

    # ========================================================
    # RUN GEMINI DETECTOR
    # ========================================================

    try:

        count, result = detect_layers(
            image
        )

    except Exception as error:

        print(
            "Detector error:",
            repr(error)
        )

        # Delete original upload.
        try:
            os.remove(filepath)
        except OSError:
            pass

        # IMPORTANT:
        # Do NOT turn an API failure into count = 0.
        return render_template(
            "index.html",
            error=(
                "AI detection failed: "
                + str(error)
            )
        )

    # ========================================================
    # CREATE RESULT FILENAME
    # ========================================================

    result_filename = (
        "result_"
        + str(uuid.uuid4())
        + ".jpg"
    )

    result_path = os.path.join(
        UPLOAD_FOLDER,
        result_filename
    )

    # ========================================================
    # SAVE RESULT IMAGE
    # ========================================================

    success = cv2.imwrite(
        result_path,
        result
    )

    if not success:

        try:
            os.remove(filepath)
        except OSError:
            pass

        return render_template(
            "index.html",
            error="Could not create the result image."
        )

    # ========================================================
    # DELETE ORIGINAL UPLOAD
    # ========================================================

    try:

        os.remove(
            filepath
        )

    except OSError:
        pass

    # ========================================================
    # RESULT IMAGE URL
    # ========================================================

    output_image = (
        "/static/uploads/"
        + result_filename
    )

    # ========================================================
    # RETURN RESULT TO EXISTING UI
    # ========================================================

    return render_template(
        "index.html",
        count=count,
        image=output_image
    )


# ============================================================
# BACKGROUND CLEANUP THREAD
# ============================================================

cleanup_thread = threading.Thread(
    target=cleanup_old_files,
    daemon=True
)

cleanup_thread.start()


# ============================================================
# START FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )