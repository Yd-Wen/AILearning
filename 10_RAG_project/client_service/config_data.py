md5_path = "./md5.text"

# Dashscope_api_key = os.environ.get("Dashscope_api_key")
dashscope_api_key = "sk-b01fa56960e0483ab12dff7a7577129f"

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# Splitter
chunk_size = 500
chunk_overlap = 50
separators = ["\n\n", "\n", " ", "", "?", "!", ".", "？", "！", "。"]
max_split_characters = 1000  # 拆分字符最大长度

# similarity search
similarity_search_k = 3

# model
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

# history
history_path = "./chat_history"

# session
session_config = {
    "configurable": {
        "session_id": "user_001"
    }
}
