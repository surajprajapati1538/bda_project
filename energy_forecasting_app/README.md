# Energy Forecasting Application

A comprehensive machine learning application for energy consumption forecasting with both Streamlit web interface and Flask REST API.

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone or download the project:**
   ```bash
   cd energy_forecasting_app
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure model files are present:**
   Make sure the following pickle files exist in the `../models/` directory:
   - `energy_model.pkl` - The trained XGBoost model
   - `create_features.pkl` - Feature engineering function
   - `model_config.pkl` - Model configuration and metadata

## Streamlit Application

Interactive web application with real-time predictions and visualizations.

### Features:
- **Single Prediction**: Get energy consumption prediction for any specific datetime
- **Date Range Prediction**: Generate predictions for multiple days with customizable frequency
- **Pattern Analysis**: Analyze hourly and weekly consumption patterns
- **Feature Importance**: View which time-based features are most important for predictions

### Running the Streamlit App:
```bash
cd streamlit_app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Usage:
1. **Single Prediction Tab**: Select a date and time to get instant prediction
2. **Date Range Tab**: Choose start/end dates and frequency for batch predictions
3. **Analysis Tab**: Generate pattern analysis charts for any date range
4. **Feature Importance Tab**: View model feature importance rankings

## Flask REST API

RESTful API for programmatic access to energy forecasting capabilities.

### Running the Flask API:
```bash
cd flask_api
python app.py
```

The API will be available at `http://localhost:5000`

### API Documentation:
Visit `http://localhost:5000` for interactive API documentation.

### Key Endpoints:

#### Health Check
```bash
GET /api/health
```

#### Single Prediction
```bash
POST /api/predict/single
Content-Type: application/json

{
    "datetime": "2024-06-15T14:00:00"
}
```

#### Range Prediction
```bash
POST /api/predict/range
Content-Type: application/json

{
    "start_date": "2024-06-15",
    "end_date": "2024-06-16",
    "frequency": "H"
}
```

#### Prediction with Chart
```bash
POST /api/predict/chart
Content-Type: application/json

{
    "start_date": "2024-06-15",
    "end_date": "2024-06-16",
    "frequency": "H",
    "chart_type": "prediction"
}
```

#### Feature Importance
```bash
GET /api/analysis/feature-importance
```

#### Pattern Analysis
```bash
POST /api/analysis/patterns
Content-Type: application/json

{
    "start_date": "2024-06-01",
    "end_date": "2024-06-07"
}
```

## Project Structure

```
energy_forecasting_app/
├── utils/
│   └── model_utils.py          # Model utilities and helper functions
├── streamlit_app/
│   └── app.py                  # Streamlit web application
├── flask_api/
│   ├── app.py                  # Flask REST API
│   └── templates/
│       └── index.html          # API documentation page
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Model Information

The application uses an XGBoost regression model trained on historical energy consumption data.

### Features Used:
- **hour**: Hour of the day (0-23)
- **dayofweek**: Day of the week (0=Monday, 6=Sunday)  
- **month**: Month of the year (1-12)
- **quarter**: Quarter of the year (1-4)
- **year**: Year
- **dayofyear**: Day of the year (1-365)
- **weekofyear**: Week of the year (1-53)
- **dayofmonth**: Day of the month (1-31)

### Performance:
- **RMSE**: ~1649 MW on test set
- **Training Data**: Historical energy consumption (AEP dataset)
- **Train/Test Split**: 2015-01-01

## Usage Examples

### Python API Client:
```python
import requests
import json

# Single prediction
response = requests.post('http://localhost:5000/api/predict/single', 
                        json={'datetime': '2024-06-15T14:00:00'})
result = response.json()
print(f"Predicted consumption: {result['prediction']['prediction']:.2f} MW")

# Range prediction
response = requests.post('http://localhost:5000/api/predict/range', 
                        json={
                            'start_date': '2024-06-15',
                            'end_date': '2024-06-16',
                            'frequency': 'H'
                        })
data = response.json()
print(f"Generated {data['summary']['count']} predictions")
```

### JavaScript API Client:
```javascript
// Single prediction
fetch('http://localhost:5000/api/predict/single', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({datetime: '2024-06-15T14:00:00'})
})
.then(response => response.json())
.then(data => console.log('Prediction:', data.prediction.prediction));
```

## Customization

### Adding New Features:
1. Modify the feature engineering function in `model_utils.py`
2. Retrain the model with new features
3. Update the pickle files

### Styling:
- **Streamlit**: Modify CSS in `streamlit_app/app.py`
- **Flask**: Update `flask_api/templates/index.html`

### API Extensions:
Add new endpoints in `flask_api/app.py` following the existing pattern.

## Troubleshooting

### Common Issues:

1. **Model files not found**:
   - Ensure pickle files exist in `../models/` directory
   - Run the notebook to generate model files

2. **Import errors**:
   - Check if all requirements are installed: `pip install -r requirements.txt`
   - Verify virtual environment is activated

3. **Port conflicts**:
   - Streamlit default: 8501
   - Flask default: 5000
   - Change ports in respective app files if needed

4. **Memory issues**:
   - Large date ranges may consume significant memory
   - Consider pagination for large requests

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📞 Support

For questions or support, please open an issue in the project repository.