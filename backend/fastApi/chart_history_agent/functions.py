from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.workflow import Context




async def clean_chat_history(ctx: Context):
    """Cleans the chat history."""
    chat_history=await ctx.get("chat_history")
    chat_history = [chat_history[-2]]+[chat_history[-1]]
    await ctx.set("chat_history", chat_history)
    await ctx.set("template_name", None)
    return "Chat history cleaned."


