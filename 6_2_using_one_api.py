from langchain_openai import ChatOpenAI

from config.load_key import load_key

"""
llm = ChatOpenAI(
    model="deepseek-r1:1.5b",
    api_key=load_key("ONE_API_KEY"),
    base_url="http://192.168.31.163:3000/v1"
)
response = llm.invoke("你是谁？")
print(response)
"""

llm2 = ChatOpenAI(
    model="qwen-plus",
    api_key=load_key("ONE_API_KEY"),
    base_url="http://192.168.31.163:3000/v1"
)
response = llm2.invoke("你是谁？")
print(response)