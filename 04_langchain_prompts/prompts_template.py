import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Tongyi

# 加载 .env 文件
load_dotenv()

llm = Tongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model='qwen-max')

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了个{gender}娃，帮王取名，直接给出名字，不做解释。"
)

# 标准写法
# prompt_text = prompt_template.format(lastname='张', gender='女')
# print(llm.invoke(prompt_text))

# 基于链的写法
chain = prompt_template | llm
print(chain.invoke({'lastname': '张', 'gender': '女'}))


