import re

from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI

from config.load_key import load_key

# 1.加载文档
loader = TextLoader("./resource/meituan-questions.txt")
documents = loader.load()

# 2.切分文档
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0,
    separator="\n\n",
    keep_separator=True
)

"""
segments = text_splitter.split_documents(documents)
print(len(segments))
for segment in segments:
    print(segment.page_content)
    print("-------")
"""
texts = re.split(r'\n\n', documents[0].page_content)
segments = text_splitter.create_documents(texts)
print(len(segments))
for segment in segments:
    print(segment.page_content)
    print("-------")

# 3.文本向量化
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v1",
    dashscope_api_key=load_key("QWEN_API_KEY")
)
redis_url = "redis://localhost:6379"
config = RedisConfig(
    index_name="meituan-index",
    redis_url=redis_url
)
vector_store = RedisVectorStore(embedding_model, config)
vector_store.add_documents(segments)

# 4.检索相关信息
query = "在线支付取消订单后钱怎么返还"
retriever = vector_store.as_retriever()
relative_segments = retriever.invoke(query, k=5)
print(relative_segments)

# 5.构建prompt提示词
prompt_template = ChatPromptTemplate.from_messages([("user",
    """
        你是一个答疑机器人，你的任务是根据下述给定的已知信息回答用户的问题。
        已知信息：{context}
        用户问题：{question}
        如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复“我无法回答您的问题”。
        请不要输出已知信息中不包含的信息或答案。
        请用中文回答用户问题。
    """)
])
text = []
for segment in relative_segments:
    text.append(segment.page_content)
prompt = prompt_template.invoke({"context":text, "question":query})
print(prompt)


# 6.调用大模型
llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)
response = llm.invoke(prompt)
print(response.content)