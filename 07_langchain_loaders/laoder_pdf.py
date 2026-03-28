from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="data/test.pdf",   # 文件路径
    mode="page",                 # 读取模式，可选page（按页数分割获取多个Document）/single（获取单个Document
    # password="123456"          # 密码
)

i = 0
for document in loader.lazy_load():
    print(document)
    i += 1
    print("="*20, i, "="*20)
