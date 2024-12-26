
class ChartMetaData:
    def __init__(self,chart_name,user_query, chart_data,chat_history):
        self.chart_name = chart_name
        self.chart_data = chart_data
        self.user_query = user_query
        self.chat_history = chat_history