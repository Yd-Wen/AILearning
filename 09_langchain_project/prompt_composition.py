import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.output_parsers import StrOutputParser

# 加载 .env 文件
load_dotenv()

chat = ChatTongyi(
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-max"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手。以我提供的参考资料为依据，简洁而专业地回答用户问题。参考资料：{context}"),
    ("human", "用户提问：{input}")
])

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="text-embedding-v4"
    )
)

vector_store.add_texts(["减肥就是要少吃多练", "在降脂减肥过程中清淡少油控制卡路里摄入并运动起来非常重要", "跑步是很好的运动"])

question = "如何减肥"
context = ""

for doc in vector_store.similarity_search(query=question, k=2):
    print(doc.page_content)
    context += doc.page_content + "\n"


def print_parser(full_prompts):
    print("*"*20, full_prompts, "*"*20)
    return full_prompts


chain = prompt | print_parser | chat | StrOutputParser()

print(chain.invoke({"input": question, "context": context}))
