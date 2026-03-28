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

# 定义工具 
@tool(description="查询指定公司的股票价格")
def get_price(name: str) -> str:
    """询指定公司的股票价格"""
    return f"股票{name}的价格是20元"

@tool(description="查询指定公司的信息")
def get_company(name: str) -> str:
    """查询指定公司的信息"""
    return f"{name}是一家上市公司，专注于互联网技术"

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[get_price, get_company],
    system_prompt="你是一个聊天助手，可以回答用户问题！告诉用户你的思考过程和为什么调用某个工具！"
)

# 执行查询
prev_count = 0
for chunk in agent.stream(
    {"messages": [
        {"role": "user", "content": "今天阿里的股票价格如何？介绍一下阿里"},
    ]},
    stream_mode="values"
):
    messages = chunk['messages']
    total = len(messages)
    new_count = total - prev_count

    print(f"\n=== 第 {prev_count + 1}~{total} 条消息 (新增 {new_count} 条) ===")

    # 只打印新增的消息
    for i, msg in enumerate(messages[prev_count:], start=prev_count + 1):
        msg_type = type(msg).__name__
        print(f"\n[{i}] {msg_type}")
        print(f"    content: {msg.content[:200] if msg.content else '(空)'}...")

        # AIMessage: 打印工具调用请求
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"    tool_calls: {[tc['name'] for tc in msg.tool_calls]}")

        # ToolMessage: 打印工具返回结果
        if hasattr(msg, 'name') and msg.name:
            print(f"    tool_name: {msg.name}")
        if hasattr(msg, 'tool_call_id') and msg.tool_call_id:
            print(f"    tool_call_id: {msg.tool_call_id}")

    prev_count = total
    print("\n" + "="*50)