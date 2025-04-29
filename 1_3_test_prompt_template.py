from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.load_key import load_key

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])
prompt = prompt_template.invoke({
    "language": "Chinese",
    "text": "Hello, how are you?"
})

llm = ChatOpenAI(
    model="deepseek-v3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY"),
)

stream = llm.stream(prompt)
for chunk in stream:
    print(chunk.text(), end="\n")
