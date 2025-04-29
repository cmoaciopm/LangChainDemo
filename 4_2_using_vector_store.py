import redis
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

from config.load_key import load_key

redis_url = "redis://localhost:6379"
redis_client = redis.from_url(redis_url)
print(redis_client.ping())

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

scored_results = vector_store.similarity_search_with_score("又大又圆的水果是什么", k=3)
for doc, score in scored_results:
    print(f"{doc.page_content} - {score}")

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})
documents = retriever.invoke("甜甜的水果是什么？")
for document in documents:
    print(document)
