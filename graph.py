import datetime

from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, MessagesState, StateGraph


@tool
def get_current_time(input: str) -> str:
    """
    Always use this tool to answer any question about the current time.
    It returns the exact UTC time in ISO 8601 format, e.g. '2025-06-04T16:44:45Z'.
    Return EXACTLY this format, without any additional text or explanation.
    """
    now = datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
    return f"The current time is {now}."


llm = ChatOllama(
    model="openhermes",
    temperature=0.2,
)

tools = [get_current_time]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)


def agent_node(state: MessagesState) -> dict:
    messages = state["messages"]

    user_input = (
        messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
    )

    chat_history = []
    for msg in messages[:-1]:
        if isinstance(msg, HumanMessage):
            chat_history.append((msg.content, None))
        elif isinstance(msg, AIMessage):
            if chat_history and chat_history[-1][1] is None:
                chat_history[-1] = (chat_history[-1][0], msg.content)

    result = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    if isinstance(result, str):
        reply = AIMessage(content=result)
    elif isinstance(result, dict) and "output" in result:
        reply = AIMessage(content=result["output"])
    elif isinstance(result, BaseMessage):
        reply = result
    else:
        reply = AIMessage(content=str(result))

    return {"messages": [*messages, reply]}


def build_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent_node)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)
    return builder.compile()
