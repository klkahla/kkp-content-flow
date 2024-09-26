import functools
import operator

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
    AIMessage
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

from typing import Annotated, Sequence, TypedDict, Literal

class MultiAgentRepository:
    def __init__(self, model):
        self.model = model

    def get_content(self, prompt_message):

        # BlogWriter agent and node
        blog_writer_agent = self.create_agent(
            self.model,
            [],
            system_message="You must provide high quality and engaging content for the editor to review.",
        )
        blog_writer_node = functools.partial(self.agent_node, agent=blog_writer_agent, name="BlogWriter")

        # editor
        editor_agent = self.create_agent(
            self.model,
            [],
            system_message="You must either approve the content from the blog writer or provide a list of improvements to the blog. Any content you approve will be scheduled on the blog and available for target clients to consume. If there are no improvements to be made, print the final blog starting with FINAL ANSWER",
        )
        editor_node = functools.partial(self.agent_node, agent=editor_agent, name="editor")

        # Tools
        tools = []
        tool_node = ToolNode(tools)

        workflow = StateGraph(AgentState)

        workflow.add_node("BlogWriter", blog_writer_node)
        workflow.add_node("editor", editor_node)
        workflow.add_node("call_tool", tool_node)

        workflow.add_conditional_edges(
            "BlogWriter",
            self.router,
            {"continue": "editor", "call_tool": "call_tool", "__end__": END},
        )
        workflow.add_conditional_edges(
            "editor",
            self.router,
            {"continue": "BlogWriter", "call_tool": "call_tool", "__end__": END},
        )

        workflow.add_conditional_edges(
            "call_tool",
            # Each agent node updates the 'sender' field
            # the tool calling node does not, meaning
            # this edge will route back to the original agent
            # who invoked the tool
            lambda x: x["sender"],
            {
                "BlogWriter": "BlogWriter",
                "editor": "editor",
            },
        )
        workflow.add_edge(START, "BlogWriter")
        graph = workflow.compile()

        events = graph.stream(
            {
                "messages": [
                    HumanMessage(
                        content=prompt_message
                    )
                ],
            },
            # Maximum number of steps to take in the graph
            {"recursion_limit": 10},
        )
        for s in events:
            print(s)
            print("----")


    def create_agent(self, llm, tools, system_message: str):
        """Create an agent."""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK, another assistant with different tools "
                    " will help where you left off. Execute what you can to make progress."
                    " \n{system_message}",
                    # " You have access to the following tools: {tool_names}.\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(system_message=system_message)
        # prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        # return prompt | llm.bind_tools(tools)
        return prompt | llm
    
    # Helper function to create a node for a given agent
    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        # We convert the agent output into a format that is suitable to append to the global state
        if isinstance(result, ToolMessage):
            pass
        else:    
            result_dict = result.dict(exclude={"type", "name"})
            result = AIMessage(content=str(result_dict), name=name)
        return {
            "messages": [result],
            # Since we have a strict workflow, we can
            # track the sender so we know who to pass to next.
            "sender": name,
        }
    
    def router(self, state) -> Literal["call_tool", "__end__", "continue"]:
        # This is the router
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            # The previous agent is invoking a tool
            return "call_tool"
        if "FINAL ANSWER" in last_message.content:
            # Any agent decided the work is done
            return "__end__"
        return "continue"

    

# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str