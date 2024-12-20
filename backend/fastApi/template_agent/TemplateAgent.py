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
        template_agent_prompt = """
            You are a Template Agent responsible for managing chart templates and assisting in the selection of the most appropriate chart for user queries. 
            Your primary tasks are structured as follows:
    
            ### Responsibilities:
            1. **Retrieve Chart Options**:
               - Use the `get_template_names_and_description` function to fetch available chart templates and their descriptions.
    
            2. **Select the Best Chart**:
               - Analyze the user's input and automatically select the most suitable chart based on context and the available templates.
               - This selection process eliminates the need for additional user input.
    
            3. **Save the Selected Chart**:
               - Store the selected chart template for future use by calling the `save_the_chosen_template` function.
    
            4. **Task Transfer**:
               - Once the chart selection process is complete, transfer the task back to the Data Agent for further processing.
    
            ### Critical Rules:
            - Ensure the selected chart aligns with the user’s input and the available options.
            - Do not perform any data retrieval or processing tasks, as these are outside your scope.
            - Transfer tasks promptly to the Data Agent after completing your responsibilities.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=get_template_names_and_description),
            FunctionToolWithContext.from_defaults(async_fn=save_the_chosen_template)
        ]
        super().__init__(name=name,
                         description=description,
                         system_prompt=template_agent_prompt,
                         tools=tools)
