import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 1. 获取client对象
client: OpenAI = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个资深的python编程专家"},
        {"role": "assistant", "content": "好的，我是资深的python编程专家，你要问什么"},
        {"role": "user", "content": "请写一个python代码，实现一个函数，返回字符串的长度"},
    ],
    stream=True              # 开启流式
)

# print(completion.choices[0].message.content)
for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
# 这段代码的作用是打印流式响应中的每个数据块（chunk）的内容
# `end=""` 参数确保每次打印后不换行，`flush=True` 确保内容立即输出到终端，这对于实时显示流式数据非常重要
