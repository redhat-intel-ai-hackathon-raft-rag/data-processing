import os
from vertexai.language_models import TextEmbeddingModel
from typing import Any

import google.auth
import google.auth.transport.requests
import openai
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("GCLOUD_PROJECT_ID")
location = os.getenv("GCLOUD_LOCATION", "us-central1")
MODEL_ID = "text-embedding-004"
embedding_model = TextEmbeddingModel.from_pretrained(MODEL_ID)
# vertexai.init(project=PROJECT_ID, location=location)


class OpenAICredentialsRefresher:
    def __init__(self, **kwargs: Any) -> None:
        # Set a dummy key here
        self.client = openai.OpenAI(**kwargs, api_key="DUMMY")
        self.creds, self.project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

    def __getattr__(self, name: str) -> Any:
        if not self.creds.valid:
            auth_req = google.auth.transport.requests.Request()
            self.creds.refresh(auth_req)

            if not self.creds.valid:
                raise RuntimeError("Unable to refresh auth")

            self.client.api_key = self.creds.token
        return getattr(self.client, name)


geminiclient = OpenAICredentialsRefresher(
    base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
)


class TaskType:
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    SEMANTIC_SIMILARITY = "SEMANTIC_SIMILARITY"
    CLASSIFICATION = "CLASSIFICATION"
    CLUSTERING = "CLUSTERING"
    QUESTION_ANSWERING = "QUESTION_ANSWERING"
    FACT_VERIFICATION = "FACT_VERIFICATION"
    CODE_RETRIEVAL_QUERY = "CODE_RETRIEVAL_QUERY"


if __name__ == "__main__":
    print(geminiclient.chat.completions.create(
        model="google/gemini-1.5-flash-002",
        messages=[{"role": "user", "content": "Why is the sky blue?"}],
    ).choices[0].message.content)
