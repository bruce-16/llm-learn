import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pydantic import BaseModel
from tool.get_completion import get_client


class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str


def test_res_struct_format():
    client = get_client()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
            },
            {"role": "user", "content": "how can I solve 8x + 7 = -23"},
        ],
        response_format=MathReasoning,
    )
    math_reasoning = completion.choices[0].message

    # 结构化的输出可能会被拒绝掉
    if math_reasoning.refusal:
        print(math_reasoning.refusal)
    elif math_reasoning.parsed:
        # print(math_reasoning.parsed.model_dump_json())
        print(math_reasoning.parsed.model_dump().get("steps"))
    else:
        print(math_reasoning.content)


if __name__ == "__main__":
    test_res_struct_format()
