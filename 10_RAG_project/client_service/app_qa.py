import streamlit as st
from rag import RAGService
import config_data as config

# 添加网页标题
st.title("智能客服")
st.divider()  # 分割线

if "rag" not in st.session_state:
    st.session_state.rag = RAGService()

if "message" not in st.session_state:
    st.session_state.message = [
        {"role": "assistant", "content": "我是一个智能助手，有什么可以帮助您？"}
    ]

for message in st.session_state.message:
    st.chat_message(message['role']).write(message['content'])

# 输入栏
prompt = st.chat_input("请输入问题")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.message.append({"role": "user", "content": prompt})
    ai_res_list = []
    with st.spinner("AI思考中..."):
        res_stream = st.session_state.rag.chain.stream({"question": prompt}, config.session_config)
        # yield
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state.message.append({"role": "assistant", "content": "".join(ai_res_list)})
