from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": ",",  # 分隔符
        "quotechar": '"',  # 带分隔符文本的包裹符
        "fieldnames": ["name", "age", "gender", "hobby"]  # 列名, 文件无列名时指定
    },
)

# documents = loader.load()
# print(documents)
for document in loader.lazy_load():
    print(document)
