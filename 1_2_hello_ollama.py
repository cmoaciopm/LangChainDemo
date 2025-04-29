from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOllama(model="deepseek-r1:14b")

message = llm.invoke(
    [
        SystemMessage("Translate the following from English into Chinese"),
        HumanMessage("Hello, how are you?")
    ]
)

print(message)