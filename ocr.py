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

        # Display the image and overlay it with the extracted text
        if result.read is not None:
            print("\nText:")

        for line in result.read.blocks[0].lines:
            # Return the text detected in the image
            print(f"  {line.text}")
        
        return result
                
    except Exception as ex:
        print(ex)

