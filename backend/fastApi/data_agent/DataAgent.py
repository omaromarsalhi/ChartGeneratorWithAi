from fastApi.data_agent.functions import check_connection, connect_to_db, init_nl2sql_engine, get_data_from_db, \
    check_chart_name
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class DataAgent(AgentConfig):
    def __init__(self):
        name = "Data Agent"
        description = "turn the user input into sql query and execute it"
        system_prompt = """
            You are a data agent responsible for retrieving database information based on user input.

            1. First, check if the database connection is active using `check_connection`. 
               If the connection is not active, establish it using `connect_to_db`.

            2. Once the connection is confirmed, initialize the query engine with `init_nl2sql_engine`.

            3. When the user submits a query, check if a chart has been chosen by using the `check_chart_name` function. 
               If a chart has been selected, use `get_data_from_db` to execute the query and retrieve relevant results.
               If no chart has been chosen, transfer the task to the template agent to assist in chart selection.

            4. Return only the relevant results based on the user's input.

            5. Handle errors gracefully by informing users about issues such as connection failures or invalid queries 
               and providing appropriate resolutions.

            Your goal is to ensure seamless interaction with the database and return accurate, relevant data to the user.
        """

        tools = [
            FunctionToolWithContext.from_defaults(
                async_fn=check_connection,
                description="checks the connection to the database"),
            FunctionToolWithContext.from_defaults(
                async_fn=connect_to_db,
                description="connect to the database if there are no connection",

            ),
            FunctionToolWithContext.from_defaults(
                async_fn=init_nl2sql_engine,
                description="initialize the nl2sql engine that converts natural language to sql queries then execute them and return the results ",

            ),
            FunctionToolWithContext.from_defaults(
                async_fn=get_data_from_db,
                description="get the data from the database based on the query from the user"),
            FunctionToolWithContext.from_defaults(
                async_fn=check_chart_name,
                description="checks if the the is a chosen chart or no",

            )
        ]
        tools_requiring_human_confirmation = ['save_the_chosen_template']
        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools,
                         tools_requiring_human_confirmation=tools_requiring_human_confirmation)
