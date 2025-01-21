import json
import os
import sys
from dataclasses import dataclass
from typing import Any

from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tool.get_completion import get_client


@dataclass
class Location:
    latitude: float
    longitude: float


def get_weather(location: str) -> str:
    return f"The weather in {location} is 20 degrees Celsius."


def call_function(name: str, args: dict[str, Any]) -> str:
    if name == "get_weather":
        return get_weather(args["location"])
    return ""


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


def test_function_call():
    client = get_client()

    # step1: 声明 message 列表，第一个可以是用户消息，也可以是 system
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "user",
            "content": "What is the weather like in Paris today?",
        }
    ]

    # step2: 发送 message，获取 completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

    # step3: 将 completion 添加到 message 列表中
    messages.append(completion.choices[0].message)

    # step4: 如果 completion 有 tool_calls，则调用工具
    if completion.choices[0].message.tool_calls is not None:
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = call_function(name, args)
            # step5: 将调用工具的结果，组装成 message
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    # step6: 将调用完 tool 后的数据，组装成 message，再次发送 message，获取 completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

    # 这是 LLM 根据上面的 message 列表，推理出来的结果
    print(f"结果: {completion.choices[0].message.content}")
    print("----")

    # 打印最终的 message 列表
    messages.append(completion.choices[0].message)
    for msg in messages:
        if isinstance(msg, dict):
            print(json.dumps(msg, indent=2))
        else:
            print(json.dumps(msg.model_dump(), indent=2))
        print("---")  # 分隔符


if __name__ == "__main__":
    test_function_call()
