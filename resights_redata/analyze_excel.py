import pandas as pd
import plotly.express as px

def analyze_excel(file):
    # Læs data
    df_stam = pd.read_excel(file, sheet_name="Stamdata")
    df_enh = pd.read_excel(file, sheet_name="Enheder")

    # Vælg relevante kolonner
    df_stam = df_stam[["Handels-ID", "Handelsdato", "Pris pr. m2 (enhedsareal)", "Enhedsareal"]]
    df_enh = df_enh[["Handels-ID", "Antal værelser"]]

    # Merge
    df = pd.merge(df_stam, df_enh, on="Handels-ID", how="left")
    df = df.dropna(subset=["Handelsdato", "Pris pr. m2 (enhedsareal)", "Antal værelser", "Enhedsareal"])
    df["Handelsdato"] = pd.to_datetime(df["Handelsdato"])
    df["Antal værelser"] = df["Antal værelser"].astype(str)
    df["År"] = df["Handelsdato"].dt.year

    # Returnér hele datasættet – analyserne laves i main.py
    return df
