import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from scraping.boligportal_scraper import fetch_boligportal

st.set_page_config(page_title="Acquisition Screening App", layout="wide")
st.title("Acquisition Screening App")

# ----------------------------
# Sidebar menu med knapper
# ----------------------------
st.sidebar.title("Moduler")

# Gem valgt modul i session state
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
    st.header("📈 Analyse af Excel-data")
    st.write("Upload Excel-filer fra Resights eller ReData.")

    uploaded_file = st.file_uploader("Upload Excel-fil", type=["xlsx"])

    if uploaded_file:
        try:
            from resights_redata.analyze_excel import analyze_excel
            st.success("Fil uploadet – analyserer...")
            df = analyze_excel(uploaded_file)
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("Ingen data fundet i filen.")
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

