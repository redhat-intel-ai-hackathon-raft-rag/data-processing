import os
import cohere
from dotenv import load_dotenv
load_dotenv()


cohereclient = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
response = cohereclient.chat(
    model="command-r",
    messages=[
        {
            "role": "system",
            "content": "Hello, how can I help you today?"
        },
        {
            "role": "user",
            "content": "hello world!"
        }
    ]
)

print(response.message.content[0].text)
