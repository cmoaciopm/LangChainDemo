from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI

from config.load_key import load_key


def get_city_weather(city:str):
    return "城市" + city + "今天天气不错"

llm = ChatOpenAI(
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=load_key("QWEN_API_KEY")
)

weather_tool = StructuredTool.from_function(
    func=get_city_weather,
    description="获取某个城市的天气"
)

llm_with_tools = llm.bind_tools([
    weather_tool
])
all_tools = {
    "get_city_weather": weather_tool
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