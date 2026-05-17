# IntelliBI

🧠 IntelliBI – AI-Driven Business Intelligence Platform
An intelligent, AI-powered BI dashboard built with Python & Streamlit.

🚀 Quick Start
1. Install Dependencies
pip install -r requirements.txt
2. Run the App
streamlit run app.py

| Feature               | Description                                 |
| --------------------- | ------------------------------------------- |
| 📡 Live API Data      | Fetches real-time products from API         |
| 📁 CSV Upload         | Upload your own dataset with auto-detection |
| 📊 KPI Cards          | Total Sales, Profit, Avg Margin, Products   |
| 📈 Interactive Charts | Bar, Pie, Line, Scatter & Trend charts      |
| 🤖 AI Insights        | Auto-generated business insights            |
| 💬 Chat Interface     | Ask questions in plain English              |
| 🔍 Smart Filters      | Category filter + price slider              |
| 🚨 Anomaly Detection  | Detects unusual patterns in data            |
| ⬇️ Export CSV         | Download filtered dataset                   |


💬 Chat Query Examples
"What is total sales?"
"Which product has the highest profit?"
"Show top 3 categories"
"What is the profit margin?"
"How many products are there?"
"Are there any outliers?"
"Give me a summary"
"What is the average price?"

📁 Project Structure
IntelliBI/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file

🛠 Tech Stack
Streamlit – UI framework
Pandas – Data manipulation
NumPy – Numerical operations
Plotly – Interactive charts
Requests – API calls

🤖 Machine Learning Used
🔹 Isolation Forest-Detects anomalies and outliers in datasets.
🔹 DBSCAN=Performs clustering and unusual behavior detection.

📝 Notes
API data auto-refreshes every 60 seconds (click "Refresh Data" for manual refresh)
For CSV uploads, the app auto-detects columns and derives missing fields (sales, profit, etc.)
Outlier detection uses the IQR (Interquartile Range) method
