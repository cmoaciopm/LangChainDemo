from langchain_core.prompts import ChatPromptTemplate
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

from config.load_key import load_key

prompt = ChatPromptTemplate([
    ("human", "{question}")
])

def format_prompt_value(prompt_value):
    return prompt_value.to_string()

redis_url = "redis://localhost:6379"
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=load_key("QWEN_API_KEY")
)
config = RedisConfig(
    index_name="fruit",
    redis_url=redis_url
)
vector_store = RedisVectorStore(embedding_model, config=config)
vector_store.add_texts([
    "香蕉很长",
    "苹果很甜",
    "西瓜又大又圆",
    "榴莲甜但刺很多",
    "椰子不大但很圆",
    "菠萝蜜很甜"
])
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})

chain = prompt | format_prompt_value | retriever

documents = chain.invoke({"question": "甜甜的水果是什么？"})
for document in documents:
    print(document)