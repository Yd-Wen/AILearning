from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.output_parsers import StrOutputParser

chat = ChatTongyi(
    dashscope_api_key="sk-b01fa56960e0483ab12dff7a7577129f",
    model="qwen3-max"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手。以我提供的参考资料为依据，简洁而专业地回答用户问题。参考资料：{context}"),
    ("human", "用户提问：{input}")
])

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(
        dashscope_api_key="sk-b01fa56960e0483ab12dff7a7577129f",
        model="text-embedding-v4"
    )
)

vector_store.add_texts(["减肥就是要少吃多练", "在降脂减肥过程中清淡少油控制卡路里摄入并运动起来非常重要", "跑步是很好的运动"])

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

question = "如何减肥"


def format_parser(documents):
    context = ""
    for doc in documents:
        print(doc.page_content)
        context += doc.page_content + "\n"
    return context


def print_parser(full_prompts):
    print("*"*20, full_prompts, "*"*20)
    return full_prompts


chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_parser }
    | prompt | print_parser | chat | StrOutputParser()
)

print(chain.invoke(question))
