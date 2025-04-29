from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_redis import RedisChatMessageHistory

from config.load_key import load_key

prompt_template = ChatPromptTemplate.from_messages([
    ("user", "{text}")
])

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

history = RedisChatMessageHistory(
    session_id="test",
    redis_url="redis://localhost:6379/0"
)

parser = StrOutputParser()

chain = prompt_template | llm | parser

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda: history
)

runnable.invoke({"text": "你是谁"})
runnable.invoke({"text": "请重复一次"})