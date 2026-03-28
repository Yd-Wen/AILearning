import os
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# 加载 .env 文件
load_dotenv()

loader = CSVLoader(
    file_path="data/info.csv",
    encoding="utf-8",
    source_column="source"      # 指定数据来源
)

vector_store = Chroma(
    collection_name="info",
    embedding_function=DashScopeEmbeddings(dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")),
    persist_directory="data/chroma_db"
)

document = loader.load()

vector_store.add_documents(
    documents=document,
    ids=['id_'+str(i+1) for i in range(len(document))]
)

vector_store.delete(ids=['id_1'])

res = vector_store.similarity_search(
    query="学python容易吗",
    k=2,
    filter={"source": "黑马程序员"}
)
print(res)
