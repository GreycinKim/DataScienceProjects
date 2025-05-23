import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shipment Organizer", layout="wide")
st.title("📦 ShipStation + FedEx CSV Organizer")

# Upload section
st.sidebar.header("Upload CSVs")
shipstation_file = st.sidebar.file_uploader("Upload ShipStation CSV", type="csv")
invoice_file = st.sidebar.file_uploader("Upload FedEx Invoice CSV", type="csv")

# Helper: fuzzy match column names
def find_column(columns, target_keywords):
    for col in columns:
        for keyword in target_keywords:
            if keyword.lower() in col.lower():
                return col
    return None

# Start after upload
if shipstation_file and invoice_file:
    st.success("Both files uploaded successfully!")

    # Read CSVs
    df_ship = pd.read_csv(shipstation_file)
    df_invoice = pd.read_csv(invoice_file)

    # Preview raw columns
    st.write("📄 ShipStation Columns:", list(df_ship.columns))
    st.write("📄 FedEx Invoice Columns:", list(df_invoice.columns))

    # Display previews
    st.subheader("📄 ShipStation Preview")
    st.dataframe(df_ship.head(10), use_container_width=True)

    st.subheader("📄 FedEx Invoice Preview")
    st.dataframe(df_invoice.head(10), use_container_width=True)

    # Auto-detect tracking columns
    tracking_col_ship = find_column(df_ship.columns, ["Tracking", "Tracking #"])
    tracking_col_invoice = find_column(df_invoice.columns, ["Tracking ID", "Express or Ground Tracking ID", "Tracking"])

    if tracking_col_ship and tracking_col_invoice:
        # Normalize tracking numbers (remove spaces, fix scientific notation)
        df_ship[tracking_col_ship] = df_ship[tracking_col_ship].apply(
            lambda x: str(int(float(x))) if isinstance(x, str) and 'E+' in x else str(x)
        ).str.strip()

        df_invoice[tracking_col_invoice] = df_invoice[tracking_col_invoice].astype(str).str.strip()

        # Merge
        merged_df = pd.merge(
            df_ship,
            df_invoice,
            how="left",
            left_on=tracking_col_ship,
            right_on=tracking_col_invoice
        )

        st.subheader("🔗 Merged Data (Based on Tracking Number)")
        st.dataframe(merged_df.head(25), use_container_width=True)

        # Filters
        with st.expander("🔍 Filter Options"):
            recipient = st.text_input("Filter by Recipient (partial match)", "")
            service_col = find_column(df_ship.columns, ["Service"])
            service_list = sorted(df_ship[service_col].dropna().unique().tolist()) if service_col else []
            service = st.selectbox("Filter by Service", ["All"] + service_list)
            date_col = find_column(df_ship.columns, ["Ship Date", "Date"])
            date = st.text_input("Filter by Ship Date (MM/DD/YY)", "")

            filtered_df = merged_df.copy()

            if recipient and "Recipient" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["Recipient"].str.contains(recipient, case=False, na=False)]
            if service != "All" and service_col:
                filtered_df = filtered_df[filtered_df[service_col] == service]
            if date and date_col:
                filtered_df = filtered_df[filtered_df[date_col] == date]

            st.write(f"Showing {len(filtered_df)} filtered rows")
            st.dataframe(filtered_df, use_container_width=True)

        # Download
        st.download_button(
            "📥 Download Filtered Data as CSV",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_shipments.csv",
            mime="text/csv"
        )

    else:
        st.error("❌ Could not find required tracking columns in one or both files.")
        st.write("ShipStation Columns:", list(df_ship.columns))
        st.write("FedEx Invoice Columns:", list(df_invoice.columns))
else:
    st.warning("Please upload both CSV files to begin.")
