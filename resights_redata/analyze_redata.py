import pandas as pd
import plotly.express as px

def analyze_redata(file):
    # Læs ReData-arket (typisk navngivet "Worksheet")
    xls = pd.ExcelFile(file)
    sheet_name = [s for s in xls.sheet_names if s.lower() == "worksheet"]

    if not sheet_name:
        raise ValueError("ReData-filens ark 'Worksheet' blev ikke fundet.")

    df = pd.read_excel(xls, sheet_name=sheet_name[0])

    # Drop rækker med manglende værdier
    df = df.dropna(subset=["Areal", "Leje/m2", "Antal værelser", "Opførelsesår"])
    df["Antal værelser"] = df["Antal værelser"].astype(str)
    df["Opførelsesår"] = df["Opførelsesår"].astype(int)

    # Scatterplot: Areal vs Leje/m2
    fig = px.scatter(
        df,
        x="Areal",
        y="Leje/m2",
        color="Antal værelser",
        title="Leje pr. m² vs Areal – farvet efter antal værelser",
        labels={"Leje/m2": "Leje pr. m²"},
        hover_data=["Opførelsesår"],
        trendline="ols",
    )

    # Beregninger
    total_avg = df["Leje/m2"].mean()
    avg_by_rooms = df.groupby("Antal værelser")["Leje/m2"].mean().reset_index()

    bins = [0, 50, 75, 100, float("inf")]
    labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
    df["Størrelsessegment"] = pd.cut(df["Areal"], bins=bins, labels=labels)
    avg_by_size = df.groupby("Størrelsessegment")["Leje/m2"].mean().reset_index()

    avg_by_year = df.groupby("Opførelsesår")["Leje/m2"].mean().reset_index()

    return df, fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year
