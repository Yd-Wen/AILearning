# AI Learning Project

本项目是一个 AI 学习教程仓库，涵盖从 OpenAI API 调用到 LangChain 框架、RAG 系统构建以及 FastAPI 集成的完整学习路径。

## 项目结构

```
├── 01_test_apikey.py          # API 密钥测试
├── 02_openai.py               # OpenAI API 基础调用
├── 03_langchain_models/       # LangChain 模型
│   ├── llm.py                 # 大语言模型
│   ├── chat_models.py         # 聊天模型
│   └── embeddings.py          # 嵌入模型
├── 04_langchain_prompts/      # LangChain 提示词
│   ├── prompts_template.py    # 提示词模板
│   ├── prompts_fewshot.py     # Few-shot 提示
│   └── prompts_chat.py        # 聊天提示词
├── 05_langchain_chains/       # LangChain 链
│   ├── str_parser.py          # 字符串解析器
│   ├── json_parser.py         # JSON 解析器
│   └── func_parser.py         # 函数解析器
├── 06_langchain_memory/       # LangChain 记忆
│   ├── history_inmemory.py    # 内存历史记录
│   └── history_file.py        # 文件历史记录
├── 07_langchain_loaders/      # 文档加载器
│   ├── loader_csv.py          # CSV 加载器
│   ├── loader_json.py         # JSON 加载器
│   ├── laoder_pdf.py          # PDF 加载器
│   └── loader_text.py         # 文本加载器
├── 08_vector_store/           # 向量存储
│   ├── vector_inmemory.py     # 内存向量存储
│   └── vector_chroma.py       # Chroma 向量数据库
├── 09_langchain_project/      # LangChain 项目
│   ├── prompt_composition.py  # 提示词组合
│   └── retriever_in_chain.py  # 链中的检索器
├── 10_RAG_project/            # RAG 项目
│   └── client_service/        # 客户端服务
│       ├── app_file_uploader.py   # 文件上传
│       ├── app_qa.py              # 问答应用
│       ├── config_data.py         # 配置文件
│       ├── file_history_store.py  # 文件历史存储
│       ├── knowledge_base.py      # 知识库
│       ├── rag.py                 # RAG 核心逻辑
│       └── vector_store.py        # 向量存储
└── 11_FastAPI/                # FastAPI 项目
    ├── main.py                # FastAPI 主应用
    └── orm.py                 # ORM 数据库模型
```

## 环境搭建

### 1. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# macOS/Linux 激活虚拟环境
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件，添加你的 API 密钥：

```env
OPENAI_API_KEY=your_openai_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
```

## 依赖列表

| 包名 | 版本 | 说明 |
|------|------|------|
| python-dotenv | - | 环境变量管理 |
| streamlit | ~1.54.0 | Web 应用框架 |
| langchain | - | LangChain 核心库 |
| langchain-community | - | LangChain 社区组件 |
| langchain-chroma | - | Chroma 向量存储集成 |
| chromadb | - | Chroma 向量数据库 |
| dashscope | - | 阿里云灵积模型服务 |
| fastapi | ~0.129.0 | 高性能 Web 框架 |
| sqlalchemy | ~2.0.46 | ORM 数据库工具 |
| pydantic | ~2.12.5 | 数据验证库 |
| openai | ~2.20.0 | OpenAI API 客户端 |

## 学习路线

1. **基础入门**: 从 `01_test_apikey.py` 开始，测试 API 密钥配置
2. **OpenAI API**: 学习 `02_openai.py` 掌握基础 API 调用
3. **LangChain 基础**:
   - 模型 (`03_langchain_models/`)
   - 提示词 (`04_langchain_prompts/`)
   - 链 (`05_langchain_chains/`)
   - 记忆 (`06_langchain_memory/`)
4. **数据处理**: 文档加载器 (`07_langchain_loaders/`) 和向量存储 (`08_vector_store/`)
5. **项目实战**: LangChain 项目 (`09_langchain_project/`) 和 RAG 系统 (`10_RAG_project/`)
6. **Web 集成**: FastAPI 集成 (`11_FastAPI/`)

## 快速开始

```bash
# 激活虚拟环境
venv\Scripts\activate

# 运行示例
python 01_test_apikey.py
```

## 注意事项

- 请确保已正确配置 API 密钥
- 向量数据库文件和聊天记录已配置在 `.gitignore` 中，不会被提交
- 建议使用 Python 3.10 及以上版本
