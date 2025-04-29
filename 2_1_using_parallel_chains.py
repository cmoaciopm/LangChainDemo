from operator import invert

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap, RunnableLambda

from config.load_key import load_key

prompt_template_zh = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into Chinese"),
    ("user", "{text}")
])

prompt_template_fr = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into French"),
    ("user", "{text}")
])

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

parser = StrOutputParser()

chain_zh = prompt_template_zh | llm | parser
chain_fr = prompt_template_fr | llm | parser

parallel_chains = RunnableMap({
    "zh_translation": chain_zh,
    "fr_translation": chain_fr
})

final_chain = parallel_chains | RunnableLambda(lambda x: f"Chinese: {x['zh_translation']}\nFrench: {x['fr_translation']}")

final_chain.get_graph().print_ascii()

print(final_chain.invoke({"text": "Nice to meet you"}))
