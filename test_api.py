import os

from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_connection():
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'API connection successful!'"}],
        )
        print("Success:", response.content)
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    test_connection()
