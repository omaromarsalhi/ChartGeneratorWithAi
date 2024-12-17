from llama_cloud import MessageRole
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.workflow import Context

from fastApi.orchestration.workflow import ProgressEvent
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





async def save_the_chosen_template(ctx: Context, template_name: str) -> str:
    """Adds the template_name to the user state."""
    ctx.write_event_to_stream(ProgressEvent(msg="Recording template_name"))
    await ctx.set("template_name", template_name)

    chat_history = await ctx.get("chat_history")
    chat_history = clean_chat_history(chat_history, template_name)
    await ctx.set("chat_history", chat_history)

    return (f"template_name {template_name} recorded in context.")


def clean_chat_history(chat_history, template_name) -> list[ChatMessage]:
    """Removes the get_template_names_and_description tool from the chat history."""
    for i, message in enumerate(chat_history):
        if message.role == MessageRole.TOOL and message.additional_kwargs[
            "name"] == "get_template_names_and_description":
            message.blocks[0].text = str(get_template_data_by_name(template_name))
    return chat_history


def get_template_data_by_name(template_name: str):
    """this function returns the template data by its name"""
    if template_name == "lineWithDataChart":
        return {
            "name": "lineWithDataChart",
            "description": lineWithDataChart
        }
    elif template_name == "basicColumChart":
        return {
            "name": "basicColumChart",
            "description": basicColumChart
        }
    elif template_name == "dashedLineChart":
        return {
            "name": "dashedLineChart",
            "description": dashedLineChart
        }
    elif template_name == "columnLabelChart":
        return {
            "name": "columnLabelChart",
            "description": columnLabelChart
        }
    elif template_name == "barChart":
        return {
            "name": "barChart",
            "description": barChart
        }
    elif template_name == "lineColumAreaChar":
        return {
            "name": "lineColumAreaChar",
            "description": lineColumAreaChar
        }
    elif template_name == "simplePieChart":
        return {
            "name": "simplePieChart",
            "description": simplePieChart
        }
    elif template_name == "splineAreaChart":
        return {
            "name": "splineAreaChart",
            "description": splineAreaChart
        }
    elif template_name == "donutChart":
        return {
            "name": "donutChart",
            "description": donutChart
        }
    elif template_name == "basicRadialBarChart":
        return {
            "name": "basicRadialBarChart",
            "description": basicRadialBarChart
        }


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
