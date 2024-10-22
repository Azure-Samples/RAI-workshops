import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

# Load environment variables from .env file
load_dotenv()

def analyze_text(comment_text):
    # analyze text
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=comment_text)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

# Return an appropriate moderation message if a violation is found
    if hate_result.severity > 0:
        return f"Your submission contains hateful content, which violates our community guidelines. Hate severity: {hate_result.severity}."
    elif self_harm_result.severity > 0:
        return f"Your submission contains self-harm content, which violates our community guidelines. Self harm severity: {self_harm_result.severity}."
    elif sexual_result.severity > 0:
        return f"Your submission contains sexual content, which violates our community guidelines. Sexual severity: {sexual_result.severity}."
    elif violence_result.severity > 0:
        return f"Your submissioin contains violent contnet, which violates our community guidelines. Violence severity: {violence_result.severity}."
    else:
        return None

if __name__ == "__main__":
    analyze_text()