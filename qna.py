import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

def get_answer_for_question(ai_endpoint, ai_key, ai_project_name, ai_deployment_name, user_question):
    try:
        # Create client using endpoint and key
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=AzureKeyCredential(ai_key))

        # Submit a question and display the answer
        response = ai_client.get_answers(question=user_question,
                                        project_name=ai_project_name,
                                        deployment_name=ai_deployment_name)
        for candidate in response.answers:
            print(candidate.answer)
            print("Confidence: {}".format(candidate.confidence))
            print("Source: {}".format(candidate.source))

    except Exception as ex:
        print(ex)
