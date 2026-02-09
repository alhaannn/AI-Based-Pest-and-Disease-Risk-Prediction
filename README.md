# 🌾 AI-Based Pest and Disease Risk Prediction System

## 🌟 Overview

The **AI-Based Pest and Disease Risk Prediction System** is a cutting-edge agricultural technology solution designed to empower farmers and agronomists with predictive insights. By leveraging historical data, real-time weather analytics, and advanced machine learning models, this system forecasts the likelihood of pest and disease outbreaks, enabling timely preventive measures.

This full-stack Django application integrates weather data processing, crop health monitoring, and an intelligent alert system to minimize crop loss and optimize pesticide usage.

---

## 🚀 Key Features

### 1. **Crop & Pest Management**
- **Comprehensive Database:** Manage detailed profiles for various crops (e.g., Rice, Wheat, Cotton) and their associated pests/diseases.
- **Life Cycle Tracking:** Monitor crop growth stages and pest life cycles to identify vulnerable periods.
- **Historical Data:** Record past infestation events to train the predictive model.

### 2. **Weather Integration**
- **Real-time Monitoring:** Track key weather parameters: Temperature, Humidity, Rainfall, and Wind Speed.
- **Data Import:** bulk import weather data via CSV for historical analysis.
- **Visual Analytics:** Interactive charts displaying weather trends over time.

### 3. **AI Prediction Engine**
- **Risk Assessment:** Calculates risk scores (0-100%) for specific crop-pest combinations based on environmental factors.
- **Machine Learning:** Uses Gradient Boosting Regressor to analyze patterns between weather conditions and pest outbreaks.
- **Risk Classification:** Automatically categorizes risks as Low, Moderate, High, or Critical.

### 4. **Smart Alerts & Notifications**
- **Automated Alerts:** Generates system alerts when high-risk conditions are detected.
- **Preventive Measures:** Provides actionable, stage-specific control recommendations (Cultural, Biological, Chemical).
- **Dashboard:** Centralized view of all active threats and upcoming risks.

### 5. **Data Analytics & Reporting**
- **Interactive Dashboards:** Visualizations of pest distribution, risk trends, and crop health status.
- **CSV Export:** Export feature for Crops, Pests, Weather Data, and Prediction Logs for offline analysis.
- **PDF Reports:** Generate detailed risk assessment reports.

---

## 🛠️ Technology Stack

- **Backend:** Django 5.x (Python)
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Frontend:** HTML5, CSS3, JavaScript (Chart.js for analytics)
- **AI/ML:** Scikit-learn, Pandas, NumPy
- **Styling:** Custom CSS with a modern, responsive design
- **Icons:** FontAwesome

---

## 📦 Installation Guide

### Prerequisites
- Python 3.10+
- Pip (Python Package Installer)
- Git

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alhaannn/AI-Based-Pest-and-Disease-Risk-Prediction.git
   cd AI-Based-Pest-and-Disease-Risk-Prediction
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load Demo Data (Optional but Recommended)**
   Populate the system with realistic Indian agricultural data:
   ```bash
   python manage.py load_indian_demo_data
   ```
   *Use `--clear` flag to wipe existing data before loading.*

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000/`.

---

## 📖 User Guide

### 1. Dashboard
The landing page provides a high-level summary:
- **Active Alerts:** Immediate threats requiring attention.
- **Weather Overview:** Current conditions in your monitored regions.
- **Quick Actions:** Shortcuts to add data or generate predictions.

### 2. Managing Data
- **Crops:** Go to `Crops > Add Crop` to register new plantings.
- **Pests:** View the `Pest Library` to understand threats.
- **Weather:** Use `Weather > Add Data` or `Import CSV` to update environmental records.

### 3. Generating Predictions
1. Navigate to **Predictions > Generate**.
2. The AI engine will analyze all crop-pest pairs against recent weather.
3. View results in the **Prediction List**. High-risk items are highlighted.

### 4. Viewing Alerts
- **Alerts Menu:** Shows all generated warnings.
- **Details:** Click an alert to see specific **Preventive Measures** tailored to the pest and crop stage.

---

## 👨‍💻 Developer Documentation

### Project Structure
```
AI-Based-Pest-and-Disease-Risk-Prediction/
├── disease_prediction/     # Project configuration
├── crops/                  # App: Crops, Pests, Infestations
├── weather/                # App: Weather data & analysis
├── predictions/            # App: ML model & risk logic
├── alerts/                 # App: Notification system
├── reports/                # App: PDF/CSV reporting
├── templates/              # HTML Templates
├── static/                 # CSS, JS, Images
└── manage.py               # Django CLI utility
```

### Key Modules

#### **ML Engine (`predictions/ml_engine.py`)**
- `calculate_risk_score(crop, pest, weather_data)`: Core logic.
- Currently uses a heuristic model weighted by:
  - **Temperature:** 30% weight (optimal range check)
  - **Humidity:** 30% weight (high humidity favorability)
  - **Rainfall:** 20% weight
  - **Crop Stage:** 20% weight (susceptibility factor)

#### **Management Commands**
- `load_indian_demo_data.py`: Script to seed the database with diverse crop/pest datasets.

### Extending the Model
To implement a more advanced model:
1. Collect labeled dataset in `predictions/data/`.
2. Train a new model using `scikit-learn`.
3. Update `ml_engine.py` to load the `.pkl` file and run inference.

---

## 🤝 Contributing

Contributions are welcome!
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Built with ❤️ for Smarter Agriculture
</p>
