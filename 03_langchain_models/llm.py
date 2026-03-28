from langchain_community.llms.tongyi import Tongyi

# 不用qwen3-max聊天模型
# 使用qwen-max大语言模型
llm = Tongyi(api_key="sk-b01fa56960e0483ab12dff7a7577129f", model='qwen-max')

# res = llm.invoke("你是谁")
res = llm.stream("你是谁")

# print(res)
for chunk in res:
    print(chunk, end="", flush=True)
