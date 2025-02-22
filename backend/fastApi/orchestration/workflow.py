import asyncio
import configparser
import os
from typing import Any

from llama_index.core.base.llms.types import MessageRole
from llama_index.llms.cohere import Cohere
from llama_index.llms.gemini import Gemini
from pydantic import BaseModel, ConfigDict, Field

from llama_index.core.llms import ChatMessage, LLM

from llama_index.core.program.function_program import get_function_tool
from llama_index.core.tools import (
    BaseTool,
    ToolSelection,
)
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)
from llama_index.core.workflow.events import InputRequiredEvent, HumanResponseEvent

from fastApi.orchestration.MyMistralAI import MyMistralAI
from fastApi.orchestration.utils import FunctionToolWithContext

config = configparser.ConfigParser()
config.read("../../config.ini")
# os.environ["GOOGLE_API_KEY"] = config.get('API', 'gemini_key')
os.environ["MISTRAL_API_KEY"] = config.get('API', 'mistral_key')


# ---- Pydantic models for config/llm prediction ----


class AgentConfig(BaseModel):
    """Used to configure an agent."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str | None = None
    description: str
    system_prompt: str | None = None
    tools: list[BaseTool] | None = None
    tools_requiring_human_confirmation: list[str] = Field(default_factory=list)


class TransferToAgent(BaseModel):
    """Used to transfer the user to a specific agent."""
    agent_name: str


class RequestTransfer(BaseModel):
    """Used to signal that either you don't have the tools to complete the task, or you've finished your task and want to transfer to another agent."""


# ---- Events used to orchestrate the workflow ----


class ActiveSpeakerEvent(Event):
    pass


class OrchestratorEvent(Event):
    agent_name: str | None = None


class ToolCallEvent(Event):
    tool_call: ToolSelection
    tools: list[BaseTool]


class ToolCallResultEvent(Event):
    chat_message: ChatMessage


class ToolRequestEvent(InputRequiredEvent):
    tool_name: str
    tool_id: str
    tool_kwargs: dict


class ToolApprovedEvent(HumanResponseEvent):
    tool_name: str
    tool_id: str
    tool_kwargs: dict
    approved: bool
    response: str | None = None


class ProgressEvent(Event):
    msg: str


# ---- Workflow ----

# DEFAULT_ORCHESTRATOR_PROMPT = (
#     "You are on orchestration agent.\n"
#     "Your job is to decide which agent to run based on the current state of the user and what they've asked to do.\n"
#     "You do not need to figure out dependencies between agents; the agents will handle that themselves.\n"
#     "Always start with the Template Agent"
#     "Here the the agents you can choose from:\n{agent_context_str}\n\n"
#     "Here is the current user state:\n{user_state_str}\n\n"
#     "Current Working Agent: {current_agent}\n\n"
#     "Do not transfer any agent to itself"
#     "Please assist the user and the agents and transfer them as needed."
#     "### Critical Rules:\n"
#     "- Never delegate tasks to agents outside the provided list.\n"
#     "- Avoid redundant or circular task transfers if it occurs figure out the problem and return the error to the user.\n\n"
#     "Error Handling: Notify users promptly of any issues, such as connection errors or invalid queries, and provide helpful resolutions."
# )

# DEFAULT_ORCHESTRATOR_PROMPT = (
#     "You are an orchestration agent.\n"
#     "Your job is to decide which agent to run based on the current state of the user and what they've asked to do.\n"
#     "You have two agents to choose from:\n"
#     "Here the agents you can choose from:\n{agent_context_str}\n\n"
#     "Here is the current user state:\n{user_state_str}\n\n"
#     "Here is the current working agent:\n{current_agent}\n\n"
#     "If the other agent request a specific agent to handle the task, you should transfer the task to that agent and this is his name {agent_name}"
#     " and if none or the name provided does not exist then do chose by yourself .\n"
#     "Do not transfer any agent to itself"
#     "Based on the user input and the current state, please decide the next step.\n"
#     "Please assist the user and the agents and transfer them as needed."
# )
# DEFAULT_ORCHESTRATOR_PROMPT = (
#     "You are an orchestration agent responsible for selecting and delegating tasks between agents or interacting naturally with the user as needed.\n\n"
#     "### Available Agents:\n"
#     "{agent_context_str}\n\n"
#     "### Current State:\n"
#     "- User State: {user_state_str}\n"
#     "- Current Working Agent: {current_agent}\n\n"
#     "### Instructions:\n"
#     "1. When selecting an agent, return the agent name **exactly as it is provided** in the list of available agents, preserving spaces, capitalization, and formatting.\n"
#     "2. If no specific agent is requested or the requested name is invalid, choose the most appropriate agent from the list.\n"
#     "3. Do not transfer tasks back to the current agent unless it explicitly makes a valid request.\n"
#     "4. If no agent is suitable or clarification is needed, interact with the user naturally without referencing function names, internal states, or chat history unless explicitly instructed.\n\n"
#     "### Critical Rules:\n"
#     "- Always return the agent name **exactly as it appears** in the provided list.\n"
#     "- Do not modify, reformat, or alter the agent name in any way.\n"
#     "- Avoid infinite loops or unnecessary task circulation unless specifically driven by a functional need."
# )

DEFAULT_ORCHESTRATOR_PROMPT = (
    "You are the Orchestrator Agent responsible for managing user requests and coordinating with system agents.\n"
    "Your job is to:\n"
    "- Manage and delegate tasks efficiently by choosing the appropriate agent.\n"
    "- Ensure smooth interaction between system agents and the user.\n\n"

    "### Available Agents:\n"
    "{agent_context_str}\n\n"

    "### Current State:\n"
    "- User State: {user_state_str}\n"
    "- Current Working Agent: {current_agent}\n\n"

    "### Rules:\n"
    "- Do not delegate tasks to agents outside the provided list.\n"
    "- Avoid redundant or circular transfers.\n"
    "- Inform users of any errors (e.g., invalid queries or connection issues) and provide helpful solutions.\n"
    "- Always call the Chat History Agent first when the user submits a **new query** that requests a new workflow. \n"
    "  - Wait for the Chat History Agent to save the query and then proceed to answer the user query by delegating it to the relevant agents as needed.\n\n"

    "### Guidelines:\n"
    "1. Handle simple requests directly if possible.\n"
    "2. Delegate data-related requests to the Data Agent and template-related tasks to the Template Agent.\n"
    "3. If no solution exists, explain the limitation to the user clearly.\n\n"

    "Your goal is to ensure efficient and seamless coordination among system agents to fulfill user requests."
)

# DEFAULT_ORCHESTRATOR_PROMPT = """
#
# You are an Orchestrator Agent responsible for coordinating tasks between agents and ensuring a seamless workflow.
#
# ### Available Agents:
# {agent_context_str}
#
# ### Current State:
# - User State: {user_state_str}
# - Current Working Agent: {current_agent}
#
# ### Instructions:
# 1. **Query Workflow**:
#    - When a user submits a query:
#      - Ask the Chat History Agent to check for existing metadata using `retrieve_chat_history`.
#      - If **history exists**:
#        - Proceed with the current conversation using the existing data.
#      - If **no history exists**:
#        - Directly proceed with the new query without saving or cleaning anything.
#        - Delegate tasks to the **Template Agent** for chart selection and the **Data Agent** for data retrieval and formatting.
#        - No saving or cleaning of chat history is required.
#
# 2. **New Topic Detection**:
#    - If the user asks a new question or a new topic is detected:
#      - If **history exists**:
#        - First, save the current chat history using `save_chat_history`.
#        - Then, clean the old chat history using `clean_chat_history`.
#        - Proceed with handling the new query.
#      - If no history exists, just proceed with the new query directly.
#
# 3. **Agent Selection**:
#    - Choose the most suitable agent based on the task requirements.
#    - Return the agent name **exactly as it appears** in the list.
#
# 4. **Collaboration and Escalation**:
#    - Ensure agents share metadata and collaborate effectively.
#    - Handle escalations or out-of-scope tasks via `RequestTransfer`.
#
# 5. **Critical Rules**:
#    - Do not modify agent names or reformat them.
#    - Avoid infinite loops or unnecessary task circulation.
#    - Interact naturally with the user when clarification is needed but avoid referencing internal states or function names.
# """

