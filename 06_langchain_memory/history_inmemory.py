import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 加载 .env 文件
load_dotenv()

chat = ChatTongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen3-max")

base_prompt = ChatPromptTemplate.from_messages([
    ("system", "请根据历史会话记录回答问题，历史会话："),
    MessagesPlaceholder("chat_history"),
    ("human", "请回答问题：{input}")
])


def print_parser(full_prompts):
    print("*"*20, full_prompts, "*"*20)
    return full_prompts


str_parser = StrOutputParser()

base_chain = base_prompt | print_parser | chat | str_parser

# 会话历史，key是session_id，value是InMemoryChatMessageHistory
conversation_history = {}


# 获取会话历史
def get_history(session_id):
    if session_id not in conversation_history:
        conversation_history[session_id] = InMemoryChatMessageHistory()
    return conversation_history[session_id]


# 新链：对原有链的增强，附加历史会话
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    history_messages_key="chat_history",
    input_messages_key="input"
)

if __name__ == "__main__":
    # 固定格式，添加LangChain的配置，为当前会话添加session_id
    session_config = {"configurable": {"session_id": "user_001"}}

    conversation_chain.invoke({"input": "小明有两只猫"}, session_config)
    conversation_chain.invoke({"input": "小刚有一只狗"}, session_config)
    print(conversation_chain.invoke({"input": "总共有几只宠物？"}, session_config))
    