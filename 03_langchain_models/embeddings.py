from langchain_community.embeddings import DashScopeEmbeddings

embedding = DashScopeEmbeddings(
    dashscope_api_key="sk-b01fa56960e0483ab12dff7a7577129f",
    model="text-embedding-v1"
)

print(embedding.embed_query("你好"))
print(embedding.embed_documents(["早上好", "晚上好"]))
