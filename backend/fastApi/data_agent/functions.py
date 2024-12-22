from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.workflow import Context
from llama_index.llms.gemini import Gemini

from fastApi.data_agent.Config import Config
from fastApi.data_agent.Database import Database
from fastApi.data_agent.Nl2SqlEngine import Nl2SqlEngine
from fastApi.data_agent.prompt import formating_prompt
from fastApi.orchestration.workflow import ProgressEvent
from sqlalchemy.exc import OperationalError

from fastApi.utils.utils import get_template_example_data_by_name, create_query_message, semantic_comparison


async def check_chart_existence(ctx: Context, user_query: str) -> bool:
    """Checks if a chart has already been selected for the given user query by inspecting the context for the 'template_name'.

    Returns:
        bool: True if a chart has been selected for the query, otherwise False.
    """
    template_name = await ctx.get("template_name", None)
    if template_name is not None:
        return True
    return False


async def check_connection(ctx: Context):
    """Verifies if a valid connection to the database exists by checking the context for the 'database'.

    Returns:
        bool: True if a valid database connection is established, otherwise False.
    """
    database = await ctx.get("database", None)
    if database is None:
        return False
    return True


async def connect_to_db(ctx: Context) -> str:
    """Establishes a connection to the database and stores the connection in the context for future use.

    Returns:
        str: A message confirming the success of the database connection.
    """
    config = Config("../../config.ini")
    ctx.write_event_to_stream(ProgressEvent(msg="connecting to the database..."))
    database = Database(config)
    await ctx.set("config", config)
    await ctx.set("database", database)
    return "Database connection established."


async def init_nl2sql_engine(ctx: Context) -> str:
    """Initializes the NL2SQL engine, enabling the conversion of natural language queries into SQL queries for database retrieval.

    Returns:
        str: A message confirming the initialization of the NL2SQL engine.
    """
    config = await ctx.get("config")
    database = await ctx.get("database")
    nl2sql_engine = Nl2SqlEngine(config, database)
    await ctx.set("nl2sql_engine", nl2sql_engine)
    return "NL2SQL engine initialized."


async def get_data_from_db(ctx: Context, user_query: str):
    """Retrieves data from the database based on the user's natural language query by converting it into an appropriate SQL query.

    Returns:
        str: A message confirming the successful retrieval of data from the database.
    """
    template_name = await ctx.get("template_name")
    query_message = create_query_message(user_query, template_name)
    nl2sql_engine = await ctx.get("nl2sql_engine")
    query_result = nl2sql_engine.query(query_message)
    await ctx.set("query_result", query_result)
    return f"Data retrieved successfully from the database."


async def format_the_data_according_to_chart(ctx: Context) -> str:
    """Formats the retrieved data according to the selected chart type, ensuring it matches the required structure for display.

    Returns:
        str: A message confirming the successful formatting of the data according to the chart.
    """
    query_result = await ctx.get("query_result")
    template_name = await ctx.get("template_name")
    if query_result is None:
        return "No data found."
    else:
        config = await ctx.get("config")
        llm = Gemini(api_key=config.get('API', 'gemini_key'))
        formated_prompt = formating_prompt.format(
            dataset=query_result,
            chart_example=get_template_example_data_by_name(template_name)
        )
        formatted_data = llm.complete(formated_prompt)
        await ctx.set("formatted_data", formatted_data)
        return "Data formatted according to the chart and stored in the context."


async def get_formatted_data(ctx: Context) -> str:
    """Retrieves the formatted data from the context, which has been prepared according to the user's selected chart.

    Returns:
        str: The formatted data message ready for presentation to the user.
    """
    formatted_data = await ctx.get("formatted_data")
    return f"This is the formatted data: {formatted_data}"

