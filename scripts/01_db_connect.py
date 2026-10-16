import pandas as pd
from sqlalchemy import create_engine

# --- Server & Database Configuration ---
SERVER_NAME = '.'  # Single dot for local default SQL Server instance
DATABASE_NAME = 'logistics_shipment_db'

# --- Build Connection String ---
connection_string = (
    f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

# --- Initialize Database Engine ---
engine = create_engine(connection_string, connect_args={'timeout': 5})

# --- Test Query ---
query = "SELECT TOP 5 * FROM shipments;"

try:
    df = pd.read_sql(query, engine)
    print("✅ Connection Successful!")
    print("\n--- Preview of Data from SQL Server ---")
    print(df[['shipment_id', 'carrier', 'delivery_status']])
except Exception as e:
    print("❌ Connection Failed:")
    print(e)