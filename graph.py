import datetime
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from typing import TypedDict

def get_current_time() -> dict:
    """
    Returns the current UTC time in ISO-8601 format.
    Example result: {"utc": "2025-05-21T06:42:00Z"}
    """
    now = datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
    return {"utc": now}

def chat_node(state: MessagesState) -> dict:
    """
    Accepts the current message state (MessagesState),
    calls the LLM (GPT-3.5-turbo) with the attached get_current_time tool.
    Returns a dictionary {"messages": [AIMessage(...)]}.
    """
    llm = init_chat_model(model="gpt-3.5-turbo")
    llm_with_tools = llm.bind_tools([get_current_time])
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_call_tool(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return "tool"
    return END

def build_graph() -> StateGraph:
    """
    Builds a message processing graph using the LLM and the get_current_time tool.
    """
    builder = StateGraph(MessagesState)
    builder.add_node("chat", chat_node)
    builder.add_node("tool", ToolNode(get_current_time))
    builder.add_edge(START, "chat")
    builder.add_edge("chat", should_call_tool, "tool")
    builder.add_edge("chat", END)
    builder.add_edge("tool", "chat")
    graph = builder.compile()
    return graph