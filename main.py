import streamlit as st

# Opsætning af app
st.set_page_config(page_title="Acquisition Screening App", layout="wide")
st.title("🏗️ Acquisition Screening App")

# Navigation
st.sidebar.title("Moduler")
module = st.sidebar.selectbox("Vælg modul", [
    "📦 Boligdata scraping", 
    "📈 Excel-analyse (Resights / ReData)", 
    "🧠 AI-analyse af lokalplan / kommuneplan"
])

# =======================
# 📦 MODUL 1: SCRAPING
# =======================
if module == "📦 Boligdata scraping":
    st.header("📦 Scraping af boligdata")
    st.write("Hent boligdata fra fx lejebolig.dk – flere portaler kommer snart.")

    postnr = st.text_input("Indtast postnummer", value="2300")

    if st.button("Start scraping (lejebolig.dk)"):
        from scraping.lejebolig_scraper import fetch_lejeboliger
        with st.spinner("Henter data..."):
            df = fetch_lejeboliger(postnr)
            st.success(f"{len(df)} boliger hentet for postnummer {postnr}")
            st.dataframe(df)

# =======================
# 📈 MODUL 2: EXCEL-ANALYSE
# =======================
elif module == "📈 Excel-analyse (Resights / ReData)":
    st.header("📈 Analyse af Excel-data")
    st.write("Upload Excel-filer fra Resights eller ReData.")

    uploaded_file = st.file_uploader("Upload Excel-fil", type=["xlsx"])

    if uploaded_file:
        from resights_redata.analyze_excel import analyze_excel
        st.success("Fil uploadet – analyserer...")
        df = analyze_excel(uploaded_file)
        st.dataframe(df)

# =======================
# 🧠 MODUL 3: PDF-AI
# =======================
elif module == "🧠 AI-analyse af lokalplan / kommuneplan":
    st.header("🧠 Upload PDF for AI-analyse")
    st.write("Upload en kommuneplan eller lokalplan i PDF-format og få en AI-opsummering.")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        from planning_ai.summarize_plans import summarize_pdf
        st.success("PDF uploadet – analyserer...")
        summary = summarize_pdf(uploaded_pdf)
        st.markdown("### 🔎 AI-opsummering")
        st.write(summary)