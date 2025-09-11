import pandas as pd

def load_college_data(filepath="data/college_data.xlsx"):
    df = pd.read_excel(filepath)
    return df.to_dict(orient='records')
