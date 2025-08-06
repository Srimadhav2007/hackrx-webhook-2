from google.cloud import aiplatform
from google.auth import default
import os
import sys # Import sys for sys.exit()
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# Ensure these environment variables are set in your .env file or deployment environment.
# PROJECT_ID: Your Google Cloud project ID.
# LOCATION: The Google Cloud region where you want to use Vertex AI models (e.g., "us-central1").
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")

# AGENT_ID is not used in this specific code path (direct GenerativeModel call).
# It would be used if interacting with a pre-configured Vertex AI Search agent.
# AGENT_ID = os.environ.get("AGENT_ID") # This line is commented out as it's not used here.

# --- Google Cloud Initialization ---
# This initializes the Vertex AI SDK with your project and location.
# It uses Application Default Credentials (ADC) by default.
try:
    # Attempt to get default credentials.
    # 'default_project_from_adc' might be None if ADC isn't fully configured with a project.
    credentials, default_project_from_adc = default()

    # Determine the final project ID to use:
    # Prioritize PROJECT_ID from environment variable.
    # Fallback to the project ID provided by ADC if the environment variable is not set.
    final_project_id_to_use = PROJECT_ID if PROJECT_ID else default_project_from_adc

    # Validate that both PROJECT_ID and LOCATION are determined.
    if not final_project_id_to_use:
        raise ValueError("Google Cloud PROJECT_ID is not set via environment variable or ADC.")
    if not LOCATION:
        raise ValueError("Google Cloud LOCATION is not set via environment variable.")

    # Initialize the Vertex AI SDK.
    aiplatform.init(project=final_project_id_to_use, location=LOCATION, credentials=credentials)
    print(f"Google Cloud initialized successfully for project: {final_project_id_to_use}, location: {LOCATION}")

except Exception as e:
    print(f"Error initializing Google Cloud: {e}")
    print("Please ensure:")
    print("1. Your 'PROJECT_ID' and 'LOCATION' environment variables are correctly set.")
    print("2. You have authenticated using 'gcloud auth application-default login' locally,")
    print("   or your service account (if deployed) has the necessary 'Vertex AI User' role.")
    print("   Also, ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set for service accounts.")
    sys.exit(1) # Exit the application if initialization fails

# --- Function to Query the Vertex AI Generative Model ---
def query_vertex_ai_rag_engine(user_query: str) -> str:
    # ... (rest of your query_vertex_ai_rag_engine function remains the same) ...
    try:
        from vertexai.generative_models import GenerativeModel # Import GenerativeModel here

        model = GenerativeModel("gemini-2.5-pro")

        chat = model.start_chat()

        print(f"\nSending query to Vertex AI Generative Model: '{user_query[:100]}...'") # Print first 100 chars

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