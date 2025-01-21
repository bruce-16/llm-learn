import os
from openai import OpenAI
from .dotenv import get_openai_key, get_proxy

proxy = get_proxy()
if proxy:
    os.environ["HTTPS_PROXY"] = proxy

client = OpenAI(
    api_key=get_openai_key(),  # This is the default and can be omitted
)

def get_client():
    return OpenAI(
        api_key=get_openai_key(),  # This is the default and can be omitted
    )

def get_completion(prompt, model="gpt-4o-mini", temperature=0):
    """
    使用 OpenAI API 获取对提示的响应

    参数:
        prompt (str): 发送给模型的提示文本
        model (str): 使用的模型名称，默认是 gpt-3.5-turbo
        temperature (float): 生成文本的随机性，0表示最确定性的响应

    返回:
        str: 模型的响应文本
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=temperature,
    )

    return chat_completion.choices[0].message.content
