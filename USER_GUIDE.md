# 📘 User Guide - AI-Based Pest and Disease Risk Prediction System

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Crop Management](#crop-management)
4. [Pest & Disease Management](#pest--disease-management)
5. [Weather Data Management](#weather-data-management)
6. [AI Predictions](#ai-predictions)
7. [Alert System](#alert-system)
8. [Analytics & Reports](#analytics--reports)
9. [Data Export](#data-export)
10. [Tips & Best Practices](#tips--best-practices)
11. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### First-Time Setup

After installation, follow these steps to set up your system:

1. **Access the Admin Panel**
   - URL: `http://127.0.0.1:8000/admin/`
   - Login with your superuser credentials
   - Add initial preventive measures for common pests

2. **Navigate to the Dashboard**
   - URL: `http://127.0.0.1:8000/`
   - View the welcome screen and statistics

3. **Add Your First Data**
   - Start with crops → Add pests → Import weather data → Generate predictions

---

## 📊 Dashboard Overview

### Main Dashboard Features

The dashboard provides a quick overview of your agricultural data:

**Statistics Cards:**
- **Total Crops**: Number of crops being monitored
- **Active Pests**: Pests/diseases in the database
- **Weather Records**: Recent weather data points
- **Risk Predictions**: Total AI-generated predictions

**Quick Actions:**
- Add Crop
- Add Pest
- Add Weather Data
- Generate Predictions

**Recent Activity:**
- Latest predictions
- Recent alerts
- Recent weather data

**Charts:**
- Risk trend over time
- Crop distribution
- Alert severity distribution

---

## 🌾 Crop Management

### Adding a New Crop

1. **Navigate**: Click "Crops" in the navigation menu
2. **Click**: "Add Crop" button
3. **Fill in Details**:
   - **Name**: e.g., "North Field Wheat"
   - **Crop Type**: Select from dropdown (Cereal, Vegetable, Fruit, etc.)
   - **Variety**: e.g., "Hard Red Winter"
   - **Growth Stage**: Current stage (Seedling, Vegetative, Flowering, etc.)
   - **Planting Date**: When the crop was planted
   - **Area (hectares)**: Size of the field
   - **Location**: Field location or coordinates
4. **Save**: Click "Save Crop"

### Viewing Crop Details

1. Navigate to "Crops" list
2. Click on a crop name
3. View comprehensive information:
   - Crop details
   - Associated infestations
   - Risk predictions
   - Recommended actions

### Tracking Infestations

1. **From Crop Detail Page**: Click "Add Infestation"
2. **Fill in Details**:
   - **Pest/Disease**: Select from dropdown
   - **Date Detected**: When infestation was noticed
   - **Severity**: Rate 1-10 (1=minor, 10=severe)
   - **Area Affected**: Hectares affected
   - **Treatment Applied**: What action was taken
   - **Notes**: Additional observations
3. **Save**: Click "Save Infestation"

**Why Track Infestations?**
- Builds historical data for ML predictions
- Helps identify patterns
- Improves prediction accuracy over time

### Editing/Deleting Crops

- **Edit**: Click "Edit" button on crop detail page
- **Delete**: Click "Delete" → Confirm deletion
- **Note**: Deleting a crop removes associated infestations and predictions

---

## 🐛 Pest & Disease Management

### Adding a Pest/Disease

1. **Navigate**: Click "Pests" in navigation
2. **Click**: "Add Pest" button
3. **Fill in Details**:
   - **Name**: Common name (e.g., "Aphids")
   - **Pest Type**: Insect, Fungal, Bacterial, Viral, or Weed
   - **Scientific Name**: Latin name (optional but recommended)
   - **Severity Level**: LOW, MEDIUM, or HIGH
   - **Symptoms**: Visible signs of infestation
   - **Affected Crops**: Which crops are vulnerable
4. **Save**: Click "Save Pest"

### Preventive Measures

Preventive measures are managed through the admin panel:

1. **Access Admin**: `/admin/alerts/preventivemeasure/`
2. **Add Measure**:
   - **Pest**: Select the pest
   - **Measure Type**: Name of the preventive action
   - **Description**: Detailed explanation
   - **Effectiveness**: HIGH, MEDIUM, or LOW
   - **Timing**: When to apply (e.g., "Before flowering")
   - **Cost**: LOW, MEDIUM, or HIGH
   - **Application Method**: How to apply

**Example Preventive Measures:**
- **Neem Oil Spray** (HIGH effectiveness, LOW cost)
- **Crop Rotation** (MEDIUM effectiveness, LOW cost)
- **Biological Control** (HIGH effectiveness, MEDIUM cost)

---

## 🌤️ Weather Data Management

### Manual Weather Entry

1. **Navigate**: Weather → Add Weather Data
2. **Fill in Details**:
   - **Date**: Date of observation
   - **Location**: Weather station or field location
   - **Temperature Min/Max/Avg**: In Celsius
   - **Humidity**: Percentage (0-100)
   - **Rainfall**: In millimeters
   - **Wind Speed**: In km/h
3. **Save**: Click "Save Weather Data"

### CSV Bulk Import

**Step 1: Download Template**
1. Navigate to Weather → Import CSV
2. Click "Download CSV Template"
3. Open in Excel or Google Sheets

**Step 2: Fill Template**

CSV Format:
```csv
date,location,temperature_min,temperature_max,temperature_avg,humidity,rainfall,wind_speed
2026-02-01,Field A,15.5,28.3,21.9,65,0,12.5
2026-02-02,Field A,16.2,29.1,22.6,68,2.3,10.8
```

**Required Columns:**
- `date`: YYYY-MM-DD format
- `location`: Text
- `temperature_min`: Decimal (°C)
- `temperature_max`: Decimal (°C)
- `temperature_avg`: Decimal (°C)
- `humidity`: Integer (0-100)
- `rainfall`: Decimal (mm)
- `wind_speed`: Decimal (km/h)

**Step 3: Upload**
1. Click "Choose File"
2. Select your CSV file
3. Click "Import Weather Data"
4. Review success message

**Tips:**
- Use consistent location names
- Ensure dates are in correct format
- Check for missing values
- Import historical data for better predictions

### Weather Analysis

1. **Navigate**: Weather → Analysis
2. **Select Time Period**: 7, 14, 30, or 60 days
3. **View Charts**:
   - Temperature trends
   - Humidity patterns
   - Rainfall distribution
   - Wind speed variations
4. **Risk Assessment**: View weather-based risk factors

---

## 🤖 AI Predictions

### Understanding the ML Engine

The system uses **Gradient Boosting Regressor** with **18 engineered features**:

**Weather Features:**
- Average temperature
- Humidity levels
- Rainfall amount
- Wind speed

**Crop Features:**
- Crop type
- Growth stage
- Area (hectares)

**Pest Features:**
- Pest type
- Severity level

**Historical Features:**
- Past infestation count
- Average historical severity
- Days since last infestation

**Seasonal Features:**
- Monsoon season indicator
- Winter season indicator
- Summer season indicator

### Generating Predictions

**Step 1: Check Data Availability**
1. Navigate to Predictions → Generate Predictions
2. Review data status:
   - ✅ Crops available
   - ✅ Pests available
   - ✅ Recent weather data
   - ✅ Historical records (optional but improves accuracy)

**Step 2: Generate**
1. Click "Generate Predictions Now"
2. Wait for processing (usually 5-30 seconds)
3. View success message with count

**Step 3: Review Results**
1. Navigate to Predictions list
2. View risk scores and levels
3. Click "Details" for comprehensive information

### Understanding Predictions

**Risk Score (0-100%):**
- **0-30%**: LOW risk - Monitor situation
- **31-69%**: MEDIUM risk - Prepare preventive measures
- **70-100%**: HIGH risk - Take immediate action

**Confidence Level:**
- Indicates how certain the model is
- Higher confidence = more reliable prediction
- Based on data quality and quantity

**Risk Level:**
- **LOW**: Green badge - Routine monitoring
- **MEDIUM**: Orange badge - Increased vigilance
- **HIGH**: Red badge - Immediate attention required

**Contributing Factors:**
- Lists the main reasons for the risk score
- Examples: "High humidity + Monsoon season + Past infestations"

### Viewing Prediction Details

1. Click "Details" on any prediction
2. View comprehensive information:
   - **Prediction Summary**: Risk score, level, confidence
   - **Recent Weather**: Last 7 days of conditions
   - **Historical Records**: Past infestations
   - **Preventive Measures**: Available actions

---

## 🔔 Alert System

### Alert Dashboard

1. **Navigate**: Alerts → Dashboard
2. **View Statistics**:
   - Total alerts (last 7/14/30/60 days)
   - Unread alerts
   - Critical alerts
   - Danger alerts

3. **Charts**:
   - **Alert Trend**: Daily alert count over time
   - **Severity Distribution**: Breakdown by severity

4. **Top Lists**:
   - Most affected crops
   - Most common pests

### Alert Severity Levels

**CRITICAL** (Dark Red):
- Risk score ≥ 80%
- Immediate action required
- Potential for significant crop loss

**DANGER** (Red):
- Risk score 70-79%
- Urgent attention needed
- High risk of infestation

**WARNING** (Orange):
- Risk score 60-69%
- Monitor closely
- Prepare preventive measures

**INFO** (Blue):
- Risk score < 60%
- Informational only
- Routine monitoring

### Managing Alerts

**View Alerts:**
1. Navigate to Alerts → Alert Center
2. Use filters:
   - **Status**: All, Unread, Read
   - **Severity**: All, Critical, Danger, Warning, Info
3. Click "Filter" to apply

**Mark as Read:**
- **Single Alert**: Click "Mark Read" button
- **All Alerts**: Click "Mark All Read" button

**Get Recommendations:**
1. Click "Recommendations" on any alert
2. View preventive measures categorized by effectiveness:
   - **High Effectiveness** (Green): Top priority
   - **Medium Effectiveness** (Orange): Alternatives
   - **Low Effectiveness** (Blue): Additional options

**Delete Alerts:**
1. Click trash icon on alert
2. Confirm deletion
3. Alert is permanently removed

### Preventive Measures Database

1. **Navigate**: Alerts → Preventive Measures
2. **Filter**:
   - By pest
   - By effectiveness level
3. **View Details**:
   - Measure type
   - Description
   - Timing
   - Cost
   - Application method

---

## 📈 Analytics & Reports

### Prediction Analytics

1. **Navigate**: Predictions → Analytics
2. **View 30-Day Statistics**:
   - Total predictions
   - High/Medium/Low risk counts

3. **Charts**:
   - **Daily High-Risk Trend**: Line chart showing high-risk predictions over 30 days
   - **Risk Distribution**: Doughnut chart showing overall risk breakdown

4. **Top Lists**:
   - **Top 5 High-Risk Crops**: Most vulnerable crops
   - **Top 5 Most Predicted Pests**: Common threats

5. **Confidence Metrics**:
   - Average confidence by risk level
   - Model performance indicators

### Alert Analytics

1. **Navigate**: Alerts → Dashboard
2. **Select Time Period**: 7, 14, 30, or 60 days
3. **View Trends**:
   - Daily alert count
   - Severity distribution
   - Top affected crops/pests

---

## 💾 Data Export

### Export Predictions (CSV)

**Purpose**: Export filtered predictions for analysis in Excel/Google Sheets

**Steps:**
1. Navigate to Predictions
2. Apply desired filters (crop, pest, risk level)
3. Click "Export CSV"
4. Save file (e.g., `predictions_20260209_111500.csv`)

**CSV Columns:**
- Prediction Date
- Crop Name, Type, Growth Stage
- Pest/Disease Name, Type
- Risk Score (%), Risk Level
- Confidence (%)
- Contributing Factors

**Use Cases:**
- Offline analysis
- Custom reports
- Sharing with agronomists
- Record keeping

### Export All Data (ZIP)

**Purpose**: Complete system backup with all data

**Steps:**
1. Navigate to Predictions
2. Click "Export All Data"
3. Save ZIP file (e.g., `pest_prediction_data_20260209_111500.zip`)
4. Extract to view 5 CSV files

**Included Files:**
1. **predictions.csv**: All predictions
2. **crops.csv**: All crop data
3. **pests.csv**: All pest/disease data
4. **weather_data.csv**: Last 100 weather records
5. **alerts.csv**: Last 100 alerts

**Use Cases:**
- Regular backups
- Data migration
- Compliance/auditing
- External analysis tools

---

## 💡 Tips & Best Practices

### Data Quality

1. **Regular Weather Updates**:
   - Update weather data daily or weekly
   - Use consistent location names
   - Ensure accuracy of measurements

2. **Track All Infestations**:
   - Record even minor infestations
   - Include treatment details
   - Add detailed notes
   - More historical data = better predictions

3. **Keep Crop Information Current**:
   - Update growth stages regularly
   - Record harvest dates
   - Update planting dates for new seasons

### Prediction Accuracy

1. **Build Historical Data**:
   - System learns from past infestations
   - More data = higher confidence
   - Track outcomes of predictions

2. **Regular Prediction Generation**:
   - Generate predictions weekly
   - More frequent during critical growth stages
   - After significant weather events

3. **Act on High-Risk Predictions**:
   - Don't ignore HIGH risk predictions
   - Implement recommended preventive measures
   - Monitor situation closely

### Alert Management

1. **Check Alerts Daily**:
   - Review critical alerts immediately
   - Mark as read when addressed
   - Don't let alerts accumulate

2. **Use Recommendations**:
   - Follow high-effectiveness measures first
   - Consider cost and timing
   - Document results

3. **Filter Effectively**:
   - Use filters to focus on priorities
   - Start with critical/danger alerts
   - Address by crop or pest type

### System Maintenance

1. **Regular Backups**:
   - Export all data monthly
   - Store backups securely
   - Test restore procedures

2. **Clean Old Data**:
   - Archive old predictions (>1 year)
   - Keep relevant historical infestations
   - Maintain weather data for trends

3. **Monitor Performance**:
   - Check prediction confidence levels
   - Review alert accuracy
   - Adjust preventive measures based on results

---

## 🔧 Troubleshooting

### Common Issues

**Issue: No predictions generated**
- **Cause**: Missing data (crops, pests, or weather)
- **Solution**: Ensure you have at least 1 crop, 1 pest, and recent weather data

**Issue: Low confidence predictions**
- **Cause**: Insufficient historical data
- **Solution**: Continue tracking infestations; confidence improves over time

**Issue: CSV import fails**
- **Cause**: Incorrect format or missing columns
- **Solution**: Use the provided template; check date format (YYYY-MM-DD)

**Issue: Alerts not generating**
- **Cause**: No high-risk predictions
- **Solution**: This is normal if risks are low; alerts only generate for HIGH risk

**Issue: Charts not displaying**
- **Cause**: Browser compatibility or JavaScript disabled
- **Solution**: Use modern browser (Chrome, Firefox, Edge); enable JavaScript

### Getting Help

**Documentation:**
- README.md - Installation and overview
- DEPLOYMENT.md - Production deployment
- This guide - Detailed usage instructions

**Support:**
- GitHub Issues: Report bugs or request features
- Email: Contact system administrator
- Admin Panel: Check system logs

### Data Recovery

**If data is lost:**
1. Check recent backups (ZIP exports)
2. Restore from backup:
   - Extract ZIP file
   - Use admin panel to import data
   - Or contact administrator

**Prevention:**
- Export all data monthly
- Store backups in multiple locations
- Test restore procedures regularly

---

## 📞 Support & Resources

### Quick Reference

**Key URLs:**
- Dashboard: `/`
- Crops: `/crops/`
- Pests: `/pests/`
- Weather: `/weather/`
- Predictions: `/predictions/`
- Alerts: `/alerts/`
- Admin: `/admin/`

**Important Actions:**
- Generate Predictions: `/predictions/generate/`
- Import Weather: `/weather/import/`
- Alert Dashboard: `/alerts/dashboard/`
- Analytics: `/predictions/analytics/`

### Best Practices Summary

✅ **DO:**
- Update weather data regularly
- Track all infestations
- Generate predictions weekly
- Act on high-risk alerts
- Export data monthly
- Review analytics regularly

❌ **DON'T:**
- Ignore high-risk predictions
- Delete historical data
- Skip weather updates
- Neglect alert management
- Forget to backup data

---

**Happy Farming! 🌾**

For additional support, consult the README.md or contact your system administrator.
