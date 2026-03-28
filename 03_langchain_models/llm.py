import os
from dotenv import load_dotenv
from langchain_community.llms.tongyi import Tongyi

# 加载 .env 文件
load_dotenv()

# 不用qwen3-max聊天模型
# 使用qwen-max大语言模型
llm = Tongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model='qwen-max')

# res = llm.invoke("你是谁")
res = llm.stream("你是谁")

# print(res)
for chunk in res:
    print(chunk, end="", flush=True)
