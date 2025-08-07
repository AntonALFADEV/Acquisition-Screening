import streamlit as st

st.set_page_config(page_title="Acquisition Screening App", layout="wide")

st.title("🏗️ Acquisition Screening App")

# Sidebar navigation
st.sidebar.title("Moduler")
module = st.sidebar.selectbox("Vælg modul", ["📦 Boligdata scraping", "📈 Excel-analyse", "🧠 Lokalplan AI"])

if module == "📦 Boligdata scraping":
    st.header("Scraping af boligdata")
    st.write("Her kan du hente leje- og salgsdata fra forskellige boligportaler.")

    postnr = st.text_input("Indtast postnummer", value="2300")

    if st.button("Start scraping (lejebolig.dk)"):
        from scraping.lejebolig_scraper import fetch_lejeboliger

        with st.spinner("Henter data..."):
            df = fetch_lejeboliger(postnr)
            st.success("Data hentet!")
            st.dataframe(df)

elif module == "📈 Excel-analyse":
    st.header("Upload og analyse af Excel-filer")
    st.write("Analyser Excel-data fra Resights og ReData.")

elif module == "🧠 Lokalplan AI":
    st.header("Upload PDF og få AI-analyse")
    st.write("Upload kommune- eller lokalplaner som PDF.")