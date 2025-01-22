import pandas as pd
from io import BytesIO

def _basic_insight_excel():
    data = {"column1": [1, 2, 3], "column2": [4, 5, 6]}
    sample_data = pd.DataFrame(data)
    excel_buffer = BytesIO()
    sample_data.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return excel_buffer

def insight_file_excel():
    """insight excel file with expected possible prompt"""
    return _basic_insight_excel()