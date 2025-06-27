import requests
from openai_common import *
import sys
import re
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class RawWebsite:
    def __init__(self, url):
        """
        Create this Website object from the given url
        """
        self.url = url
        self.response = requests.get(url, headers=headers).content

system_prompt_parody = "You are an assistant that receives a website in raw HTML format \
and converts it into a parody website, using the received content and with layout and formatting similar to the original. \
Respond with ONLY the result HTML file, no other remarks - just return a raw HTML. In addition, look for any relative paths inside the HTML and replace them with the website URL, which will be provided as well."

def user_prompt_for_parody(website):
    user_prompt = f"The URL of the website is: {website.url}\nThe HTML content of the website to parodize is:\n {website.response}"
    return user_prompt

def messages_for_parody(website):
    return [
        {"role": "system", "content": system_prompt_parody},
        {"role": "user", "content": user_prompt_for_parody(website)}
    ]

def parodize(website):
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for_parody(website)
    )
    return response.choices[0].message.content

def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content written to {filename}")

def url_to_filename(url: str) -> str:
    # Parse the URL
    parsed = urlparse(url)

    # Combine netloc and path
    path = parsed.netloc + parsed.path

    # Replace slashes and unsafe characters with underscores
    safe_path = re.sub(r'[^a-zA-Z0-9]', '_', path)

    # Limit filename length and append .html
    return safe_path[:255] + ".html"


if len(sys.argv) != 2:
    print("Please provide a URL")
    exit()
url = sys.argv[1]

print(f"Fetching from URL {url}")
website = RawWebsite(url)

print("Asking model to parodize...")
content = parodize(website)

filename = url_to_filename(url)
print(f"Writing to file {url}")
write_to_file(filename, content)