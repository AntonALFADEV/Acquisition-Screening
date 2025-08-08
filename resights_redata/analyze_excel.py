import pandas as pd
import plotly.express as px

def analyze_excel(file):
    # Læs faner
    df_stam = pd.read_excel(file, sheet_name="Stamdata")
    df_enh = pd.read_excel(file, sheet_name="Enheder")

    # Vælg relevante kolonner
    df_stam = df_stam[["Handels-ID", "Handelsdato", "Pris pr. m2 (enhedsareal)"]]
    df_enh = df_enh[["Handels-ID", "Antal værelser", "Areal (enhed)"]]

    # Merge og rens
    df = pd.merge(df_stam, df_enh, on="Handels-ID", how="left")
    df = df.dropna(subset=["Handelsdato", "Pris pr. m2 (enhedsareal)", "Antal værelser", "Areal (enhed)"])
    df["Handelsdato"] = pd.to_datetime(df["Handelsdato"])
    df["Antal værelser"] = df["Antal værelser"].astype(str)
    df["År"] = df["Handelsdato"].dt.year

    # Plot med trendlinje
    fig = px.scatter(
        df,
        x="Handelsdato",
        y="Pris pr. m2 (enhedsareal)",
        color="Antal værelser",
        title="Pris pr. m² over tid – farvet efter antal værelser",
        labels={"Pris pr. m2 (enhedsareal)": "Pris pr. m²"},
        hover_data=["Areal (enhed)"],
        trendline="lowess",
        trendline_options=dict(frac=0.3)
    )

    # Gennemsnit (samlet)
    total_avg = df["Pris pr. m2 (enhedsareal)"].mean()

    # Gennemsnit pr. antal værelser
    avg_by_rooms = df.groupby("Antal værelser")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

    # Gruppér efter størrelses-segment
    bins = [0, 50, 75, 100, float("inf")]
    labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
    df["Størrelsessegment"] = pd.cut(df["Areal (enhed)"], bins=bins, labels=labels)

    avg_by_size = df.groupby("Størrelsessegment")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

    # Årlige gennemsnit
    avg_by_year = df.groupby("År")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

    return fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year
