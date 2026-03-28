from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="data/test.txt",
    encoding="utf-8"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    separators=["\n\n", "\n", " ", "", "?", "!", "？", "！"],
    length_function=len  # 使用python默认方法获取字符串长度
)

documents = loader.load()
print(documents)

split_documents =splitter.split_documents(documents)
print(split_documents)
print(len(split_documents))
