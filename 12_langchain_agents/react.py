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
@tool(description="获取体重，单位千克")
def get_weight() -> int:
    """获取体重，单位千克"""
    return 90

@tool(description="获取身高，单位厘米")
def get_height() -> int:
    """获取身高，单位厘米"""
    return 172

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[get_weight, get_height],
    system_prompt="你是一个严格遵循ReAct框架的聊天助手，可以回答用户问题！且每轮仅能调用一个工具，禁止单次调用多个工具。并告诉用户你的思考过程、工具调用的原因，用思考、行动、观察三个结构告知用户。"
)

# 执行查询
prev_count = 0
for chunk in agent.stream(
    {"messages": [
        {"role": "user", "content": "计算我的BMI指数"},
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
        print(f"    content: {msg.content[:500] if msg.content else '(空)'}...")

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