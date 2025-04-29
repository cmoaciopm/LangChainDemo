from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage

from config.load_key import load_key

llm = ChatTongyi(
    model="qwen-plus",
    api_key=load_key("QWEN_API_KEY")

)

stream = llm.stream([HumanMessage("你是谁？你能帮我解决什么问题？")])
for chunk in stream:
    print(chunk.text(), end="\n")