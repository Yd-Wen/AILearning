import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

# 加载 .env 文件
load_dotenv()

# 初始化模型
model = ChatTongyi(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-max"
)

# 定义工具 - 新版使用 @tool 装饰器
@tool(description="查询天气")
def get_weather(location: str) -> str:
    """查询指定城市的天气"""
    return f"{location}的天气是晴天"

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题！"
)

# 执行查询
res = agent.invoke({
    "messages": [
        {"role": "user", "content": "今天北京的天气如何？"}
    ]
})

for msg in res['messages']:
    print(type(msg).__name__, msg.content)
