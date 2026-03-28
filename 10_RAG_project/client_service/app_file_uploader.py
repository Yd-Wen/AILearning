"""
基于 streamlit 的 WEB 上传服务
pip install streamlit

Streamlit: 当WEB页面刷新，代码重新运行
    - 解决方案: 使用session-state, 字典, 默认为空字典
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

if "service" not in st.session_state:
    st.session_state.service = KnowledgeBaseService()

# 添加网页标题
st.title("知识库更新")

# 文件上传控件
uploader_file = st.file_uploader(
    label="请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False  # 是否允许上传多个文件
)

if uploader_file:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024   # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}， 文件大小：{file_size:.2f}KB")

    # get_value -> bytes -> decode('utf-8)
    text = uploader_file.getvalue().decode('utf-8')

    # 上传
    with st.spinner("上传中..."):
        time.sleep(1)
        st.write(st.session_state.service.upload(text, file_name))
