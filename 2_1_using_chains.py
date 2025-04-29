from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from config.load_key import load_key

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

parser = StrOutputParser()

chain = prompt_template | llm | parser
print(chain.invoke({"text": "Nice to meet you", "language": "Chinese"}))

analysis_prompt = ChatPromptTemplate.from_template("我应该怎么回答这句话？{talk}。给我一个五个字以内的示例")
chain2 = {"talk": chain} | analysis_prompt | llm | parser
print(chain2.invoke({"text": "Nice to meet you", "language": "Chinese"}))

chain2.get_graph().print_ascii()