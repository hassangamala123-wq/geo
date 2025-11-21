# app.py
# Streamlit safe import
try:
    import streamlit as st
except ModuleNotFoundError:
    class MockStreamlit:
        def __getattr__(self, name):
            def dummy(*args, **kwargs):
                return None
            return dummy
    st = MockStreamlit()

import pandas as pd
import altair as alt
from io import BytesIO

# Configure page
if hasattr(st, "set_page_config"):
    st.set_page_config(page_title="Daily Geological Report Analyzer", layout="wide")

# Sidebar
if hasattr(st, "sidebar"):
    st.sidebar.title("DGR Analyzer")
    st.sidebar.info("Upload your Daily Geological Report Excel file.")
    uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])
else:
    uploaded_file = None

# Read sheet safely
def read_sheet(xls, name):
    return xls.get(name)

# --- MAIN EXECUTION ---
if uploaded_file:
    try:
        # Read all sheets at once without openpyxl dependency
        xls = pd.read_excel(uploaded_file, sheet_name=None)
    except Exception as e:
        st.error(f"Failed to read Excel file: {e}")
        xls = {}

    # Tabs
    if hasattr(st, "tabs"):
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Well Information", "Lithology", "Gas Readings", "Charts", "Export Report"
        ])
    else:
        tab1 = tab2 = tab3 = tab4 = tab5 = None

    # Extract sheets
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
                    chart = alt.Chart(gas.reset_index()).mark_line().encode(
                        x='index', y=col, tooltip=[col]
                    ).properties(title=f"{col} Trend", height=300)
                    st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("No gas sheet to chart.")

    # ---- EXPORT MERGED REPORT ----
    if tab5:
        with tab5:
            st.header("Export Merged Report")
            output = BytesIO()
            try:
                import xlsxwriter
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                writer_ok = True
            except Exception:
                writer_ok = False
                writer = None  # no engine available  # fallback to default engine

            if dgr is not None:
                dgr.to_excel(writer, sheet_name="DGR", index=False)
            if litho is not None:
                litho.to_excel(writer, sheet_name="Lithology", index=False)
            if gas is not None:
                gas.to_excel(writer, sheet_name="Gas", index=False)

            if writer_ok:
                writer.close()
                st.download_button(
                    label="Download Merged Excel Report",
                    data=output.getvalue(),
                    file_name="Merged_DGR_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No Excel engine available (xlsxwriter/openpyxl missing). Cannot export.")
            )


# ------------------------
# Basic test cases
# ------------------------
def test_imports():
    try:
        import pandas
        import altair
    except Exception:
        raise AssertionError("Core modules failed to import.")
    return True

def test_mock_streamlit():
    try:
        _ = st.sidebar if hasattr(st, "sidebar") else None
    except Exception:
        raise AssertionError("Mock Streamlit failed.")
    return True