DEFAULT_TOOL_REJECT_STR = "The tool call was not approved, likely due to a mistake or preconditions not being met."


class OrchestratorAgent(Workflow):
    def __init__(
            self,
            orchestrator_prompt: str | None = None,
            default_tool_reject_str: str | None = None,
            **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.orchestrator_prompt = orchestrator_prompt or DEFAULT_ORCHESTRATOR_PROMPT
        self.default_tool_reject_str = (
                default_tool_reject_str or DEFAULT_TOOL_REJECT_STR
        )

    @step
    async def setup(
            self, ctx: Context, ev: StartEvent
    ) -> ActiveSpeakerEvent | OrchestratorEvent:
        """Sets up the workflow, validates inputs, and stores them in the context."""
        active_speaker = await ctx.get("active_speaker", default="")
        user_msg = ev.get("user_msg")
        agent_configs = ev.get("agent_configs", default=[])
        llm: LLM = ev.get("llm", default=MyMistralAI())
        # llm: LLM = ev.get("llm", default=Gemini(model_name="models/gemini-2.0-flash-exp"))

        chat_history = ev.get("chat_history", default=[])
        initial_state = ev.get("initial_state", default={})
        if (
                user_msg is None
                or agent_configs is None
                or llm is None
                or chat_history is None
        ):
            raise ValueError(
                "User message, agent configs, llm, and chat_history are required!"
            )
        if not llm.metadata.is_function_calling_model:
            print(llm.metadata)
            raise ValueError("LLM must be a function calling model!")

        # store the agent configs in the context
        agent_configs_dict = {ac.name: ac for ac in agent_configs}
        await ctx.set("agent_configs", agent_configs_dict)
        await ctx.set("llm", llm)

        chat_history.append(ChatMessage(role=MessageRole.USER, content=user_msg))
        await ctx.set("chat_history", chat_history)

        await ctx.set("user_state", initial_state)

        # if there is an active speaker, we need to transfer forward the user to them
        if active_speaker:
            return ActiveSpeakerEvent()

        # otherwise, we need to decide who the next active speaker is
        return OrchestratorEvent(user_msg=user_msg)

    @step
    async def speak_with_sub_agent(
            self, ctx: Context, ev: ActiveSpeakerEvent
    ) -> ToolCallEvent | ToolRequestEvent | StopEvent:
        """Speaks with the active sub-agent and handles tool calls (if any)."""

        active_speaker = await ctx.get("active_speaker")

        agent_config: AgentConfig = (await ctx.get("agent_configs"))[active_speaker]
        chat_history = await ctx.get("chat_history")
        llm = await ctx.get("llm")

        user_state = await ctx.get("user_state")
        user_state_str = "\n".join([f"{k}: {v}" for k, v in user_state.items()])
        system_prompt = (
                agent_config.system_prompt.strip()
                + f"\n\nHere is the current user state:\n{user_state_str}"
        )

        llm_input = [ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)] + chat_history
        print("llm_input: ", llm_input)
        # inject the request transfer tool into the list of tools
        tools = [get_function_tool(RequestTransfer)] + agent_config.tools

        await asyncio.sleep(2)
        response = await llm.achat_with_tools(tools, chat_history=llm_input)

        tool_calls: list[ToolSelection] = llm.get_tool_calls_from_response(
            response, error_on_no_tool_call=False
        )
        print("number of tools: ", len(tool_calls))
        for tool_call in tool_calls:
            print("chosen tool by th agent", tool_call)

        if len(tool_calls) == 0:
            chat_history.append(response.message)
            await ctx.set("chat_history", chat_history)
            return StopEvent(
                result={
                    "response": response.message.content,
                    "chat_history": chat_history,
                }
            )

        await ctx.set("num_tool_calls", len(tool_calls))

        for tool_call in tool_calls:
            if tool_call.tool_name == "RequestTransfer":
                await ctx.set("active_speaker", None)
                ctx.write_event_to_stream(
                    ProgressEvent(msg="Agent is requesting a transfer. Please hold.")
                )
                return OrchestratorEvent()

            elif tool_call.tool_name in agent_config.tools_requiring_human_confirmation:
                ctx.write_event_to_stream(
                    ToolRequestEvent(
                        prefix=f"Tool {tool_call.tool_name} requires human approval.",
                        tool_name=tool_call.tool_name,
                        tool_kwargs=tool_call.tool_kwargs,
                        tool_id=tool_call.tool_id,
                    )
                )
            else:
                ctx.send_event(
                    ToolCallEvent(tool_call=tool_call, tools=agent_config.tools)
                )

        chat_history.append(response.message)
        await ctx.set("chat_history", chat_history)

    @step
    async def handle_tool_approval(
            self, ctx: Context, ev: ToolApprovedEvent
    ) -> ToolCallEvent | ToolCallResultEvent:
        """Handles the approval or rejection of a tool call."""
        if ev.approved:
            active_speaker = await ctx.get("active_speaker")
            agent_config = (await ctx.get("agent_configs"))[active_speaker]
            return ToolCallEvent(
                tools=agent_config.tools,
                tool_call=ToolSelection(
                    tool_id=ev.tool_id,
                    tool_name=ev.tool_name,
                    tool_kwargs=ev.tool_kwargs,
                ),
            )
        else:
            new_response = ("the user has rejected the tool call and this is his reason : " + ev.response + " ."
                                                                                                            "if his reason does not make any sense then take this instead "
                            + self.default_tool_reject_str)
            return ToolCallResultEvent(
                chat_message=ChatMessage(
                    role=MessageRole.TOOL,
                    # content=ev.response or self.default_tool_reject_str,
                    content=new_response,
                    additional_kwargs={
                        "tool_call_id": ev.tool_id,
                        "name": ev.tool_name,
                    },
                )
            )

    @step(num_workers=4)
    async def handle_tool_call(
            self, ctx: Context, ev: ToolCallEvent
    ) -> ActiveSpeakerEvent:
        """Handles the execution of a tool call."""

        tool_call = ev.tool_call
        tools_by_name = {tool.metadata.get_name(): tool for tool in ev.tools}

        tool = tools_by_name.get(tool_call.tool_name)
        additional_kwargs = {
            "tool_call_id": tool_call.tool_id,
            "name": tool.metadata.get_name(),
        }
        if not tool:
            tool_msg = ChatMessage(
                role=MessageRole.TOOL,
                content=f"Tool {tool_call.tool_name} does not exist",
                additional_kwargs=additional_kwargs,
            )

        try:
            if isinstance(tool, FunctionToolWithContext):
                tool_output = await tool.acall(ctx, **tool_call.tool_kwargs)
            else:
                tool_output = await tool.acall(**tool_call.tool_kwargs)

            tool_msg = ChatMessage(
                role=MessageRole.TOOL,
                content=tool_output.content,
                additional_kwargs=additional_kwargs,
            )
        except Exception as e:
            tool_msg = ChatMessage(
                role=MessageRole.TOOL,
                content=f"Encountered error in tool call: {e}",
                additional_kwargs=additional_kwargs,
            )

        ctx.write_event_to_stream(
            ProgressEvent(
                msg=f"Tool {tool_call.tool_name} called with {tool_call.tool_kwargs} returned {tool_msg.content}"
            )
        )

        return ToolCallResultEvent(chat_message=tool_msg)

    @step
    async def aggregate_tool_results(
            self, ctx: Context, ev: ToolCallResultEvent
    ) -> ActiveSpeakerEvent:
        """Collects the results of all tool calls and updates the chat history."""
        num_tool_calls = await ctx.get("num_tool_calls")
        results = ctx.collect_events(ev, [ToolCallResultEvent] * num_tool_calls)

        if not results:
            return

        chat_history = await ctx.get("chat_history")
        for result in results:
            chat_history.append(result.chat_message)
        await ctx.set("chat_history", chat_history)

        return ActiveSpeakerEvent()

    @step
    async def orchestrator(
            self, ctx: Context, ev: OrchestratorEvent
    ) -> ActiveSpeakerEvent | StopEvent:
        """Decides which agent to run next, if any."""
        agent_configs = await ctx.get("agent_configs")
        chat_history = await ctx.get("chat_history")

        agent_context_str = ""
        for agent_name, agent_config in agent_configs.items():
            agent_context_str += f"{agent_name}: {agent_config.description}\n"

        user_state = await ctx.get("user_state")
        user_state_str = "\n".join([f"{k}: {v}" for k, v in user_state.items()])

        current_agent_name = await ctx.get("active_agent", default="None")
        print("current_agent_name: ", current_agent_name)
        system_prompt = self.orchestrator_prompt.format(
            agent_context_str=agent_context_str, user_state_str=user_state_str, current_agent=current_agent_name
        )

        # system_prompt = self.orchestrator_prompt.format(
        #     agent_context_str=agent_context_str, user_state_str=user_state_str
        # )

        llm_input = [ChatMessage(role="system", content=system_prompt)] + chat_history
        llm = await ctx.get("llm")
        print("llm_input orchestrator: ", llm_input)
        # convert the TransferToAgent pydantic model to a tool
        tools = [get_function_tool(TransferToAgent)]

        await asyncio.sleep(2)
        response = await llm.achat_with_tools(tools, chat_history=llm_input)

        tool_calls = llm.get_tool_calls_from_response(
            response, error_on_no_tool_call=False
        )
        print("number of tools of orchestrator: ", len(tool_calls))
        for tool_call in tool_calls:
            print("from orchestrator", tool_call)
        # if no tool calls were made, the orchestrator probably needs more information
        if len(tool_calls) == 0:
            chat_history.append(response.message)
            return StopEvent(
                result={
                    "response": response.message.content,
                    "chat_history": chat_history,
                }
            )

        tool_call = tool_calls[0]
        selected_agent = tool_call.tool_kwargs["agent_name"]
        await ctx.set("active_speaker", selected_agent)
        await ctx.set("active_agent", selected_agent)

        ctx.write_event_to_stream(
            ProgressEvent(msg=f"Transferring to agent {selected_agent}")
        )

        return ActiveSpeakerEvent()
