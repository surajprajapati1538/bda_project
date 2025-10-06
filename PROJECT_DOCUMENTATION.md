# Energy Forecasting Project Documentation

## Project Overview

**Project Name:** Energy Consumption Forecasting System  
**Repository:** bda_project  
**Owner:** surajprajapati1538  
**Date Created:** October 2025  
**Technology Stack:** Python, Machine Learning, Web Applications

## Executive Summary

This project implements an advanced energy consumption forecasting system using machine learning techniques. The system provides accurate predictions of energy consumption patterns through both interactive web interfaces and REST API endpoints. Built with XGBoost regression algorithms, the application offers real-time predictions, pattern analysis, and feature importance insights.

## Project Architecture

### System Components

1. **Machine Learning Model**
   - Algorithm: XGBoost Regression
   - Target Variable: Energy consumption (MW)
   - Features: Time-based features (hour, day, week, month, year)
   - Performance: RMSE ~1649 MW

2. **Web Applications**
   - **Streamlit Dashboard:** Interactive user interface
   - **Flask API:** RESTful web service with UI

3. **Data Processing**
   - Dataset: AEP (American Electric Power) hourly consumption data
   - Feature Engineering: Time-series decomposition and temporal features
   - Data Validation: Automated preprocessing pipeline

## Technical Specifications

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.12+ | Runtime environment |
| Streamlit | 1.25.0+ | Interactive dashboard |
| Flask | 2.3.0+ | Web API framework |
| XGBoost | 1.7.0+ | Machine learning model |
| Pandas | 2.0.0+ | Data manipulation |
| NumPy | 1.24.0+ | Numerical computations |
| Matplotlib | 3.7.0+ | Data visualization |
| Seaborn | 0.12.0+ | Statistical plots |
| Scikit-learn | 1.3.0+ | ML utilities |

### File Structure

