from datetime import datetime, timedelta
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from config.load_key import load_key


@tool
def get_current_date():
    """获取今天的日期"""
    return datetime.datetime.today().strftime("%Y-%m-%d")

@tool
def get_yesterday_date():
    """获取昨天的日期"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

llm_with_tools = llm.bind_tools([
    get_current_date,
    get_yesterday_date
])
all_tools = {
    "get_current_date": get_current_date,
    "get_yesterday_date": get_yesterday_date
}
query = "昨天是几月几日"
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