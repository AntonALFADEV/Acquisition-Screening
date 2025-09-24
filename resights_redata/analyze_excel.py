import pandas as pd
import plotly.express as px

def analyze_excel(file):
    # Læs arket "Stamdata" og "Enheder"
    xls = pd.ExcelFile(file)
    sheet_names = [s.lower() for s in xls.sheet_names]

    if "stamdata" in sheet_names and "enheder" in sheet_names:
        df_stam = pd.read_excel(
            xls, sheet_name=[s for s in xls.sheet_names if s.lower() == "stamdata"][0]
        )
        df_enh = pd.read_excel(
            xls, sheet_name=[s for s in xls.sheet_names if s.lower() == "enheder"][0]
        )

        df_stam = df_stam[["Handels-ID", "Handelsdato", "Pris pr. m2 (enhedsareal)", "Enhedsareal"]]
        df_enh = df_enh[["Handels-ID", "Antal værelser"]]

        df = pd.merge(df_stam, df_enh, on="Handels-ID", how="left")
        df = df.dropna(subset=["Handelsdato", "Pris pr. m2 (enhedsareal)", "Antal værelser", "Enhedsareal"])
        df["Handelsdato"] = pd.to_datetime(df["Handelsdato"])
        df["Antal værelser"] = df["Antal værelser"].astype(str)
        df["År"] = df["Handelsdato"].dt.year

        # Scatterplot med dato direkte på x-aksen
        fig = px.scatter(
            df,
            x="Handelsdato",
            y="Pris pr. m2 (enhedsareal)",
            color="Antal værelser",
            title="Pris pr. m² over tid – farvet efter antal værelser",
            labels={"Pris pr. m2 (enhedsareal)": "Pris pr. m²"},
            hover_data={"Handelsdato": True, "Enhedsareal": True},
            trendline="ols",  # Plotly kan stadig lave regression på datotid
        )

        fig.update_layout(xaxis_title="Handelsdato")

        # Beregninger
        total_avg = df["Pris pr. m2 (enhedsareal)"].mean()
        avg_by_rooms = df.groupby("Antal værelser")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        bins = [0, 50, 75, 100, float("inf")]
        labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
        df["Størrelsessegment"] = pd.cut(df["Enhedsareal"], bins=bins, labels=labels)
        avg_by_size = df.groupby("Størrelsessegment")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        avg_by_year = df.groupby("År")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        return df, fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year

    else:
        raise ValueError("Excel-arket ser ikke ud til at komme fra Resights (mangler 'Stamdata' og 'Enheder').")
