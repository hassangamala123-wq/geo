import streamlit as st
import pandas as pd

st.title("Daily Geological Report Analyzer")

uploaded_file = st.file_uploader("Upload Daily Geological Report (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        st.success("File uploaded successfully")

        # Load sheets if they exist
        sheets = xls.sheet_names

        # --- DAILY GEOLOGICAL REPORT SHEET ---
        dgr_df = None
        if "Daily Geological Report" in sheets:
            dgr_df = pd.read_excel(xls, "Daily Geological Report")
            st.subheader("Well Information")
            st.dataframe(dgr_df.head())
        else:
            st.warning("Sheet 'Daily Geological Report' not found.")

        # --- LITHOLOGICAL DESCRIPTION ---
        litho_desc_df = None
        if "Lithological Description" in sheets:
            litho_desc_df = pd.read_excel(xls, "Lithological Description")
            st.subheader("Lithological Description")
            st.dataframe(litho_desc_df.head())
        else:
            st.warning("Sheet 'Lithological Description' not found.")

        # --- GAS READINGS SHEET ---
        gas_df = None
        if "Lithology %, ROP & Gas Reading" in sheets:
            gas_df = pd.read_excel(xls, "Lithology %, ROP & Gas Reading")
            st.subheader("Gas Readings")
            st.dataframe(gas_df.head())
        else:
            st.warning("Sheet 'Lithology %, ROP & Gas Reading' not found.")

        # --- MERGED REPORT PREVIEW ---
        st.header("Merged Report Summary")
        summary = {}

        # Extract well info (example assumes key-value layout)
        if dgr_df is not None:
            try:
                info = dgr_df.set_index(dgr_df.columns[0])[dgr_df.columns[1]].to_dict()
                summary.update(info)
            except:
                pass

        st.json(summary)

        # Extract drilling progress
        if dgr_df is not None:
            st.subheader("Drilling Progress Summary")
            dp_cols = [
                "24:00 Hrs Depth", "00:00 Hrs Depth", "06:00 Hrs Depth",
                "Progress (Last 24H)", "Progress (Last 6H)"
            ]
            for col in dp_cols:
                if col in dgr_df.columns:
                    st.write(f"**{col}:** {dgr_df[col].iloc[0]}")

        # Formation tops
        if dgr_df is not None:
            st.subheader("Formation Tops (Actual vs Prognosis)")
            ft_cols = [c for c in dgr_df.columns if "Formation Top" in c]
            if ft_cols:
                st.dataframe(dgr_df[ft_cols])

        # Gas summary
        if gas_df is not None:
            st.subheader("Gas Summary (TG, C1, C2, C3, C4I, C4N, C5)")
            gas_cols = ["TG", "C1", "C2", "C3", "C4I", "C4N", "C5"]
            existing = [g for g in gas_cols if g in gas_df.columns]
            if existing:
                st.dataframe(gas_df[existing])

    except Exception as e:
        st.error(f"Error reading file: {e}")
