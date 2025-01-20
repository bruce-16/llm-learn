import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tool.dotenv import get_openai_key
from openai import OpenAI

def main():
    client = OpenAI(
        api_key=get_openai_key(),  # This is the default and can be omitted
    )

    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."},
      ],
    )
    print(completion.choices[0].message)

if __name__ == "__main__":
    main()
