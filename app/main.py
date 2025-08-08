elif module == "📈 Excel-analyse (Resights / ReData)":
    st.header("📈 Analyse af Resights / ReData Excel-data")
    st.write("Upload Excel-filer fra Resights – ejerboliger i fast format.")

    uploaded_file = st.file_uploader("Upload Excel-fil", type=["xlsx"])

    if uploaded_file:
        try:
            from resights_redata.analyze_excel import analyze_excel

            st.success("Fil uploadet – analyserer...")
            df_full = analyze_excel(uploaded_file)

            # 🎯 Filtrér på år
            available_years = sorted(df_full["År"].dropna().unique())
            selected_years = st.multiselect("Vælg år der skal med i analysen", options=available_years, default=available_years)

            if selected_years:
                df = df_full[df_full["År"].isin(selected_years)]

                # 📊 Plot med filtreret data
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

                # 📈 Statistik
                st.subheader("📊 Statistik")

                total_avg = df["Pris pr. m2 (enhedsareal)"].mean()
                st.metric("Gennemsnitlig pris pr. m² (alle boliger)", f"{total_avg:,.0f} kr.")

                avg_by_rooms = df.groupby("Antal værelser")["Pris pr. m2 (enhedsareal)"].mean().reset_index()
                st.markdown("**Gennemsnit pr. antal værelser:**")
                st.dataframe(avg_by_rooms, use_container_width=True)

                # Segmenter efter størrelse
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

