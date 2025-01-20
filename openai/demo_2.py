import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tool.dotenv import get_openai_key
from openai import OpenAI

def get_json_data():
    """
    使用 OpenAI API JSON 数据

    """
    client = OpenAI(api_key=get_openai_key())

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "developer", "content": "You extract email addresses into JSON data."},
            {
                "role": "user",
                "content": "Feeling stuck? Send a message to help@mycompany.com.",
            },
        ],
        # https://platform.openai.com/docs/guides/structured-outputs 
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "email_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "description": "The email address that appears in the input",
                            "type": "string",
                        },
                        "additionalProperties": False,
                    },
                },
            },
        },
    )

    print(response.choices[0].message.content);

if __name__ == "__main__":
    get_json_data()
