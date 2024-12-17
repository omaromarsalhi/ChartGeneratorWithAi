from llama_index.core.workflow import Context

from fastApi.data_agent.ChartMetaData import ChartMetaData

from fastApi.templates.ChartsDescriptions import (
    lineWithDataChart,
    basicRadialBarChart,
    splineAreaChart,
    donutChart,
    barChart,
    lineColumAreaChar,
    simplePieChart,
    basicColumChart,
    dashedLineChart,
    columnLabelChart
)
from fastApi.utils.utils import semantic_comparison, clean_chat_history


async def save_the_chosen_template(ctx: Context, template_name: str, user_query: str) -> str:
    """Adds the template_name to the user state."""

    charts_metadata = await ctx.get("charts_metadata",default=[])

    for chart_metadata in charts_metadata:
        if semantic_comparison(chart_metadata.user_query, user_query, await ctx.get("config")):
            return "Chart already exists."

    chart_metadata = ChartMetaData(template_name, user_query, None, False)
    charts_metadata += [chart_metadata]

    await ctx.set("charts_metadata", charts_metadata)

    chat_history = await ctx.get("chat_history")
    chat_history = clean_chat_history(chat_history, template_name)
    await ctx.set("chat_history", chat_history)

    return f"template_name {template_name} recorded in context."

async def get_template_names_and_description(ctx: Context):
    """this function gives the charts types with their description and names"""
    return [
        {
            "name": "lineWithDataChart",
            "description": lineWithDataChart
        },
        {
            "name": "basicColumChart",
            "description": basicColumChart
        },
        {
            "name": "dashedLineChart",
            "description": dashedLineChart
        },
        {
            "name": "columnLabelChart",
            "description": columnLabelChart
        },
        {
            "name": "barChart",
            "description": barChart
        },
        {
            "name": "lineColumAreaChar",
            "description": lineColumAreaChar
        },
        {
            "name": "simplePieChart",
            "description": simplePieChart
        },
        {
            "name": "splineAreaChart",
            "description": splineAreaChart
        },
        {
            "name": "donutChart",
            "description": donutChart
        },
        {
            "name": "basicRadialBarChart",
            "description": basicRadialBarChart
        }
    ]
