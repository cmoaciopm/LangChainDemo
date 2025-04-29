from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_redis import RedisChatMessageHistory

from config.load_key import load_key

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

history = RedisChatMessageHistory(
    session_id="test",
    redis_url="redis://localhost:6379/0"
)

runnable = RunnableWithMessageHistory(
    llm,
    get_session_history=lambda: history
)

runnable.invoke({"text": "请重复一次"})