from langchain.tools import tool
from langchain_openai import ChatOpenAI

from config.load_key import load_key


@tool(description="获取某个城市的天气")
def get_city_weather(city:str):
    """
    :param city: 城市
    :return:
    """
    return "城市" + city + "今天天气不错"

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

llm_with_tools = llm.bind_tools([
    get_city_weather
])
all_tools = {
    "get_city_weather": get_city_weather
}
query = "北京今天天气怎么样？"
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