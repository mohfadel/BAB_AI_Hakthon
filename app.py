from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from ocr import get_text_read
import os

app = Flask(__name__)

# Get Configuration Settings
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
upload_folder = os.getenv('UPLOAD_FOLDER')

# Ensure upload directory exists
os.makedirs(upload_folder, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)
            ocr_result = get_text_read(ai_endpoint, ai_key, file_path)
            ocr_result_text = "<ul>"
            if ocr_result.read is not None:
                for line in ocr_result.read.blocks[0].lines:
                    # Return the text detected in the image
                    ocr_result_text += "<li>" + line.text + "</li>"
                ocr_result_text += "</ul>"
                return render_template("ocr-result.html", filename=file.filename, ocr_result_text=ocr_result_text)
            else:
                return f"OCR return None Text from image file name : {file.filename}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)