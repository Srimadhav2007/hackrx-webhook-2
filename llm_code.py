from google.cloud import aiplatform
from google.cloud import storage
from google.auth import default
import os
import time
from dotenv import load_dotenv

load_dotenv()


PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
AGENT_ID = os.environ.get("AGENT_ID")


# --- Google Cloud Initialization ---
try:
    credentials, project = default()
    aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
    print(f"Google Cloud initialized successfully for project: {project}, location: {LOCATION}")
except Exception as e:
    print(f"Error initializing Google Cloud: {e}")
    print("Please ensure you have authenticated using 'gcloud auth application-default login'")
    exit()

# --- Function to Query the Vertex AI Agent/App ---
def query_vertex_ai_rag_engine(user_query: str) -> str:
    try:
        from vertexai.generative_models import GenerativeModel, Tool, Part # Use 'generative_models' directly, not 'preview' unless it's truly necessary

        model = GenerativeModel("gemini-2.5-pro")

        chat = model.start_chat()

        print(f"\nSending query to Vertex AI Agent/App: '{user_query}'")


        response = chat.send_message(
            user_query,
        )

        answer = response.text
        return answer

    except ModuleNotFoundError as e:
        print(f"Error querying Vertex AI Agent/App: {e}")
        if "google.cloud.aiplatform.generative_models" in str(e):
            print("Hint: Ensure 'google-cloud-aiplatform' is installed and upgraded, and the import path is correct.")
        # Add specific hints for other potential ModuleNotFound errors too
        return f"Error: Could not get an answer. Details: {e}"
    except Exception as e:
        print(f"An unexpected error occurred during RAG query: {e}")
        # Provide more specific guidance if possible
        if "AGENT_ID" in str(e) or "not found" in str(e):
            print("Ensure AGENT_ID is correct and the agent is deployed.")
        if "PROJECT_ID" in str(e) or "LOCATION" in str(e):
            print("Ensure PROJECT_ID and LOCATION are correctly configured.")
        return f"Error: Could not get an answer. Details: {e}"
