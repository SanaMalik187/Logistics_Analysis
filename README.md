#  Executive Logistics & Supply Chain Analytics

[Unified Logistics Dashboard](outputs/dashboard2.png)

## 🔍 Project Overview
This project is an end-to-end data analytics pipeline designed to evaluate carrier performance, freight spending, and operational risk. By integrating **SQL Server** data extraction with **Python (Pandas & Matplotlib)** analysis, this tool transforms raw supply chain metrics into an executive-grade decision matrix.

The centerpiece of this project is a custom **Dark-Mode Unified Carrier Matrix**, which maps four core business dimensions simultaneously:
1. **Total Shipment Volume** (X-Axis)
2. **Total Freight Spend / Cost** (Y-Axis)
3. **Cost-per-Mile Efficiency** (Bubble Size)
4. **Delay Risk & Reliability** (Color Spectrum)

---

## 📂 Repository Structure

logistics_analysis/
│
├── outputs/
│   ├── dashboard1.png   # Dark-mode executive dashboard
│   └── dashboard2.png
│
├── scripts/
│   ├── 01_db_connect.py                      # Handles secure SQL Server connection
│   └── 02_analysis.py                        # Core data processing & visualization logic
│
└── README.md                              # Project documentation

🛠️ Tech Stack & Libraries
Language: Python 3.x

Database Management: SQL Server, SQLAlchemy

Data Manipulation & Analysis: Pandas

Data Visualization: Matplotlib 

🚀 Getting Started & How to Run
Follow these steps to set up and run the analysis locally:

1. Clone the Repository
Bash
git clone [https://github.com/SanaMalik187/logistics_analysis.git](https://github.com/your-username/logistics_analysis.git)
cd logistics_analysis
2. Install Dependencies
Make sure you have the required Python libraries installed:

Bash
pip install pandas matplotlib sqlalchemy pyodbc
3. Configure Database Connection
Ensure your database credentials are correctly set up in scripts/db_connect.py.

4. Run the Analysis Script
Execute the main analysis script from the root directory:

Bash
python scripts/analysis.py
This script queries SQL Server, processes carrier metrics, displays the visual interactive dashboard, and automatically saves/overwrites the latest chart inside the outputs/ folder.

💡 Key Business Insights
Spend Concentration: Identified which carriers consume the largest share of the total freight budget relative to their shipment volume.

Cost Efficiency Outliers: Used bubble-sizing to instantly spotlight carriers with high cost-per-mile rates, flagging areas for contract renegotiation.

Risk Management: Color-coded delay percentages allow stakeholders to immediately spot unreliable carriers operating under high volume.


<ElicitationsGroup message="Ready for the final steps to put this on GitHub?">
  <Elicitation label="Show git commands to push project to GitHub" query="Show me the step-by-step git commands to initialize, commit, and push my project to GitHub."/>
  <Elicitation label="Add technology badges to the top of the README" query="How can I add tech stack badges (Python, SQL Server, Pandas) to the top of my README?"/>
</ElicitationsGroup>