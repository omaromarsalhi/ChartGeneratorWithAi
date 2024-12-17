from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig
from fastApi.template_agent.functions import get_template_names_and_description, save_the_chosen_template


class TemplateAgent(AgentConfig):
    def __init__(self):
        name = "Template Agent"
        description = "chooses the appropriate template of a chart"
        system_prompt = """
            1. Retrieve Chart Options:
               Use the get_template_names_and_description function to fetch available chart templates and descriptions.
            2. Select the Best Chart:
               Analyze the user's input and automatically select the most appropriate chart based on the context and the available templates.
                This eliminates the need for user input on the chart type.
            3. Save the Selected Chart:
               Use save_the_chosen_template to store the selected chart template for future use.
            4. When you finish transfer the job the data agent
        """
        tools = [
            FunctionToolWithContext.from_defaults(async_fn=get_template_names_and_description),
            FunctionToolWithContext.from_defaults(async_fn=save_the_chosen_template)
        ]
        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools)
