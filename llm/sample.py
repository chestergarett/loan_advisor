from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

messages = [
    (
        "system",
        "You are a helpful assistant that gives financial advise.",
    ),
    ("human", "What to do I am drowning in debt?"),
]

ai_msg = llm.invoke(messages)
print(ai_msg)