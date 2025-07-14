# 🌾 AgriScope – India Crop Intelligence Dashboard

AgriScope is an AI-powered dashboard built for agriculture students, researchers, and policymakers to explore and analyze crop production trends across India.  
It combines historical data, rainfall patterns, and real-time AI insights using Google’s Gemini API — all wrapped in a sleek, Streamlit-powered UI.



---

## 🔍 Features

✅ Compare crop production trends across Indian states  
✅ Analyze **rainfall vs. yield correlations**  
✅ Get **live mandi price updates** using Gemini AI  
✅ Generate **AI-powered summaries** of agri patterns  
✅ Forecast **future crop trends** with Gemini  
✅ View interactive **choropleth map** for regional output  
✅ Export **PDF reports** with charts and AI insights

---

## 🧠 Why It’s Useful

> Most AgriTech tools are made for large enterprises.  
> **AgriScope is made for students.** 📚  
It transforms raw CSVs and government data into interactive visualizations, research-ready insights, and forecasted trends — all powered by AI.

---

## 🛠️ Tech Stack

| Layer         | Tech                                 |
|---------------|--------------------------------------|
| Frontend      | `Streamlit`, `Plotly`, `Matplotlib`  |
| Backend       | `Python`, `Pandas`, `scikit-learn`   |
| AI / LLMs     | `Gemini 1.5 Flash API`               |
| Data Sources  | Govt. crop datasets, rainfall data   |
| Export Tools  | `fpdf`, `Streamlit download button`  |

---

## 📁 Project Structure

```bash
AgriScope/
│
├── app.py                          # Streamlit UI app
├── train_yield_model.py           # ML model trainer
├── utils/
│   ├── data_loader.py             # Load crop, rainfall, price data
│   ├── gemini_ai.py               # Gemini API AI functions
│   ├── geo_plot.py                # Choropleth map builder
│   ├── charts.py                  # Matplotlib + Plotly chart renderers
│   ├── price_loader.py
│   ├── rainfall_loader.py
│   └── pdf_exporter.py            # Generate PDF reports
│
├── data/
│   ├── crop_production.csv        # Raw crop data
│   ├── rainfall_data.csv
│   └── india_states.geojson       # GeoJSON map of Indian states
│
├── .streamlit/
│   └── secrets.toml               # Store Gemini API Key
│
└── requirements.txt
🚀 Run Locally
1. Clone the repo

git clone https://github.com/yourusername/agriscope.git
cd agriscope
2. Install dependencies

pip install -r requirements.txt
3. Setup your Gemini API key
Create a .streamlit/secrets.toml file:

toml

GEMINI_API_KEY = "your_gemini_api_key"
4. Start the Streamlit app

streamlit run app.py
📊 Sample Demo
Choose a region like Punjab, pick Rice and Wheat, generate insights and predictions, and download a PDF — all in one flow!

📦 PDF Export Example
Every student can export a complete visual + AI summary report for assignments or local studies.

🤝 Contributions
This project is part of my #10Weeks10Projects challenge.
If you're passionate about AI for Bharat — feel free to collaborate, fork, or suggest improvements.

🙏 Acknowledgments
Government of India open data portal

Gemini 1.5 Flash (Google AI)

Indian agriculture students who inspired this tool

📬 Contact
🔗 LinkedIn –https://www.linkedin.com/in/reddy-santosh-kumar-a5b9622a2/
🐙 GitHub – https://github.com/Santosh-Reddy1310
📧 Email – reddysantosh1310@gmail.com

🌱 Built for Bharat
“Empowering the next billion learners with AI-powered, real-world tools.”
