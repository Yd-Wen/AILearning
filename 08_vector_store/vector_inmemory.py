from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

loader = CSVLoader(
    file_path="data/info.csv",
    encoding="utf-8",
    source_column="source"      # 指定数据来源
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(dashscope_api_key="sk-b01fa56960e0483ab12dff7a7577129f")
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
    filter=lambda doc: doc.metadata.get("source") == "极客时间"
)
print(res)
