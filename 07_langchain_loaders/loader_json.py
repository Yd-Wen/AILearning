from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    # file_path="./data/stu.json",
    # file_path="./data/stus.json",
    file_path="data/stus.jsonl",
    jq_schema=".hobby[0]",
    text_content=False,
    json_lines=True
)

for document in loader.lazy_load():
    print(document)
