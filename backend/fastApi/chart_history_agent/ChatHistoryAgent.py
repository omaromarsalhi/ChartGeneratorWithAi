from fastApi.chart_history_agent.functions import clean_chat_history, retrieve_chat_history, save_chat_history
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class ChatHistoryAgent(AgentConfig):
    def __init__(self):
        name = "Chat History Agent"
        description = "Manage chat history by saving, retrieving, and cleaning chart-related data to ensure efficient reuse of user queries and context."
        chart_cleaner_agent_prompt = (
            "You are the Chat History Agent, responsible for managing and saving chart-related queries and metadata.\n"
            "Responsibilities:\n"
            "1. **Query Handling**:\n"
            "   - Check if the user's query exists in stored metadata using `retrieve_chat_history`:\n"
            "     - If it exists, retrieve and set the associated metadata (template name, chat history, and formatted data).\n"
            "     - If it does not exist, save the previous query using `save_chat_history`, then signal the Orchestrator to proceed with the Template Agent.\n"
            "2. **Collaboration**:\n"
            "   - Work with the Orchestrator to delegate tasks to other agents as needed.\n"
        )

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=clean_chat_history),
            FunctionToolWithContext.from_defaults(async_fn=retrieve_chat_history),
            FunctionToolWithContext.from_defaults(async_fn=save_chat_history),
        ]

        super().__init__(name=name,
                         description=description,
                         system_prompt=chart_cleaner_agent_prompt,
                         tools=tools)
