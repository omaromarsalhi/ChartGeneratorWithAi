from fastApi.chart_history_agent.functions import clean_chat_history
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class ChatHistoryAgent(AgentConfig):
    def __init__(self):
        name = "Chat History Agent"
        description = "clean the chat history"
        chart_cleaner_agent_prompt = """
            You are a Chart Cleaner Agent responsible for clearing chart-related data. 
            Operate autonomously and use `RequestTransfer` to delegate tasks outside your scope. 
            Do not interact with the user directly or request their input.
            ### Responsibilities:
            1. **Chart History Cleanup**:
                - Use `clean_chart_history` to clear all chart-related data.
            2. **Task Transfer**:
                - Use `RequestTransfer` to delegate tasks beyond your scope.
                - Do not ask the user for any input at any stage.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=clean_chat_history),
        ]

        super().__init__(name=name,
                         description=description,
                         system_prompt=chart_cleaner_agent_prompt,
                         tools=tools)
