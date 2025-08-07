import pandas as pd

def analyze_excel(file):
    # Enkel preview af uploadet Excel-fil
    df = pd.read_excel(file)
    return df.head(50)  # viser de første 50 rækker