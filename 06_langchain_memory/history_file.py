import os
import json
from typing import Sequence

from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

# 加载 .env 文件
load_dotenv()

# message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict: 字典列表 -> BaseMessage类实例列表
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id      # 会话ID
        self.storage_path = storage_path  # 不同ID的会话历史的存储路径
        # 会话历史文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id + ".json")
        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        """参数为单个BaseMessage，而非Sequence"""
        # 读取已有消息
        all_messages = self.messages  # 直接使用@property装饰的messages属性
        # 追加单个消息（而非extend）
        all_messages.append(message)
        # 转换为字典列表并写入文件
        message_dicts = [message_to_dict(msg) for msg in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(message_dicts, f, ensure_ascii=False)  # 加ensure_ascii=False避免中文乱码

    @property  # property装饰器将messages方法转变成成员属性
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                message_data = json.load(f)
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


chat = ChatTongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen3-max")

base_prompt = ChatPromptTemplate.from_messages([
    ("system", "请根据历史会话记录回答问题，历史会话："),
    MessagesPlaceholder("chat_history"),
    ("human", "请回答问题：{input}")
])


def print_parser(full_prompts):
    print("*" * 20, full_prompts, "*" * 20)
    return full_prompts


str_parser = StrOutputParser()

base_chain = base_prompt | print_parser | chat | str_parser


# 获取会话历史
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


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

    # conversation_chain.invoke({"input": "小明有两只猫"}, session_config)
    # conversation_chain.invoke({"input": "小刚有一只狗"}, session_config)
    print(conversation_chain.invoke({"input": "总共有几只宠物？"}, session_config))
