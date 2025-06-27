from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found")

openai = OpenAI()


def test_prompt():
    message = "Hello, GPT! This is a test prompt to check that you're working!"
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": message}])
    print(response.choices[0].message.content)
