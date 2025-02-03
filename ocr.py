import os
import time

# import namespaces
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
    

def get_text_read(ai_endpoint, ai_key, image_path):

    try:
        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )

        # Open image file
        with open(image_path, "rb") as f:
                image_data = f.read()

        # Use Analyze image function to read text in image
        result = cv_client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ]
        )
        
        return result
                
    except Exception as ex:
        print(ex)


def get_text_from_result(ocr_result):
    ocr_result_text = ""
    if ocr_result.read is not None:
        for line in ocr_result.read.blocks[0].lines:
            # Return the text detected in the image
            ocr_result_text += line.text
    return ocr_result_text;
     
