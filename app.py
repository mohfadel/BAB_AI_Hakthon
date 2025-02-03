from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import ocr
import qna
import os

app = Flask(__name__)

# Get Configuration Settings
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
lang_ai_endpoint = os.getenv('LANG_AI_SERVICE_ENDPOINT')
lang_ai_key = os.getenv('LANG_AI_SERVICE_KEY')
lang_ai_project_name = os.getenv('LANG_QA_PROJECT_NAME')
lang_ai_deployment_name = os.getenv('LANG_QA_DEPLOYMENT_NAME')
upload_folder = os.path.join('static', 'uploads')


# Ensure upload directory exists
os.makedirs(upload_folder, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)
            
            # call OCR to get text from image
            ocr_result = ocr.get_text_read(ai_endpoint, ai_key, file_path)
            ocr_result_text = ocr.get_text_from_result(ocr_result)
            print(ocr_result_text)

            # call QNA 
            qa_result = qna.get_answer_for_question(lang_ai_endpoint, lang_ai_key, lang_ai_project_name, lang_ai_deployment_name, ocr_result_text)

            return render_result(file.filename, ocr_result, qa_result)
    return render_template("index.html")

def render_result(fileName, ocr_result, qna_result):
    ocr_result_text = "<ul>"
    if ocr_result.read is not None:
        for line in ocr_result.read.blocks[0].lines:
            # Return the text detected in the image
            ocr_result_text += "<li>" + line.text + "</li>"
        ocr_result_text += "</ul>"
        return render_template("result.html", filename=fileName, result=ocr_result_text)
    else:
        return f"OCR return None Text from image file name : {fileName}"

if __name__ == "__main__":
    app.run(debug=True)