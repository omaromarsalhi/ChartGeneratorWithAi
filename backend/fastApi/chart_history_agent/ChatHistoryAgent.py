from fastApi.chart_history_agent.functions import clean_chat_history
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class ChatHistoryAgent(AgentConfig):
    def __init__(self):
        name = "Chat History Agent"
        description = "clean the chat history"
        chart_cleaner_agent_prompt = """
            You are a Chart Cleaner Agent responsible for removing any residual chart-related data. 
            Use the `clean_chart_history` function to clear all chart history effectively. 

            ### Responsibilities:
            1. **Chart History Cleanup**:
               - Call `clean_chart_history` to remove all chart-related data.
               - Ensure the cleanup operation is successful.

            2. **Task Forwarding**:
               - If a task is outside your scope or requires additional processing, forward it to the appropriate agent for handling.
               - Do not attempt to complete tasks beyond your responsibilities.

            ### Critical Rules:
            - Focus solely on chart cleanup within your scope.
            - Forward tasks that require different capabilities to other agents for proper handling.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=clean_chat_history),
        ]

        super().__init__(name=name,
                         description=description,
                         system_prompt=chart_cleaner_agent_prompt,
                         tools=tools)
