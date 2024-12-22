from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig
from fastApi.template_agent.functions import get_template_names_and_description, save_the_chosen_template


class TemplateAgent(AgentConfig):
    def __init__(self):
        name = "Template Agent"
        description = "chooses the appropriate template of a chart if the is no chart selected"
        system_prompt = """
            1. Retrieve Chart Options:
               Use the get_template_names_and_description function to fetch available chart templates and descriptions.
            2. Select the Best Chart:
               Analyze the user's input and automatically select the most appropriate chart based on the context and the available templates.
                This eliminates the need for user input on the chart type.
            3. Save the Selected Chart:
               Use save_the_chosen_template to store the selected chart template for future use.
            4. When you finish transfer the job the `Data Agent`
        """,
        template_agent_prompt ="""
            You are a Template Agent managing chart templates. 
            You must never interact with the user directly. Instead, always perform your tasks autonomously 
            and transfer any responsibility back to the orchestrator using `RequestTransfer`.
            ### Responsibilities:
            1. **Retrieve Chart Options**:
                - Use `get_template_names_and_description` to fetch available chart templates.
            2. **Select the Best Chart**:
                - Automatically select the most suitable chart based on context without asking for user input.
            3. **Save the Selected Chart**:
                - Save the chosen chart using `save_the_chosen_template` without any user confirmation.
            4. **Task Transfer**:
                - Use `RequestTransfer` to delegate tasks beyond your scope.
                - Do not ask the user for any input at any stage.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=get_template_names_and_description),
            FunctionToolWithContext.from_defaults(async_fn=save_the_chosen_template)
        ]
        super().__init__(name=name,
                         description=description,
                         system_prompt=template_agent_prompt,
                         tools=tools)
