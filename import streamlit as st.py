import streamlit as st
import pandas as pd
import pyodbc
from datetime import date

# Function to create a database connection
def create_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=sales;UID=root;PWD=mysql123')
    return conn

# Function to fetch data from the database
def fetch_data(start_date, end_date, spice):
    conn = create_connection()
    query = """
    SELECT Date, Price
    FROM YourSpiceTable
    WHERE Date BETWEEN ? AND ?
    AND Spice = ?
    ORDER BY Date
    """
    df = pd.read_sql(query, conn, params=[start_date, end_date, spice])
    conn.close()
    return df

# Function to get list of spices from the database
def get_spices():
    conn = create_connection()
    query = "SELECT DISTINCT Spice FROM YourSpiceTable ORDER BY Spice"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['Spice'].tolist()

# Set page config
st.set_page_config(page_title="Spice Price Tracker", layout="wide")

# Main title
st.title("Spice Price Tracker")

# Create date inputs and spice selection dropdown
col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input("Start Date", date.today())

with col2:
    end_date = st.date_input("End Date", date.today())

with col3:
    spices = get_spices()
    selected_spice = st.selectbox("Select Spice", spices)

# Create fetch button
if st.button("Fetch Data"):
    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        try:
            # Fetch data from the database
            df = fetch_data(start_date, end_date, selected_spice)
            
            if df.empty:
                st.warning("No data found for the selected criteria.")
            else:
                st.write(f"Showing prices for {selected_spice} from {start_date} to {end_date}")
                st.dataframe(df)
                
                # Display a line chart
                st.line_chart(df.set_index('Date')['Price'])
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add a footer
st.markdown("---")
st.markdown("Data sourced from SQL Server database.")