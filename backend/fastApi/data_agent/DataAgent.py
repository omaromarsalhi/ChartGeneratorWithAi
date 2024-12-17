from fastApi.data_agent.functions import check_connection, connect_to_db, init_nl2sql_engine, get_data_from_db, \
     format_the_data_according_to_chart, get_formatted_data, check_chart_existence
from fastApi.orchestration.utils import FunctionToolWithContext
from fastApi.orchestration.workflow import AgentConfig


class DataAgent(AgentConfig):
    def __init__(self):
        name = "Data Agent"
        description = "turn the user input into sql query and execute it"
        system_prompt = """
            You are a data agent responsible for retrieving and processing database information based on user queries.
            on every user query that is related to retrieving data, you should:
             **Chart Selection**: When a query is submitted, check if a chart has been chosen using the `check_chart_existence` function. 
               - If yes, retrieve relevant results by executing the query with `get_data_from_db`. 
               - IF no chart selected,DO transfer the task to the Template Agent and ensure that.
             **Database Connection**: Before processing any query, ensure the database connection is active using `check_connection`.
               - If inactive, establish the connection using `connect_to_db`.
             **Data Formatting** : after getting the data from the database, format it according to the chosen chart using `format_the_data_according_to_chart`.
             do not use `get_formatted_data` function until the user asks to see the formatted data.
             **Query Initialization**: After confirming the connection, initialize the query engine with `init_nl2sql_engine` to handle the user’s query.
        """

        tools = [
            FunctionToolWithContext.from_defaults(async_fn=check_connection),
            FunctionToolWithContext.from_defaults(async_fn=connect_to_db),
            FunctionToolWithContext.from_defaults(async_fn=init_nl2sql_engine),
            FunctionToolWithContext.from_defaults(async_fn=get_data_from_db),
            FunctionToolWithContext.from_defaults(async_fn=check_chart_existence),
            FunctionToolWithContext.from_defaults(async_fn=format_the_data_according_to_chart),
            FunctionToolWithContext.from_defaults(async_fn=get_formatted_data)
        ]

        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools)
