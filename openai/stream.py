import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pydantic import BaseModel
from tool.get_completion import get_client


class EntitiesModel(BaseModel):
    attributes: list[str]
    colors: list[str]
    animals: list[str]


def test_stream():
    client = get_client()

    with client.beta.chat.completions.stream(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract entities from the input text"},
            {
                "role": "user",
                "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
            },
        ],
        response_format=EntitiesModel,
    ) as stream:
        for event in stream:
            if event.type == "content.delta":
                if event.parsed is not None:
                    # Print the parsed data as JSON
                    print("content.delta parsed:", event.parsed)
            elif event.type == "content.done":
                print("content.done")

    final_completion = stream.get_final_completion()
    print("Final completion:", final_completion)


if __name__ == "__main__":
    test_stream()
