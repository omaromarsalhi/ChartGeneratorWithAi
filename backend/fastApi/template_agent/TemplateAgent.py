from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig
from fastApi.template_agent.functions import get_template_names_and_description, save_the_chosen_template, \
    format_the_data_according_to_chart


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
            4. Transfer Task to Data Agent:
               Use RequestTransfer to send the task to the data agent for data retrieval and storage.
            5. Format the Data:
               After the data agent successfully retrieves and stores the data, 
               use format_the_data_according_to_chart to structure the data to fit the selected chart.
            Key Goals:
            - Efficiency: Automate chart selection and data formatting to minimize user intervention.
            - Accuracy: Ensure the selected chart fits the user's needs based on their input.
            - Streamlining: Automatically save and format data for smooth task handover to the data agent.
        """

        tools = [
            FunctionToolWithContext.from_defaults(
                async_fn=get_template_names_and_description,
                description="get the descriptions and names of the available charts"),
            FunctionToolWithContext.from_defaults(
                async_fn=save_the_chosen_template,
                description="save the chosen template",
            ),
            FunctionToolWithContext.from_defaults(
                async_fn=format_the_data_according_to_chart,
                description="format the data according to the chosen chart",
            )
        ]
        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools)

