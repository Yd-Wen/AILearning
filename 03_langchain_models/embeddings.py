import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

# 加载 .env 文件
load_dotenv()

embedding = DashScopeEmbeddings(
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-v1"
)

print(embedding.embed_query("你好"))
print(embedding.embed_documents(["早上好", "晚上好"]))
