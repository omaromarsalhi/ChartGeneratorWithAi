from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.workflow import Context

from fastApi.chart_history_agent.ChartMetaData import ChartMetaData
from fastApi.utils.utils import semantic_comparison
from sql_db_search.Nl2SqlApplication import Config


async def retrieve_chat_history(ctx: Context,user_query:str) -> str:
    """Retrieves the ChartMetaData along with the chart history and the formatted chart from the context if exists."""
    config=Config('../../config.ini')
    chart_metadata=await ctx.get("chart_metadata",[])
    for metadata in chart_metadata:
        if semantic_comparison(metadata.user_query,user_query,config):
            await ctx.set("template_name",metadata.chart_name)
            await ctx.set("chat_history", metadata.chat_history)
            await ctx.set("formatted_data", metadata.chart_data)
            return "history retrieved."
    return "No history found."

async def save_chat_history(ctx: Context,user_query:str,template_name:str):
    """Saves the chat history and the user query with the retrieved data to the context."""
    chart_metadata = ChartMetaData(
        chart_name=template_name,
        chart_data=await ctx.get("formatted_data"),
        user_query=user_query,
        chat_history=await ctx.get("chat_history")
    )
    saved_metadata= await ctx.get("chart_metadata",[])
    saved_metadata.append(chart_metadata)
    await ctx.set("chart_metadata",saved_metadata)
    return "ChartMetaData saved."

async def clean_chat_history(ctx: Context):
    """Cleans the chat history."""
    chat_history=await ctx.get("chat_history")
    chat_history = [chat_history[-2]]+[chat_history[-1]]
    await ctx.set("chat_history", chat_history)
    await ctx.set("template_name", None)
    await ctx.set("formatted_data", None)
    return "Chat history cleaned."


