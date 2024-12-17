from llama_index.core import PromptTemplate

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

