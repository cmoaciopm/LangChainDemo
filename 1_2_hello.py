from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from config.load_key import load_key

llm = ChatOpenAI(
    model="deepseek-v3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

message = llm.invoke(
    [
        HumanMessage("你是谁？你能帮我解决什么问题？")
    ]
)
print(message)