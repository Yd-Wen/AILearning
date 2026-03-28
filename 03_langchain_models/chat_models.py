import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 加载 .env 文件
load_dotenv()

# 实例化模型
# 不用用qwen-max大语言模型
# 使用qwen3-max聊天模型
chat = ChatTongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen3-max")

# 准备消息
messages = [
    # SystemMessage(content="你是一名边塞诗人"),
    # HumanMessage(content="请作一首唐诗"),
    # AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    # HumanMessage(content="仿照上面的例子作一首边塞诗")
    # 二元元组简写形式
    ("system", "你作为一名边塞诗人"),
    ("human", "请作一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    ("human", "仿照上面的例子作一首边塞诗")
]

# 聊天
res = chat.stream(messages)

# 输出 chunk.content
for chunk in res:
    print(chunk.content, end="", flush=True)
