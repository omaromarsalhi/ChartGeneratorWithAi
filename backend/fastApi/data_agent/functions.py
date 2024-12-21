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
    """Check if the chart for the user query has been chosen or not."""
    charts_metadata = await ctx.get("charts_metadata",default=[])
    for chart_metadata in charts_metadata:
        # chat_history = await ctx.get("chat_history")
        # chat_history = chat_history[-1]
        # await ctx.set("chat_history", chat_history)
        if semantic_comparison(chart_metadata.user_query, user_query, await ctx.get("config")):
            return True
    return False


async def check_connection(ctx: Context):
    """Check if the database connection is successful."""
    database = await ctx.get("database")
    try:
        with database.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except OperationalError as e:
        return False


async def connect_to_db(ctx: Context) -> str:
    """Connect to the database and save the connection in the context."""
    config = Config("../../config.ini")
    ctx.write_event_to_stream(ProgressEvent(msg="connecting to the database..."))
    database = Database(config)
    await ctx.set("config", config)
    await ctx.set("database", database)
    return "Database connection established."


async def init_nl2sql_engine(ctx: Context) -> str:
    """Initializes the NL2SQL engine to let user convert natural language to SQL and select data from the database."""
    config = await ctx.get("config")
    database = await ctx.get("database")
    nl2sql_engine = Nl2SqlEngine(config, database)
    await ctx.set("nl2sql_engine", nl2sql_engine)
    return "NL2SQL engine initialized."


async def get_data_from_db(ctx: Context, user_query: str):
    """This function returns the data from the database based on the user query"""
    charts_metadata = list(await ctx.get("charts_metadata"))
    template_name = charts_metadata[-1].chart_name
    query_message = create_query_message(user_query, template_name)
    nl2sql_engine = await ctx.get("nl2sql_engine")
    query_result = nl2sql_engine.query(query_message)
    await ctx.set("query_result", query_result)
    return f"Data retrieved successfully from the database."


async def format_the_data_according_to_chart(ctx: Context) -> str:
    """Formats the data according to the chart."""
    query_result = await ctx.get("query_result")
    charts_metadata = list(await ctx.get("charts_metadata"))
    template_name = charts_metadata[-1].chart_name
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
    """retrieves the formatted data from the context."""
    formatted_data = await ctx.get("formatted_data")
    return f"This is the formatted data: {formatted_data}"
