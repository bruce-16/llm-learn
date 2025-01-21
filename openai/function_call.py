import os
import sys

from openai.types.chat import ChatCompletionToolParam

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tool.get_completion import get_client


def test_function_call():
    client = get_client()
    tools: list[ChatCompletionToolParam] = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Bogotá, Colombia",
                        }
                    },
                    "required": ["location"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "What is the weather like in Paris today?"}
        ],
        tools=tools,
    )

    print(completion.choices[0].message.tool_calls)


if __name__ == "__main__":
    test_function_call()
