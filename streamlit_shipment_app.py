
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shipment Organizer", layout="wide")

st.title("📦 ShipStation + FedEx CSV Organizer")

# Upload section
st.sidebar.header("Upload CSVs")
shipstation_file = st.sidebar.file_uploader("Upload ShipStation CSV", type="csv")
invoice_file = st.sidebar.file_uploader("Upload FedEx Invoice CSV", type="csv")

if shipstation_file and invoice_file:
    st.success("Both files uploaded successfully!")

    # Read CSVs
    df_ship = pd.read_csv(shipstation_file)
    df_invoice = pd.read_csv(invoice_file)

    # Display previews
    st.subheader("📄 ShipStation Preview")
    st.dataframe(df_ship.head(10), use_container_width=True)

    st.subheader("📄 FedEx Invoice Preview")
    st.dataframe(df_invoice.head(10), use_container_width=True)

    # Normalize tracking numbers
    df_ship["Tracking #"] = df_ship["Tracking #"].astype(str).str.strip()
    df_invoice["Express or Ground Tracking ID"] = df_invoice["Express or Ground Tracking ID"].astype(str).str.strip()

    # Merge
    merged_df = pd.merge(
        df_ship,
        df_invoice,
        how="left",
        left_on="Tracking #",
        right_on="Express or Ground Tracking ID"
    )

    st.subheader("🔗 Merged Data (Based on Tracking #)")
    st.dataframe(merged_df.head(25), use_container_width=True)

    # Filters
    with st.expander("🔍 Filter Options"):
        recipient = st.text_input("Filter by Recipient (partial match)", "")
        service = st.selectbox("Filter by Service", ["All"] + sorted(df_ship["Service"].dropna().unique().tolist()))
        date = st.text_input("Filter by Ship Date (MM/DD/YY)", "")

        filtered_df = merged_df.copy()

        if recipient:
            filtered_df = filtered_df[filtered_df["Recipient"].str.contains(recipient, case=False, na=False)]
        if service != "All":
            filtered_df = filtered_df[filtered_df["Service"] == service]
        if date:
            filtered_df = filtered_df[filtered_df["Ship Date"] == date]

        st.write(f"Showing {len(filtered_df)} filtered rows")
        st.dataframe(filtered_df, use_container_width=True)

    # Download
    st.download_button("📥 Download Filtered Data as CSV", data=filtered_df.to_csv(index=False), file_name="filtered_shipments.csv", mime="text/csv")

else:
    st.warning("Please upload both CSV files to begin.")
