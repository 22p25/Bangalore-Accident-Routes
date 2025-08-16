USE PYTHON 3.11.x version for this project.
WE HAVE USED OFFICIAL BANGALORE DATA FROM KAGGLE PLATFORM, IT CONTAINS NEARLY 41 LAKHS DATA ROWS.

## 📦 Installation

1.    python -m venv .venv

      source .venv/bin/activate   # on Linux/Mac

      .venv\Scripts\activate      # on Windows

3.    python -m pip install --upgrade pip

      pip install -r requirements.txt

## ▶️ Running the App

3.    cd src
      
4.    streamlit run streamlit_app.py


## 🖼 Example Usage

- **Origin:** Hoodi (12.9961, 77.6955)
- **Destination:** Electronic City (12.8452, 77.6600)  
- Tradeoff alpha and beta slider is used to adjust risk and distance, higher beta means given preference to safety rather than shortest distance, high alpha means given preference to shorter distance than safety.
- Hotspot slider is used to plot hotspots accoridng to distance and number of hotspots you required.
