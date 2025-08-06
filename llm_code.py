from google.cloud import aiplatform
from google.auth import default
import os
import sys
import json # Import json module
import tempfile # Import tempfile for creating temporary files
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
# AGENT_ID is not used in this specific code path.
# AGENT_ID = os.environ.get("AGENT_ID")

# --- Service Account Key from Environment Variable ---
# This environment variable will hold the RAW JSON content of your service account key.
# You will set this in Railway's variables tab.
SERVICE_ACCOUNT_JSON_CONTENT = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

# --- Google Cloud Initialization ---
try:
    # If the SERVICE_ACCOUNT_JSON_CONTENT is provided, write it to a temporary file.
    if SERVICE_ACCOUNT_JSON_CONTENT:
        # Create a temporary file to store the service account key.
        # This file will be automatically deleted when the context manager exits.
        # We need a named temporary file that persists for the duration of the app.
        # Using a fixed path in /tmp is also an option if tempfile.NamedTemporaryFile is complex.
        
        # Option A: Using tempfile (more robust for unique names)
        # with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.json') as temp_key_file:
        #     temp_key_file.write(SERVICE_ACCOUNT_JSON_CONTENT)
        #     temp_key_file_path = temp_key_file.name
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key_file_path
        # print(f"Service account key written to temporary file: {temp_key_file_path}")

        # Option B: Using a fixed path in /tmp (simpler for Docker)
        temp_key_file_path = "/tmp/service_account_key.json"
        with open(temp_key_file_path, "w", encoding="utf-8") as f:
            f.write(SERVICE_ACCOUNT_JSON_CONTENT)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key_file_path
        print(f"Service account key written to temporary file: {temp_key_file_path}")

    # Now, call google.auth.default(). It will automatically find the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable pointing to our temporary file.
    credentials, default_project_from_adc = default()

    final_project_id_to_use = PROJECT_ID if PROJECT_ID else default_project_from_adc

    if not final_project_id_to_use:
        raise ValueError("Google Cloud PROJECT_ID is not set via environment variable or ADC.")
    if not LOCATION:
        raise ValueError("Google Cloud LOCATION is not set via environment variable.")

    aiplatform.init(project=final_project_id_to_use, location=LOCATION, credentials=credentials)
    print(f"Google Cloud initialized successfully for project: {final_project_id_to_use}, location: {LOCATION}")

except Exception as e:
    print(f"Error initializing Google Cloud: {e}")
    print("Please ensure:")
    print("1. Your 'PROJECT_ID' and 'LOCATION' environment variables are correctly set.")
    print("2. If using a service account, the 'GOOGLE_APPLICATION_CREDENTIALS_JSON' environment variable contains the full JSON content.")
    print("3. Your service account has the necessary 'Vertex AI User' role.")
    sys.exit(1)

# --- Function to Query the Vertex AI Generative Model ---
def query_vertex_ai_rag_engine(user_query: str) -> str:
    try:
        from vertexai.generative_models import GenerativeModel # Import GenerativeModel here

        model = GenerativeModel("gemini-2.5-pro")

        chat = model.start_chat()

        print(f"\nSending query to Vertex AI Generative Model: '{user_query[:100]}...'")

        response = chat.send_message(user_query)

        answer = response.text
        return answer

    except Exception as e:
        print(f"An error occurred during Vertex AI Generative Model query: {e}")
        print("Please check:")
        print("1. The model name ('gemini-2.5-pro') is valid and available in your configured LOCATION.")
        print("2. Your Google Cloud project has access to this model.")
        print("3. Your API usage is within quota limits.")
        return f"Error: Could not get an answer from the model. Details: {e}"