"""
前提：meituan-questions.txt里的内容已经全部向量化。也就是说文件5_practicing_rag.py中的1-3步都以执行过
"""

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_openai import ChatOpenAI
from operator import itemgetter

from config.load_key import load_key

query = "在线支付取消订单后钱怎么返还"

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
retriever = vector_store.as_retriever()

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

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

def collect_documents(segments):
    text = []
    for segment in segments:
        text.append(segment.page_content)
    return text

chain = (
    {
        "context": itemgetter("question") | retriever | collect_documents,
        "question": itemgetter("question")
    }
    | prompt_template
    | llm
    | StrOutputParser()
)

response = chain.invoke({"question":query})
print(response)