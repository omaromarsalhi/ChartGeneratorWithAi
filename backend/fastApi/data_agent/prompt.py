from llama_index.core import PromptTemplate
from llama_index.core.prompts import PromptType

combined_prompt = (
    "You are an agent designed to interact with a SQL database and return data that fits a specific chart template. "
    "Given an input question and the chart example, create a syntactically correct MySQL query to run. "
    "Only execute the query and return the result, no explanations or descriptions. "
    "You must return only the result of the query, no other information. "
    "You are not allowed to explain or describe the SQL query itself.\n\n"
    "do not make any reduction to the result of the query. always return the full result of the query."
    
    "You can order the results by a relevant column to return the most interesting examples in the database. "
    "Never query for all the columns from a specific table; only ask for the relevant columns given the question.\n\n"

    "You must only use the information returned by the query to construct your final answer. "
    "Only use the given tools to interact with the database. "
    "You MUST double-check your query before executing it. If you get an error while executing a query, rewrite the query and try again.\n\n"

    "Here is the chart example and the question in the same string for this task:\n"

    "{schema}\n\n"
    "Question: {query_str}\n"
    "SQLQuery: "
)

# Use this combined prompt in the query engine
custom_prompt = PromptTemplate(
    combined_prompt,
    prompt_type=PromptType.TEXT_TO_SQL,
)


response_prompt = (
    "Given an input question and a chart example, synthesize a response from the query results and format the data "
    "according to the chart structure provided.\n"
    "Query: {query_str}\n"
    "SQL: {sql_query}\n"
    "SQL Response: {context_str}\n\n"
    "If the SQL query involves restricted operations (like DELETE, INSERT, UPDATE, or DROP), "
    "respond with 'Sorry, this operation is not allowed'. Otherwise, provide the result of the query in the "
    "following format based on the chart example:\n\n"
    "{chart_example}\n\n"
    "Response: "
)




response_prompt = PromptTemplate(
    response_prompt,
    prompt_type=PromptType.SQL_RESPONSE_SYNTHESIS_V2,
)

prompt = """
    You are a data visualization assistant. Your task is to:
    1. Analyze the provided dataset.
    2. Format the data to fit the specified chart example.
    3. Return the formatted chart data as a JSON object.

    ### Input:
    - **Dataset:** A raw dataset in tabular or structured text format, containing headers and corresponding rows of values.
    - **Chart Example:** A JSON template specifying the chart structure, with placeholders for labels, values, or other chart fields.

    ### Output:
    A JSON object formatted to match the chart example.

    Dataset:
    {dataset}
    Chart Example:
    {chart_example}
"""

formating_prompt = PromptTemplate(
    prompt
)



