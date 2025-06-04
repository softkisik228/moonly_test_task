import datetime
import os

from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from langchain_community.llms import GigaChat
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


@tool
def get_current_time(input: str) -> dict:
    """
    Returns the current UTC time as an ISO8601 string.

    Returns:
        dict: Dictionary with the current UTC time under the 'utc' key.
    """
    now = datetime.datetime.now().replace(microsecond=0).isoformat() + "Z"
    return {"utc": now}


llm = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope="GIGACHAT_API_CORP",
    model="GigaChat-Pro",
    verify_ssl_certs=False,
)

tools = [get_current_time]
agent_executor = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


def agent_node(state):
    """
    Processes the latest user message using the agent executor and adds the assistant's response to the state.

    Args:
        state (MessagesState): The current state containing the conversation messages.

    Returns:
        dict: Updated state with the assistant's response message appended.
    """
    last_user_message = state["messages"][-1]

    if not isinstance(last_user_message, HumanMessage):
        raise ValueError("Last message must be a HumanMessage")

    # Получаем ответ агента (список сообщений)
    result = agent_executor.invoke([last_user_message])

    # Проверяем, что это список BaseMessage
    if isinstance(result, BaseMessage):
        new_messages = [result]
    elif isinstance(result, list) and all(isinstance(m, BaseMessage) for m in result):
        new_messages = result
    else:
        new_messages = [AIMessage(content=str(result))]

    return add_messages(state, new_messages)


def build_graph():
    """
    Builds and compiles the LangGraph state graph for the agent workflow.

    Returns:
        StateGraph: The compiled state graph with the agent node.
    """
    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent_node)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)
    return builder.compile()
