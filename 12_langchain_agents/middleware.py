from ast import mod
import os
from textwrap import wrap
from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

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

"""
1. agent 执行前
2. agent 执行后
3. model 执行前
4. model 执行中
5. model 执行后
6. tool 执行中
"""

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent] 附带{len(state['messages'])}条消息")
    
@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent] 附带{len(state['messages'])}条消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before model] 附带{len(state['messages'])}条消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after model] 附带{len(state['messages'])}条消息")

@wrap_model_call
def model_call_hook(request, handler):
    print("[model call] 模型调用")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"[tool call] 执行{request.tool_call['name']}工具")
    print(f"[tool call] 传入参数{request.tool_call['args']}")
    return handler(request)

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model,  model_call_hook, tool_call_hook],
    system_prompt="你是一个聊天助手，可以回答用户问题！"
)

# 执行查询
prev_count = 0
for chunk in agent.stream(
    {"messages": [
        {"role": "user", "content": "今天北京的天气如何？"},
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
