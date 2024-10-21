import os
from dotenv import load_dotenv

import vertexai
import openai
from google.auth import default, transport
from google.oauth2 import service_account
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


load_dotenv()
PROJECT_ID = "polar-ring-439102-e9"
# location = "us-central1"
location = "asia-northeast1"
MODEL_ID = "text-embedding-004"
credentials = service_account.Credentials.from_service_account_file(
    os.getenv("GCLOUD_SERVICE_ACCOUNT_KEY_PATH"),
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
vertexai.init(project=PROJECT_ID, location=location)
auth_request = transport.requests.Request()
credentials.refresh(auth_request)
geminiclient = openai.OpenAI(
    base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
    api_key=credentials.token,
)
embedding_model = TextEmbeddingModel.from_pretrained(MODEL_ID)


class TaskType:
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    SEMANTIC_SIMILARITY = "SEMANTIC_SIMILARITY"
    CLASSIFICATION = "CLASSIFICATION"
    CLUSTERING = "CLUSTERING"
    QUESTION_ANSWERING = "QUESTION_ANSWERING"
    FACT_VERIFICATION = "FACT_VERIFICATION"
    CODE_RETRIEVAL_QUERY = "CODE_RETRIEVAL_QUERY"
# they were trained for the different downstream tasks,
# so it's good to use the same task type for the same task


def refresh_client():
    global geminiclient
    credentials.refresh(auth_request)
    geminiclient = openai.OpenAI(
        base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
        api_key=credentials.token,
    )


if __name__ == "__main__":
    print(embedding_pipeline(["Hello, world!"], TaskType.RETRIEVAL_QUERY))
