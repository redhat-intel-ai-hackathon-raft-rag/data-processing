import vertexai
import openai

from google.auth import default, transport


PROJECT_ID = "polar-ring-439102-e9"
location = "us-central1"
vertexai.init(project=PROJECT_ID, location=location)
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
auth_request = transport.requests.Request()
credentials.refresh(auth_request)
API_KEY = credentials.token
geminiclient = openai.OpenAI(
    base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
    api_key=credentials.token,
)