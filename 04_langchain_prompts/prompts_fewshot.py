import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms import Tongyi

# 加载 .env 文件
load_dotenv()

llm = Tongyi(api_key=os.getenv("DASHSCOPE_API_KEY"), model='qwen-max')

example_prompt = PromptTemplate.from_template("单词：{word}， 反义词：{antonym}")

example_data = [
    {"word": "good", "antonym": "bad"},
    {"word": "big", "antonym": "small"}
]

few_shot_template = FewShotPromptTemplate(
   example_prompt=example_prompt,                   # 示例模板
   examples=example_data,                           # 示例数据
   prefix="给出单词的反义词，示例如下：",                # 示例数据的前缀
   suffix="请基于上述示例，给出 {input_word} 的反义词",  # 示例数据的后缀
   input_variables=['input_word']                   # 注入前缀/后缀的变量
)

# prompt_text = few_shot_template.invoke({"input_word": "beautiful"}).to_string()
prompt_text = few_shot_template.format(input_word="beautiful")

print(prompt_text)

res = llm.invoke(prompt_text)

print(res)
