import pandas as pd
import plotly.express as px

def analyze_excel(file):
    # Find arknavne i filen
    xls = pd.ExcelFile(file)
    sheet_names = [s.lower() for s in xls.sheet_names]

    # -------------------------
    # CASE 1: RESIGHTS-DATA
    # -------------------------
    if "stamdata" in sheet_names and "enheder" in sheet_names:
        df_stam = pd.read_excel(xls, sheet_name=[s for s in xls.sheet_names if s.lower() == "stamdata"][0])
        df_enh = pd.read_excel(xls, sheet_name=[s for s in xls.sheet_names if s.lower() == "enheder"][0])

        df_stam = df_stam[["Handels-ID", "Handelsdato", "Pris pr. m2 (enhedsareal)", "Enhedsareal"]]
        df_enh = df_enh[["Handels-ID", "Antal værelser"]]

        df = pd.merge(df_stam, df_enh, on="Handels-ID", how="left")
        df = df.dropna(subset=["Handelsdato", "Pris pr. m2 (enhedsareal)", "Antal værelser", "Enhedsareal"])
        df["Handelsdato"] = pd.to_datetime(df["Handelsdato"])
        df["Antal værelser"] = df["Antal værelser"].astype(str)
        df["År"] = df["Handelsdato"].dt.year

        fig = px.scatter(
            df,
            x="Handelsdato",
            y="Pris pr. m2 (enhedsareal)",
            color="Antal værelser",
            title="Pris pr. m² over tid – farvet efter antal værelser",
            labels={"Pris pr. m2 (enhedsareal)": "Pris pr. m²"},
            hover_data=["Enhedsareal"],
            trendline="lowess",
            trendline_options=dict(frac=0.3)
        )

        total_avg = df["Pris pr. m2 (enhedsareal)"].mean()
        avg_by_rooms = df.groupby("Antal værelser")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        bins = [0, 50, 75, 100, float("inf")]
        labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
        df["Størrelsessegment"] = pd.cut(df["Enhedsareal"], bins=bins, labels=labels)
        avg_by_size = df.groupby("Størrelsessegment")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        avg_by_year = df.groupby("År")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

        return df, fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year

    # -------------------------
    # CASE 2: REDATA-DATA
    # -------------------------
    elif "worksheet" in sheet_names:
        df = pd.read_excel(xls, sheet_name=[s for s in xls.sheet_names if s.lower() == "worksheet"][0])

        df = df.dropna(subset=["Areal", "Leje/m2", "Antal værelser", "Opførelsesår"])
        df["Antal værelser"] = df["Antal værelser"].astype(str)
        df["Opførelsesår"] = df["Opførelsesår"].astype(int)

        fig = px.scatter(
            df,
            x="Areal",
            y="Leje/m2",
            color="Antal værelser",
            title="Leje pr. m² vs Areal – farvet efter antal værelser",
            labels={"Leje/m2": "Leje pr. m²"},
            hover_data=["Opførelsesår"],
            trendline="lowess",
            trendline_options=dict(frac=0.3)
        )

        total_avg = df["Leje/m2"].mean()
        avg_by_rooms = df.groupby("Antal værelser")["Leje/m2"].mean().reset_index()

        bins = [0, 50, 75, 100, float("inf")]
        labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
        df["Størrelsessegment"] = pd.cut(df["Areal"], bins=bins, labels=labels)
        avg_by_size = df.groupby("Størrelsessegment")["Leje/m2"].mean().reset_index()

        avg_by_year = df.groupby("Opførelsesår")["Leje/m2"].mean().reset_index()

        return df, fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year

    else:
        raise ValueError("Ukendt filformat – ingen gyldige ark fundet.")
