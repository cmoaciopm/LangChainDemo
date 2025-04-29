from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from config.load_key import load_key

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY"),
    temperature=1.7 # Range from 0 to 2
)

for i in range(5):
    response = llm.invoke([HumanMessage("给我的小狗起个炫酷的名字？返回字数要求在4个汉字以内")])
    print(str(i) + ">>" + response.content)