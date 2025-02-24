import os
from pathlib import Path
import base64

from openai import AzureOpenAI
import azure.identity
from azure.ai.evaluation import ContentSafetyEvaluator

from dotenv import load_dotenv

load_dotenv()

credential = azure.identity.DefaultAzureCredential()
token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

token = token_provider()

base64_image = ""

with Path.open("chair.jpeg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

# Your Azure OpenAI configuration
api_key = token
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

# Path to your image
image_path = "chair.jpeg"

def get_image_description(image_path=image_path, api_key=api_key, endpoint=endpoint, deployment_name=deployment_name, api_version="2024-10-21"):
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Call the API with the image
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that describes images accurately."},
            {"role": "user", "content": [
                {"type": "text", "text": "What's in this image? Please describe it in detail."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]}
        ],
        max_tokens=300
    )
    
    # Extract the description
    image_description = response.choices[0].message.content
    return image_description

image_description = get_image_description()

azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_OPENAI_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_AI_PROJECT_NAME"),
}

# instantiate an evaluator with image and multi-modal support
safety_evaluator = ContentSafetyEvaluator(credential=credential, azure_ai_project=azure_ai_project)

# example of a conversation with an image URL
conversation_image_url = {
    "messages": [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "You are an AI assistant that understands images."}
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Can you describe this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpg;base64,{base64_image}"},
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": image_description,
                }
            ],
        },
    ]
}

# Example usage
if __name__ == "__main__":

    # Get description
    image_description = get_image_description(image_path, api_key, endpoint, deployment_name)
    
    # Print the description
    #print(f"Image Description: {image_description}")

    # run the evaluation on the conversation to output the result
    safety_score = safety_evaluator(conversation=conversation_image_url)
    print(safety_score)