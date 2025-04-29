from langchain_community.embeddings import DashScopeEmbeddings
from config.load_key import load_key

embedding_model = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=load_key("QWEN_API_KEY")
)

text = "This is a test query."
query_result = embedding_model.embed_query(text)
print(query_result)
print(len(query_result))