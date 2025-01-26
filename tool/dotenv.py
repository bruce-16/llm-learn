import os
from dotenv import load_dotenv, find_dotenv


def get_openai_key():
    _ = load_dotenv(find_dotenv())
    return os.environ["OPEN_AI_KEY_API"]


def get_firecrawl_bearer_token():
    _ = load_dotenv(find_dotenv())
    return os.environ["FIRECRAWL_BEARER_TOKEN"]


def get_proxy():
    _ = load_dotenv(find_dotenv())
    return os.environ.get("HTTPS_PROXY", "")
