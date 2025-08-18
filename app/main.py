import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from resights_redata.analyze_excel import analyze_excel
from resights_redata.analyze_redata import analyze_redata

st.set_page_config(page_title="Acquisition Screening App", layout="wide")
st.title("Acquisition Screening App")

# ----------------------------
# Sidebar menu med knapper
# ----------------------------
st.sidebar.title("Moduler")

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "🏠 Ejerboligpriser"

if st.sidebar.button("🏠 Ejerboligpriser"):
    st.session_state.selected_module = "🏠 Ejerboligpriser"

if st.sidebar.button("🏢 Lejeboligpriser"):
    st.session_state.selected_module = "🏢 Lejeboligpriser"

if st.sidebar.button("🧐 AI-analyse af lokalplan / kommuneplan"):
    st.session_state.selected_module = "🧐 AI-analyse af lokalplan / kommuneplan"

module = st.session_state.selected_module

# ----------------------------
# MODUL 1: RESIGHTS – Ejerboligpriser
# ----------------------------
if module == "🏠 Ejerboligpriser":
    st.header("🏠 Analyse af ejerboligpriser")
    st.write("Upload Excel-filer fra Resights – ejerboliger i fast format.")

    uploaded_file = st.file_uploader("Upload Excel-fil", type=["xlsx"], key="ejerboliger")

    if uploaded_file:
        try:
            st.success("Fil uploadet – analyserer...")
            df_full, fig_base, total_avg, avg_by_rooms, avg_by_size, avg_by_year = analyze_excel(uploaded_file)

            available_years = sorted(df_full["År"].dropna().unique())
            selected_years = st.multiselect("Vælg år", options=available_years, default=available_years)

            if selected_years:
                df = df_full[df_full["År"].isin(selected_years)]

                import plotly.express as px
                fig = px.scatter(
                    df,
                    x="Handelsdato_numeric",  # brug den numeriske dato der laves i analyze_excel
                    y="Pris pr. m2 (enhedsareal)",
                    color="Antal værelser",
                    title="Pris pr. m² over tid – farvet efter antal værelser",
                    labels={"Pris pr. m2 (enhedsareal)": "Pris pr. m²"},
                    hover_data={"Handelsdato": True, "Enhedsareal": True, "Handelsdato_numeric": False},
                    trendline="ols"
                )
                # Vis “rigtig” aksetekst
                fig.update_layout(xaxis_title="Handelsdato")
                st.plotly_chart(fig, use_container_width=True)

                # 👉 Antal observationer (punkter i plottet)
                st.metric("Antal observationer", f"{len(df)}")

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
# MODUL 2: REDATA – Lejeboligpriser
# ----------------------------
elif module == "🏢 Lejeboligpriser":
    st.header("🏢 Analyse af lejeboligpriser")
    st.write("Upload Excel-filer fra ReData – lejeboliger i fast format.")

    uploaded_file = st.file_uploader("Upload ReData Excel-fil", type=["xlsx"], key="redata")

    if uploaded_file:
        try:
            st.success("Fil uploadet – analyserer...")
            df, fig, total_avg, avg_by_rooms, avg_by_size, avg_by_year = analyze_redata(uploaded_file)

            if df is not None:
                st.plotly_chart(fig, use_container_width=True)

                # 👉 Antal observationer (punkter i plottet)
                st.metric("Antal observationer", f"{len(df)}")

                st.subheader("📊 Statistik")
                st.metric("Gennemsnitlig leje pr. m²", f"{total_avg:,.0f} kr.")

                st.markdown("**Gennemsnit pr. antal værelser:**")
                st.dataframe(avg_by_rooms, use_container_width=True)

                st.markdown("**Gennemsnit pr. størrelsessegment:**")
                st.dataframe(avg_by_size, use_container_width=True)

                st.markdown("**Gennemsnit pr. opførelsesår:**")
                st.dataframe(avg_by_year, use_container_width=True)
        except Exception as e:
            st.error(f"Fejl under ReData-analyse: {e}")

# ----------------------------
# MODUL 3: PDF-AI
# ----------------------------
elif module == "🧐 AI-analyse af lokalplan / kommuneplan":
    st.header("🧐 Upload PDF for AI-analyse")
    st.write("Upload en kommuneplan eller lokalplan i PDF-format og få en AI-opsummering.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], key="pdf")

    if uploaded_pdf:
        try:
            from planning_ai.summarize_plans import summarize_pdf
            st.success("PDF uploadet – analyserer...")
            summary = summarize_pdf(uploaded_pdf)
            st.markdown("### 🔎 AI-opsummering")
            st.write(summary)
        except Exception as e:
            st.error(f"Fejl under PDF-analyse: {e}")
