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
            1. When the user submits a query, first check if a chart has been chosen using the check_chart_name function. 
               If a chart has been selected, retrieve the relevant results by executing the query with get_data_from_db.
               If no chart is chosen, transfer the task to the template agent to assist in chart selection using the RequestTransfer function.
            2. Before processing the query, ensure the database connection is active by using check_connection. 
               If the connection is inactive, establish it using connect_to_db.
            3. Once the connection is confirmed, initialize the query engine with init_nl2sql_engine to handle the query.
            4. Return only the relevant data based on the user’s input, ensuring accuracy and relevance.
            5. Handle errors effectively by notifying users of connection issues or invalid queries, and provide helpful resolutions.
            Your goal is to facilitate smooth database interactions and ensure users receive accurate, relevant data from their queries.
        """

        tools = [
            FunctionToolWithContext.from_defaults(
                async_fn=check_connection,
                description="checks the connection to the database"),
            FunctionToolWithContext.from_defaults(
                async_fn=connect_to_db,
                description="connect to the database if there are no connection and does not take any arguments",

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
        super().__init__(name=name,
                         description=description,
                         system_prompt=system_prompt,
                         tools=tools)
