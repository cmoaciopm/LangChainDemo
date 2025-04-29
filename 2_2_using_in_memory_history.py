from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI

from config.load_key import load_key

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

history = InMemoryChatMessageHistory()
history.add_user_message("你是谁？")
ai_message = llm.invoke(history.messages)
print(ai_message.content)
history.add_message(ai_message)

history.add_user_message("请重复一次")
ai_message2 = llm.invoke(history.messages)
print(ai_message2.content)
history.add_message(ai_message2)

