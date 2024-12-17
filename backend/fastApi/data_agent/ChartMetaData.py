
class ChartMetaData:
    def __init__(self,chart_name,user_query, chart_data,chart_state):
        self.chart_name = chart_name
        self.chart_data = chart_data
        self.chart_state = chart_state
        self.user_query = user_query