import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser

# 加载 .env 文件
load_dotenv()

chat = ChatTongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen3-max")

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个边塞诗人"),
    ("human", "请作一首唐诗"),
    MessagesPlaceholder('history'),
    ("human", "仿照之前你给出的唐诗，作一首边塞诗")
])

history_data = [
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。"),
    ("human", "再作一首"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
]

parser = StrOutputParser()

# prompt_text = chat_prompt.invoke({'history': history_data}).to_string()
# print(prompt_text)

# res = chat.invoke(prompt_text)
# print(res.content)

chain = chat_prompt | chat | parser | chat
# print(chain.invoke({'history': history_data}).content)
for chunk in chain.stream({'history': history_data}):
    print(chunk.content, end="", flush=True)
