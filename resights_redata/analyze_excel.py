import pandas as pd
import plotly.express as px

def analyze_excel(file):
    # Læs data fra begge faner
    df_stamdata = pd.read_excel(file, sheet_name="Stamdata")
    df_enheder = pd.read_excel(file, sheet_name="Enheder")

    # Vælg relevante kolonner
    df_stamdata = df_stamdata[["Handels-ID", "Handelsdato", "Pris pr. m2 (enhedsareal)"]]
    df_enheder = df_enheder[["Handels-ID", "Antal værelser"]]

    # Join på Handels-ID
    df = pd.merge(df_stamdata, df_enheder, on="Handels-ID", how="left")

    # Fjern rækker med manglende værdier
    df = df.dropna(subset=["Handelsdato", "Pris pr. m2 (enhedsareal)", "Antal værelser"])

    # Formatér data
    df["Handelsdato"] = pd.to_datetime(df["Handelsdato"])
    df["Antal værelser"] = df["Antal værelser"].astype(str)

    # Lav punktdiagram
    fig = px.scatter(
        df,
        x="Handelsdato",
        y="Pris pr. m2 (enhedsareal)",
        color="Antal værelser",
        title="Pris pr. m² over tid – farvet efter antal værelser",
        labels={
            "Handelsdato": "Handelsdato",
            "Pris pr. m2 (enhedsareal)": "Pris pr. m²",
            "Antal værelser": "Værelser"
        },
        hover_data=["Handels-ID"]
    )

    return fig
