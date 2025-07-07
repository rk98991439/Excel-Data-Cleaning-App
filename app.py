import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Data Cleaning App", layout="wide")

st.title("🧹 Excel Data Cleaning App")

# Sidebar - Upload Excel File
st.sidebar.header("Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

    st.sidebar.header("Data Cleaning Options")

    cleaned_data = data.copy()
    updates_summary = []  # To collect update messages

    # Remove Duplicates
    if st.sidebar.checkbox("Remove Duplicate Rows"):
        cleaned_data = cleaned_data.drop_duplicates()
        updates_summary.append(f"✅ Duplicates removed. New shape: {cleaned_data.shape}")

    # Convert to Lowercase
    if st.sidebar.checkbox("Convert String Columns to Lowercase"):
        str_cols = cleaned_data.select_dtypes(include='object').columns
        for col in str_cols:
            cleaned_data[col] = cleaned_data[col].str.lower()
        updates_summary.append("✅ Converted string columns to lowercase")

    # Find Duplicates (Does not modify data)
    if st.sidebar.checkbox("Highlight Duplicate Rows"):
        duplicate_rows = cleaned_data[cleaned_data.duplicated()]
        if not duplicate_rows.empty:
            st.warning(f"⚠️ Found {len(duplicate_rows)} duplicate rows:")
            st.dataframe(duplicate_rows)
        else:
            st.success("✅ No duplicate rows found.")

    # Drop Missing Values
    if st.sidebar.checkbox("Drop Rows with Missing Values"):
        cleaned_data = cleaned_data.dropna()
        updates_summary.append(f"✅ Rows with missing values dropped. New shape: {cleaned_data.shape}")

    # Columns for side-by-side view
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Original Data")
        st.dataframe(data)

    with col2:
        st.subheader("🧹 Cleaned Data Preview")
        st.dataframe(cleaned_data)

    # Display updates summary
    if updates_summary:
        st.subheader("📝 Cleaning Summary")
        for msg in updates_summary:
            st.write(msg)

    # Download cleaned data
    csv = cleaned_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Cleaned Data as CSV", csv, "cleaned_data.csv", "text/csv")

else:
    st.info("Please upload an Excel file to get started.")
