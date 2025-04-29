from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.load_key import load_key

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

prompt = ChatPromptTemplate.from_messages(["human", "把{sentence}翻译成{language}"])
#prompt = ChatPromptTemplate.from_messages([("human", "你好，请用下面这种语言回答我的问题 {language}")])

parser = StrOutputParser()

chain = prompt | llm | parser
as_tool = chain.as_tool(name="translatetool", description="翻译工具")

all_tools = {"translatetool": as_tool}
print(as_tool.args)
llm_with_tools = llm.bind_tools([as_tool])

#query = "今天天气真冷，这句话用英语怎么回答？"
query = "如何用英语回复这句话“今天天气真冷”？要求使用更随意的表达方式。"
messages = [query]

ai_msg = llm_with_tools.invoke(messages)
print(f"Message from LLM: {ai_msg}")
messages.append(ai_msg)

if ai_msg.tool_calls:
    for tool_call in ai_msg.tool_calls:
        selected_tool = all_tools[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        print(f"Message from tool: {tool_msg}")
        messages.append(tool_msg)

result = llm_with_tools.invoke(messages).content
print(result)