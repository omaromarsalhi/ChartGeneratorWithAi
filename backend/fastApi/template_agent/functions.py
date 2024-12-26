from llama_index.core.workflow import Context

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
from fastApi.utils.utils import clean_chat_history


async def save_the_chosen_template(ctx: Context, template_name: str) -> str:
    """Stores the selected template name and updates the chat history."""
    await ctx.set("template_name", template_name)
    chat_history = await ctx.get("chat_history")
    chat_history = clean_chat_history(chat_history, template_name)
    await ctx.set("chat_history", chat_history)

    return f"Template {template_name} recorded."


async def get_template_names_and_description(ctx: Context):
    """Returns available chart types with their names and descriptions."""
    return [
        {"name": "lineWithDataChart", "description": lineWithDataChart},
        {"name": "basicColumChart", "description": basicColumChart},
        {"name": "dashedLineChart", "description": dashedLineChart},
        {"name": "columnLabelChart", "description": columnLabelChart},
        {"name": "barChart", "description": barChart},
        {"name": "lineColumAreaChar", "description": lineColumAreaChar},
        {"name": "simplePieChart", "description": simplePieChart},
        {"name": "splineAreaChart", "description": splineAreaChart},
        {"name": "donutChart", "description": donutChart},
        {"name": "basicRadialBarChart", "description": basicRadialBarChart}
    ]


