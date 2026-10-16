import pandas as pd
from sqlalchemy import create_engine

SERVER = '.'
DATABASE = 'logistics_shipment_db'
engine =create_engine(f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes")

df=pd.read_sql("SELECT * FROM shipments",engine)

print("=" * 50)
print(" LOGISTICS PERFORMANCE & FINANCIAL REPORT")
print("=" * 50)
print("\n--- 1. FINANCIAL & SPEND ANALYSIS ---")

# Total Spend by Carrier: Which carrier accounts for the highest total freight spend?
total_spend=df.groupby("carrier")["freight_cost"].sum()
print(total_spend.sort_values(ascending=False).reset_index().head(1))

# Budget Share (%): What percentage of the overall total freight budget does each carrier represent?
total_spend=df.groupby("carrier")["freight_cost"].sum().reset_index()
total=total_spend["freight_cost"].sum()
percent_share=(total_spend["freight_cost"]/total)*100
total_spend["budget_share"]=percent_share
print(total_spend.sort_values("budget_share",ascending=False))

# Cost by Package Type: What is the average freight cost for each package type?
cost_by_pckg_type=df.groupby("package_type")["freight_cost"].mean()
print(cost_by_pckg_type.sort_values(ascending=False).reset_index())



print("\n--- 2. OPERATIONAL RELIABILITY ANALYSIS ---")

# What is the exact count of shipments for each delivery status (On-Time, Delayed, Cancelled, etc.) across the entire dataset?
status_breakdown=df.groupby("delivery_status")["shipment_id"].count().reset_index()
print(status_breakdown)

# When factoring in total shipment volumes, which carrier has the highest percentage of delayed shipments?
carrier_delay_rates=pd.read_sql("""SELECT carrier,count(carrier) as COUNT
                                                       FROM shipments
                                                       WHERE delivery_status='Delayed'
                                                       GROUP BY carrier  ;
                                                        """,engine)
total_delayed_shipments=carrier_delay_rates["COUNT"].sum()
delay_percent=(carrier_delay_rates['COUNT']/total_delayed_shipments)*100
carrier_delay_rates["Shipment Delayed %"]=delay_percent
print(carrier_delay_rates.sort_values("Shipment Delayed %",ascending=False))

# On average, do shipments that end up delayed cost more or less than shipments that arrive on time?
delay_cost_comparison = df.groupby('delivery_status')['freight_cost'].mean().reset_index()
delay_cost_comparison['freight_cost'] = delay_cost_comparison['freight_cost'].round(2)
print(delay_cost_comparison)



print("\n--- 3. ROUTE EFFICIENCY (COST PER MILE) ---")

# Average Transit Distance: What is the average distance (in miles) traveled per shipment for each carrier?
avg_transit_distance=df.groupby("carrier")["distance_miles"].mean().reset_index()
print(avg_transit_distance)

# Cost-per-Mile Efficiency: Which carrier provides the best financial efficiency when measuring Cost per Mile?
df["cost_per_mile"]=df["freight_cost"]/df["distance_miles"]
Cost_per_Mile_Efficiency=df.groupby("carrier")["cost_per_mile"].mean().reset_index().sort_values("cost_per_mile",ascending=False)
print(Cost_per_Mile_Efficiency)


print("\n--- 4. RISK & OUTLIER DETECTION ---")

# Top Cost Anomalies: What are the top 5 most expensive individual shipments in the entire database, and which carriers operated them?
top_cost_anomalies=pd.read_sql(""" SELECT  TOP 5 carrier,shipment_id,freight_cost 
                                                     FROM shipments
                                                     ORDER BY freight_cost DESC; """,engine)
print(top_cost_anomalies)


# High-Cost Risk: Do shipments with a very high freight cost have a higher tendency to be delayed compared to lower-cost shipments?
high_cost_risk = pd.read_sql("""
    SELECT 
        delivery_status,
        COUNT(*) AS total_shipments,
        ROUND(AVG(freight_cost), 2) AS avg_freight_cost
    FROM shipments
    WHERE delivery_status IN ('On_Time', 'Delayed')
    GROUP BY delivery_status;
""", engine)
print(high_cost_risk)



# ==========================================
# VISUALIZATION & EXECUTIVE DASHBOARD
# ==========================================
import matplotlib.pyplot as plt
import pandas as pd
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# 1. TOP-LEFT: Pie Chart (Carrier Budget Share)
axes[0, 0].pie(
    total_spend["freight_cost"],
    labels=total_spend["carrier"],
    autopct="%1.1f%%",
    startangle=140,
    colors=["#2b5c8f", "#d95f02", "#7570b3", "#1b9e77"],
)
axes[0, 0].set_title(
    "Carrier Budget Share (% Total Spend)", fontsize=12, fontweight="bold"
)

# 2. TOP-RIGHT: Grouped Bar Chart (Carrier Delay Breakdown)
carrier_status = (
    df.groupby(["carrier", "delivery_status"])["shipment_id"]
    .count()
    .unstack(fill_value=0)
)
carrier_status.plot(
    kind="bar",
    ax=axes[0, 1],
    color=["#2ca02c", "#d62728", "#ff7f0e", "#1f77b4"],
    width=0.7,
)
axes[0, 1].set_title(
    "Delivery Reliability by Carrier", fontsize=12, fontweight="bold"
)
axes[0, 1].set_xlabel("Carrier")
axes[0, 1].set_ylabel("Shipment Count")
axes[0, 1].tick_params(axis="x", rotation=30)
axes[0, 1].legend(title="Status")

# 3. BOTTOM-LEFT: Horizontal Bar Chart + Benchmark Line (Efficiency)
overall_avg_cpm = df["cost_per_mile"].mean()

axes[1, 0].barh(
    Cost_per_Mile_Efficiency["carrier"],
    Cost_per_Mile_Efficiency["cost_per_mile"],
    color="#3182bd",
    height=0.5,
)
axes[1, 0].axvline(
    x=overall_avg_cpm,
    color="red",
    linestyle="--",
    linewidth=1.5,
    label=f"Fleet Avg (${overall_avg_cpm:.2f}/mi)",
)
axes[1, 0].set_title(
    "Cost-per-Mile Efficiency vs. Benchmark", fontsize=12, fontweight="bold"
)
axes[1, 0].set_xlabel("Cost per Mile ($)")
axes[1, 0].set_ylabel("Carrier")
axes[1, 0].legend(loc="lower right")

# 4. BOTTOM-RIGHT: Scatter Plot (Distance vs. Cost Anomalies)
axes[1, 1].scatter(
    df["distance_miles"],
    df["freight_cost"],
    alpha=0.6,
    c="#7570b3",
    edgecolors="k",
    s=50,
)
# Highlight top 5 cost anomalies in bright red
axes[1, 1].scatter(
    df.nlargest(5, "freight_cost")["distance_miles"],
    df.nlargest(5, "freight_cost")["freight_cost"],
    color="red",
    s=90,
    label="Top Cost Anomalies",
)
axes[1, 1].set_title(
    "Cost Risk & Outlier Detection (Distance vs Cost)",
    fontsize=12,
    fontweight="bold",
)
axes[1, 1].set_xlabel("Distance (Miles)")
axes[1, 1].set_ylabel("Freight Cost ($)")
axes[1, 1].legend(loc="upper left")
plt.tight_layout()

import os
os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/dashboard1.png", dpi=300, facecolor=fig.get_facecolor())
plt.show()


plt.style.use("dark_background")
carrier_summary = (
    df.groupby("carrier")
    .agg(
        total_spend=("freight_cost", "sum"),
        avg_cost_per_mile=("cost_per_mile", "mean"),
        total_shipments=("shipment_id", "count"),
        delay_count=("delivery_status", lambda x: (x == "Delayed").sum()),
    )
    .reset_index()
)

carrier_summary["delay_rate"] = (
    carrier_summary["delay_count"] / carrier_summary["total_shipments"]
) * 100
fig, ax = plt.subplots(figsize=(10, 6))
bubble_sizes = carrier_summary["avg_cost_per_mile"] * 300

scatter = ax.scatter(
    carrier_summary["total_shipments"],
    carrier_summary["total_spend"],
    s=bubble_sizes,
    c=carrier_summary["delay_rate"],
    cmap="RdYlGn_r",  # Red for high delay %, Green for low delay %
    alpha=0.85,
    edgecolors="white",  # White border around bubbles for contrast
    linewidth=1.5,
)
for i, row in carrier_summary.iterrows():
    ax.annotate(
        row["carrier"],
        (row["total_shipments"], row["total_spend"]),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=10,
        fontweight="bold",
        color="white",
    )
ax.set_title(
    "Carrier Matrix: Volume vs. Spend vs. Efficiency vs. Delay Risk",
    fontsize=13,
    fontweight="bold",
    pad=15,
    color="white",
)
ax.set_xlabel("Total Shipment Volume", fontsize=11, color="white")
ax.set_ylabel("Total Freight Spend ($)", fontsize=11, color="white")

cbar = plt.colorbar(scatter)
cbar.set_label("Delay Rate (%)", fontsize=10, color="white")
cbar.ax.yaxis.set_tick_params(color="white")

ax.grid(True, linestyle="--", alpha=0.2, color="gray")
plt.tight_layout()
import os
os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/dashboard2.png", dpi=300, facecolor=fig.get_facecolor())
plt.show()