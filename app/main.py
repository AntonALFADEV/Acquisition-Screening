import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from scraping.boligportal_scraper import fetch_boligportal
from resights_redata.analyze_excel import analyze_excel

st.set_page_config(page_title="Acquisition Screening App", layout="wide")
st.title("Acquisition Screening App")

# ----------------------------
# Sidebar menu med knapper
# ----------------------------
st.sidebar.title("Moduler")

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "📦 Boligdata scraping"

if st.sidebar.button("📦 Boligdata scraping"):
    st.session_state.selected_module = "📦 Boligdata scraping"

if st.sidebar.button("📈 Excel-analyse (Resights / ReData)"):
    st.session_state.selected_module = "📈 Excel-analyse (Resights / ReData)"

if st.sidebar.button("🧠 AI-analyse af lokalplan / kommuneplan"):
    st.session_state.selected_module = "🧠 AI-analyse af lokalplan / kommuneplan"

module = st.session_state.selected_module

# ----------------------------
# MODUL 1: SCRAPING
# ----------------------------
if module == "📦 Boligdata scraping":
    st.header("📦 Scraping af boligdata")
    st.write("Hent boligdata fra Boligportal baseret på postnummer.")
    postnr = st.text_input("Indtast postnummer", value="2300")

    if st.button("Start scraping (boligportal.dk)"):
        try:
            with st.spinner("Henter data..."):
                df = fetch_boligportal(postnr)
                if not df.empty:
                    st.success(f"{len(df)} boliger hentet fra Boligportal for postnummer {postnr}")
                    st.dataframe(df)
                else:
                    st.warning("Ingen resultater fundet.")
        except Exception as e:
            st.error(f"Fejl under scraping: {e}")

# ----------------------------
# MODUL 2: EXCEL-ANALYSE
# ----------------------------
elif module == "📈 Excel-analyse (Resights / ReData)":
    st.header("📈 Analyse af Resights / ReData Excel-data")
    st.write("Upload Excel-filer fra Resights – ejerboliger i fast format.")

    uploaded_file = st.file_uploader("Upload Excel-fil", type=["xlsx"])

    if uploaded_file:
        try:
            st.success("Fil uploadet – analyserer...")
            df_full, fig_base, total_avg, avg_by_rooms, avg_by_size, avg_by_year = analyze_excel(uploaded_file)

            # Filtrér år
            available_years = sorted(df_full["År"].dropna().unique())
            selected_years = st.multiselect("Vælg år", options=available_years, default=available_years)

            if selected_years:
                df = df_full[df_full["År"].isin(selected_years)]

                # Opdater fig med filtreret data
                import plotly.express as px
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
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📊 Statistik")
                st.metric("Gennemsnitlig pris pr. m² (alle boliger)", f"{df['Pris pr. m2 (enhedsareal)'].mean():,.0f} kr.")

                st.markdown("**Gennemsnit pr. antal værelser:**")
                st.dataframe(df.groupby("Antal værelser")["Pris pr. m2 (enhedsareal)"].mean().reset_index(), use_container_width=True)

                bins = [0, 50, 75, 100, float("inf")]
                labels = ["0–50 m²", "51–75 m²", "76–100 m²", "100+ m²"]
                df["Størrelsessegment"] = pd.cut(df["Enhedsareal"], bins=bins, labels=labels)
                avg_by_size = df.groupby("Størrelsessegment")["Pris pr. m2 (enhedsareal)"].mean().reset_index()

                st.markdown("**Gennemsnit pr. størrelsessegment:**")
                st.dataframe(avg_by_size, use_container_width=True)

                avg_by_year = df.groupby("År")["Pris pr. m2 (enhedsareal)"].mean().reset_index()
                st.markdown("**Årlige gennemsnitspriser (filtreret):**")
                st.dataframe(avg_by_year, use_container_width=True)
            else:
                st.warning("Vælg mindst ét år for at se analyserne.")
        except Exception as e:
            st.error(f"Fejl under Excel-analyse: {e}")

# ----------------------------
# MODUL 3: PDF-AI
# ----------------------------
elif module == "🧠 AI-analyse af lokalplan / kommuneplan":
    st.header("🧠 Upload PDF for AI-analyse")
    st.write("Upload en kommuneplan eller lokalplan i PDF-format og få en AI-opsummering.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        try:
            from planning_ai.summarize_plans import summarize_pdf
            st.success("PDF uploadet – analyserer...")
            summary = summarize_pdf(uploaded_pdf)
            st.markdown("### 🔎 AI-opsummering")
            st.write(summary)
        except Exception as e:
            st.error(f"Fejl under PDF-analyse: {e}")

