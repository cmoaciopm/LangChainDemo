from langchain.agents import initialize_agent, AgentType
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

agent = initialize_agent(
    tools = [get_city_weather],
    llm = llm,
    agent = AgentType.OPENAI_FUNCTIONS,
    verbose = True
)

query = "北京今天天气怎么样"
response = agent.invoke(query)
print(response)