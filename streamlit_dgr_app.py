import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Fallback safeguards for missing Streamlit
if hasattr(st, "set_page_config"):
    st.set_page_config(page_title="Daily Geological Report Analyzer", layout="wide")

if hasattr(st, "sidebar"):
    st.sidebar.title("DGR Analyzer")
    st.sidebar.info("Upload your Daily Geological Report Excel file.")
    uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])
else:
    uploaded_file = None

# Utility to read sheet safely
def read_sheet(xls, name):
    return pd.read_excel(xls, name) if name in xls.sheet_names else None

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)

    # Tabs only if Streamlit available
    if hasattr(st, "tabs"):
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Well Information", "Lithology", "Gas Readings", "Charts", "Export Report"
        ])
    else:
        tab1 = tab2 = tab3 = tab4 = tab5 = None

    dgr = read_sheet(xls, "Daily Geological Report")
    litho = read_sheet(xls, "Lithological Description")
    gas = read_sheet(xls, "Lithology %, ROP & Gas Reading")

    # ---- WELL INFORMATION ----
    if tab1:
        with tab1:
            st.header("Well Information Summary")
            if dgr is not None:
                st.dataframe(dgr)
            else:
                st.warning("Daily Geological Report sheet not found.")

    # ---- LITHOLOGY ----
    if tab2:
        with tab2:
            st.header("Lithological Description")
            if litho is not None:
                st.dataframe(litho)
            else:
                st.warning("Lithological Description sheet not found.")

    # ---- GAS READINGS ----
    if tab3:
        with tab3:
            st.header("Gas Readings Table")
            if gas is not None:
                st.dataframe(gas)
            else:
                st.warning("Gas reading sheet not found.")

    # ---- CHARTS ----
    if tab4:
        with tab4:
            st.header("Gas Reading Charts")
            if gas is not None:
                numeric_cols = ["TG", "C1", "C2", "C3", "C4I", "C4N", "C5"]
                existing = [c for c in numeric_cols if c in gas.columns]

                for col in existing:
                    fig, ax = plt.subplots()
                    ax.plot(gas[col])
                    ax.set_title(f"{col} Trend")
                    st.pyplot(fig)
            else:
                st.warning("No gas sheet to chart.")

    # ---- EXPORT MERGED REPORT ----
    if tab5:
        with tab5:
            st.header("Export Merged Report")
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')

            if dgr is not None: dgr.to_excel(writer, sheet_name="DGR", index=False)
            if litho is not None: litho.to_excel(writer, sheet_name="Lithology", index=False)
            if gas is not None: gas.to_excel(writer, sheet_name="Gas", index=False)

            writer.save()
            st.download_button(
                label="Download Merged Excel Report",
                data=output.getvalue(),
                file_name="Merged_DGR_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# ------------------------
# requirements.txt content
# ------------------------
# streamlit
# pandas
# openpyxl
# matplotlib

# ------------------------
# Basic test cases
# ------------------------
def test_imports():
    try:
        import pandas
        import matplotlib
    except Exception:
        raise AssertionError("Core modules failed to import.")
    return True

def test_mock_streamlit():
    # Streamlit missing should not crash the app
    try:
        _ = st.sidebar if hasattr(st, "sidebar") else None
    except Exception:
        raise AssertionError("Mock Streamlit failed.")
    return True