```
bda-project/
├── energy_forecasting_app/
│   ├── streamlit_app/
│   │   └── app.py                 # Streamlit dashboard
│   ├── flask_api/
│   │   ├── app.py                 # Flask web application
│   │   └── templates/
│   │       ├── dashboard.html     # Interactive UI
│   │       └── index.html         # API documentation
│   ├── utils/
│   │   └── model_utils.py         # Core ML utilities
│   ├── energy_model.pkl           # Trained XGBoost model
│   ├── create_features.pkl        # Feature engineering pipeline
│   └── model_config.pkl           # Model configuration
├── model_training/
│   ├── AEP_hourly.csv            # Training dataset
│   └── *.ipynb                   # Jupyter notebooks
├── env/                          # Virtual environment
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

## Features and Capabilities

### 1. Single Prediction
- **Input:** Date and time selection
- **Output:** Energy consumption prediction in MW
- **Visualization:** Prediction charts and metrics

### 2. Range Prediction
- **Input:** Start date, end date, frequency (hourly/daily)
- **Output:** Time series predictions with statistics
- **Analytics:** Min, max, average consumption patterns

### 3. Pattern Analysis
- **Hourly Patterns:** 24-hour consumption cycles
- **Weekly Patterns:** Day-of-week consumption trends
- **Statistical Insights:** Mean, standard deviation, extremes

### 4. Feature Importance
- **Model Insights:** Most influential features
- **Visualization:** Feature importance rankings
- **Interpretability:** Understanding prediction drivers

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- Git (for cloning repository)
- 4GB+ RAM (for model operations)

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/surajprajapati1538/bda_project.git
   cd bda_project
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv env
   .\env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Applications**
   ```bash
   # Streamlit Dashboard
   cd energy_forecasting_app/streamlit_app
   streamlit run app.py
   
   # Flask Web Application
   cd energy_forecasting_app/flask_api
   python app.py
   ```

## Usage Guide

### Streamlit Dashboard (http://localhost:8501)

1. **Single Prediction Tab**
   - Select date and time using form controls
   - Click "Make Prediction" button
   - View prediction result and charts

2. **Range Prediction Tab**
   - Set start and end dates
   - Choose frequency (hourly/daily)
   - Generate comprehensive predictions

3. **Analysis Tab**
   - Select date range for analysis
   - View hourly and weekly patterns
   - Examine consumption trends

4. **Feature Importance Tab**
   - Display model feature rankings
   - Understand prediction factors

### Flask Web Application (http://localhost:5000)

1. **Interactive Dashboard**
   - Similar functionality to Streamlit
   - Professional web interface
   - AJAX-based real-time updates

2. **API Endpoints**
   - `/api/predict/single` - Single prediction
   - `/api/predict/range` - Range predictions
   - `/api/analysis` - Pattern analysis
   - `/api/analysis/feature-importance` - Feature insights

## API Documentation

### Single Prediction Endpoint

**POST** `/api/predict/single`

**Request Body:**
```json
{
  "datetime": "2024-01-15 14:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "datetime": "2024-01-15 14:30:00",
    "prediction": 12345.67,
    "features": {...}
  }
}
```

### Range Prediction Endpoint

**POST** `/api/predict/range`

**Request Body:**
```json
{
  "start_date": "2024-01-15",
  "end_date": "2024-01-16",
  "frequency": "H"
}
```

**Response:**
```json
{
  "success": true,
  "predictions": [...],
  "summary": {
    "count": 24,
    "mean": 12000.0,
    "max": 15000.0,
    "min": 9000.0
  }
}
```

## Model Performance

### Training Metrics
- **Algorithm:** XGBoost Regression
- **RMSE:** ~1649 MW
- **Features:** 8 time-based features
- **Training Data:** AEP hourly consumption (2004-2018)

### Feature Importance Rankings
1. Hour of day
2. Day of week
3. Month of year
4. Day of year
5. Quarter
6. Year
7. Week of year
8. Day of month

## Development Guidelines

### Code Structure
- **Modular Design:** Separate utilities, models, and applications
- **Error Handling:** Comprehensive exception management
- **Documentation:** Inline comments and docstrings
- **Version Control:** Git with meaningful commit messages

### Testing Strategy
- **Unit Tests:** Model utilities validation
- **Integration Tests:** API endpoint testing
- **User Testing:** Dashboard functionality verification

### Deployment Considerations
- **Environment Variables:** Secure configuration management
- **Scalability:** Containerization ready
- **Monitoring:** Logging and error tracking
- **Performance:** Optimized for production workloads

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   - Solution: Activate virtual environment
   - Command: `.\env\Scripts\activate`

2. **JSON Serialization Error**
   - Solution: Numpy type conversion implemented
   - Status: Fixed in current version

3. **Port Already in Use**
   - Solution: Change port or stop existing process
   - Alternative ports: 8501, 8502, 5000, 5001

4. **Model Loading Failure**
   - Solution: Verify pickle files exist
   - Location: `energy_forecasting_app/*.pkl`

## Future Enhancements

### Planned Features
1. **Real-time Data Integration**
   - Live data streaming
   - Automatic model updates
   - Real-time monitoring dashboard

2. **Advanced Analytics**
   - Seasonal decomposition
   - Anomaly detection
   - Forecast confidence intervals

3. **Enhanced UI/UX**
   - Mobile responsiveness
   - Advanced charting
   - Custom themes

4. **Model Improvements**
   - Ensemble methods
   - Deep learning integration
   - Weather data incorporation

## Contact Information

**Project Owner:** surajprajapati1538  
**Repository:** https://github.com/surajprajapati1538/bda_project  
**Documentation Date:** October 2025

## Appendices

### Appendix A: Dataset Information
- **Source:** American Electric Power (AEP)
- **Time Period:** 2004-2018
- **Frequency:** Hourly measurements
- **Size:** ~121,000 records
- **Format:** CSV with datetime index

### Appendix B: Technical Requirements
- **Minimum RAM:** 4GB
- **Storage:** 500MB+ free space
- **Network:** Internet for initial setup
- **Browser:** Modern web browser (Chrome, Firefox, Edge)

### Appendix C: Version History
- **v1.0:** Initial model development
- **v2.0:** Streamlit dashboard integration
- **v3.0:** Flask API implementation
- **v4.0:** Professional UI enhancements

---

*This document serves as comprehensive documentation for the Energy Forecasting Project. For technical support or questions, please refer to the repository issues section.*