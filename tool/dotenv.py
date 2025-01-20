import os
from dotenv import load_dotenv, find_dotenv

def get_openai_key():
    _ = load_dotenv(find_dotenv())
    return os.environ['KEY_API']

def get_proxy():
    _ = load_dotenv(find_dotenv())
    return os.environ.get('HTTPS_PROXY', '')
