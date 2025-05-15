import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Constants
TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your .env or system
ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "microsoft/Phi-3.5-vision-instruct"

def get_feedback_response(user_prompt):
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is not set in environment variables.")

    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(TOKEN),
    )

    messages = [
        SystemMessage("You are an academic advisor AI. Give clear, constructive, truthful do not sugarcoat like fletcher in whiplash and motivating feedback based on academic performance."),
        UserMessage(user_prompt)
    ]

    try:
        response = client.complete(
            stream=False,  # ✅ Important: single object
            messages=messages,
            model=MODEL_NAME,
            timeout=30  # ⏱️ Set reasonable timeout
        )
        
        # ✅ This is the correct way to get the output for non-streaming
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"⚠️ AI generation failed: {str(e)}"
    
    finally:
        client.close()
