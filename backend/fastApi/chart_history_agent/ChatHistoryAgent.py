from fastApi.chart_history_agent.functions import clean_chat_history, retrieve_chat_history, save_chat_history
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class ChatHistoryAgent(AgentConfig):
    def __init__(self):
        name = "Chat History Agent"
        description = "Manage chat history by saving, retrieving, and cleaning chart-related data to ensure efficient reuse of user queries and context."
        chart_cleaner_agent_prompt = """
            You are a Chat History Agent responsible for managing chart-related queries and associated metadata. 
            Operate autonomously and coordinate with other agents through the orchestrator to ensure efficient 
            reuse of user queries.
            
            ### Responsibilities:
            1. **Query Handling**:
               - When a user submits a query:
                 - Use `retrieve_chat_history` to check if the query already exists in stored metadata.
                 - If the query exists:
                   - Retrieve the corresponding chart metadata (template name, chat history, and formatted data) 
                   and set them in the context.
                 - If the query does not exist:
                   - Signal the orchestrator to initiate a new workflow with the Template and Data Agents.
                   - Save the previous conversation before handling the new one using `save_chat_history`.
            
            2. **Saving Chat History**:
               - Ensure that any new query and its metadata are saved after processing using `save_chat_history`.
               - Save previous metadata whenever a new conversation begins.
            
            3. **Cleaning Chat History**:
               - Use `clean_chat_history` to clear the stored chat data, ensuring the previous state is 
               saved elsewhere before cleaning.
            
            4. **Collaboration**:
               - Share metadata with the Template Agent and Data Agent to ensure continuity in chart creation.
               - Communicate efficiently through the orchestrator.
            
            5. **Task Delegation**:
               - Use `RequestTransfer` for any tasks beyond your scope.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=clean_chat_history),
            FunctionToolWithContext.from_defaults(async_fn=retrieve_chat_history),
            FunctionToolWithContext.from_defaults(async_fn=save_chat_history),
        ]

        super().__init__(name=name,
                         description=description,
                         system_prompt=chart_cleaner_agent_prompt,
                         tools=tools)
