from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig
from functions import get_template_names_and_description, save_the_chosen_template


class TemplateAgent(AgentConfig):
    def __init__(self):
        self.NAME = "Template Agent"
        self.DESCRIPTION = "chooses the appropriate template of a chart"
        self.SYSTEM_PROMPT = """
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
        """
        self.TOOLS = [FunctionToolWithContext.from_defaults(
            async_fn=get_template_names_and_description,
            description="get the descriptions and names of the available charts"),
            FunctionToolWithContext.from_defaults(
                async_fn=save_the_chosen_template,
                description="save the chosen template",

            )

        ]
        self.TOOLS_REQUIRING_HUMAN_CONFIRMATION = ['save_the_chosen_template']
        super().__init__(name=self.NAME,
                         description=self.DESCRIPTION,
                         system_prompt=self.SYSTEM_PROMPT,
                         tools=self.TOOLS,
                         tools_requiring_human_confirmation=self.TOOLS_REQUIRING_HUMAN_CONFIRMATION)
