# Bangalore Accident Routes

A data-driven route optimization system for Bangalore that helps users find safer routes by analyzing historical accident data. This project uses official Bangalore accident data from Kaggle containing nearly 41 lakh (4.1 million) data rows to provide intelligent route suggestions that balance safety and distance.

## 🚗 Features

- **Safe Route Planning**: Find routes that minimize accident risk while considering distance
- **Interactive Visualization**: View accident hotspots and safe routes on an interactive map
- **Customizable Parameters**: Adjust safety vs. distance trade-offs using intuitive sliders
- **Real-time Analysis**: Process large-scale accident data for dynamic route suggestions
- **Hotspot Detection**: Visualize accident-prone areas based on customizable distance parameters

## 🛠️ Technology Stack

- **Python 3.11.x**: Core programming language
- **Streamlit**: Web application framework for interactive UI
- **Data Source**: Official Bangalore accident data from Kaggle (41+ lakh records)
- **Geospatial Analysis**: Location-based route optimization algorithms

## 📋 Prerequisites

- Python 3.11.x (required version)
- pip package manager
- Git

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/22p25/Bangalore-Accident-Routes.git
   cd Bangalore-Accident-Routes
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Linux/Mac
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   cd src
   streamlit run streamlit_app.py
   ```

5. **Access the application**
   - Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## 🎯 Usage

### Route Planning
The application provides intelligent route suggestions between two points:

- **Default Example**: 
  - Origin: Hoodi (12.9961, 77.6955)
  - Destination: Electronic City (12.8452, 77.6600)

### Parameter Controls

#### Trade-off Sliders (Alpha & Beta)
- **Alpha (Distance Weight)**: Higher values prioritize shorter routes over safety
- **Beta (Safety Weight)**: Higher values prioritize safety over shortest distance
- Use these sliders to balance between getting there quickly vs. getting there safely

#### Hotspot Analysis
- **Hotspot Slider**: Controls the visualization of accident hotspots
- Adjust based on:
  - Distance radius for hotspot detection
  - Number of hotspots to display
- Helps identify accident-prone areas to avoid

## 📊 Data Source

This project utilizes official Bangalore accident data sourced from Kaggle, containing:
- **Volume**: Nearly 41 lakh (4.1 million) accident records
- **Coverage**: Comprehensive historical accident data for Bangalore
- **Authority**: Official government data ensuring reliability and accuracy

## 🗺️ How It Works

1. **Data Processing**: Analyzes massive accident datasets to identify high-risk areas
2. **Risk Assessment**: Calculates accident probability for different route segments
3. **Route Optimization**: Uses algorithms that balance safety and efficiency
4. **Visual Feedback**: Provides interactive maps showing safe routes and danger zones

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation




---

**Note**: This project is designed to assist in route planning and should be used as a supplementary tool alongside standard navigation systems. Always follow traffic rules and exercise caution while driving.
