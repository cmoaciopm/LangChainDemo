import uvicorn
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes

from config.load_key import load_key

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

parser = StrOutputParser()

chain = prompt_template | llm | parser

output = chain.invoke({"text": "nice to meet you", "language": "Chinese"})
print(output)

app = FastAPI(
    title="大模型语言翻译助手",
    version="v1.0",
    description="基于LangChain框架构建的大模型语言翻译助手"
)
add_routes(app, chain, path="/langchainDemo")

uvicorn.run(app, host="127.0.0.1", port=8000)
