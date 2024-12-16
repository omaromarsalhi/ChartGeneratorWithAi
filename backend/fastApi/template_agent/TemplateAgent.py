from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig
from fastApi.template_agent.functions import get_template_names_and_description, save_the_chosen_template


class TemplateAgent(AgentConfig):
    def __init__(self):
        name = "Template Agent"
        description = "chooses the appropriate template of a chart"
        system_prompt = """
            You are a data visualization assistant. Given the user's
            input, your task is to automatically choose the most appropriate
            chart from a list of available options. Each chart has a name and
            a description, which you can retrieve using the
            get_template_names_and_description function. Select the chart that
            best fits the user's needs based on their situation and the chart
            descriptions. Once you’ve made your selection, 
            use the save_the_chosen_template function to save the name
            of the chosen chart template for future use. At this step,
            you will not ask the user to choose a chart; your selection
            will be made automatically based on the given context.
            then pass the job to another agent to the data agent to generate the chart with the data from the database by RequestTransfer function.
        """
        tools = [
            FunctionToolWithContext.from_defaults(
                async_fn=get_template_names_and_description,
                description="get the descriptions and names of the available charts"),
            FunctionToolWithContext.from_defaults(
                async_fn=save_the_chosen_template,
                description="save the chosen template",
            )
        ]
        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools)

