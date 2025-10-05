"""
Energy Forecasting Flask API
RESTful API for energy consumption predictions
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from model_utils import EnergyForecastingModel, create_prediction_chart, create_feature_importance_chart, create_hourly_pattern_chart, create_weekly_pattern_chart

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global model instance
model = None

def convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

def init_model():
    """Initialize the forecasting model"""
    global model
    try:
        model = EnergyForecastingModel()
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return image_base64

@app.route('/')
def home():
    """Home page with interactive dashboard"""
    return render_template('dashboard.html')

@app.route('/api-docs')
def api_docs():
    """API documentation page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        info = model.get_model_info()
        feature_importance = model.get_feature_importance()
        
        return jsonify({
            'model_info': info,
            'feature_importance': feature_importance
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/single', methods=['POST'])
def predict_single():
    """Predict energy consumption for a single datetime"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        datetime_str = data.get('datetime')
        
        if not datetime_str:
            return jsonify({'error': 'datetime parameter is required'}), 400
        
        # Validate datetime format
        try:
            datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS'}), 400
        
        result = model.predict_single_datetime(datetime_str)
        
        if result:
            return jsonify({
                'success': True,
                'prediction': convert_numpy_types(result)
            })
        else:
            return jsonify({'error': 'Prediction failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/range', methods=['POST'])
def predict_range():
    """Predict energy consumption for a date range"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        frequency = data.get('frequency', 'H')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date parameters are required'}), 400
        
        result_df = model.predict_date_range(start_date, end_date, freq=frequency)
        
        if result_df is not None and not result_df.empty:
            # Convert to JSON-friendly format
            predictions = []
            for idx, row in result_df.iterrows():
                predictions.append({
                    'datetime': idx.isoformat(),
                    'prediction': float(row['prediction']),
                    'features': {col: float(row[col]) for col in model.config['features'] if col in row}
                })
            
            # Calculate summary statistics
            summary = {
                'count': len(predictions),
                'mean': float(result_df['prediction'].mean()),
                'max': float(result_df['prediction'].max()),
                'min': float(result_df['prediction'].min()),
                'std': float(result_df['prediction'].std())
            }
            
            return jsonify({
                'success': True,
                'predictions': convert_numpy_types(predictions),
                'summary': convert_numpy_types(summary)
            })
        else:
            return jsonify({'error': 'Prediction failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/chart', methods=['POST'])
def predict_with_chart():
    """Predict and return chart as base64 image"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        frequency = data.get('frequency', 'H')
        chart_type = data.get('chart_type', 'prediction')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date parameters are required'}), 400
        
        result_df = model.predict_date_range(start_date, end_date, freq=frequency)
        
        if result_df is not None and not result_df.empty:
            # Create chart based on type
            if chart_type == 'prediction':
                fig = create_prediction_chart(
                    result_df, 
                    title=f"Energy Consumption Prediction ({start_date} to {end_date})"
                )
            elif chart_type == 'hourly':
                fig = create_hourly_pattern_chart(result_df)
            elif chart_type == 'weekly':
                fig = create_weekly_pattern_chart(result_df)
            else:
                return jsonify({'error': 'Invalid chart_type. Use: prediction, hourly, or weekly'}), 400
            
            # Convert to base64
            chart_base64 = fig_to_base64(fig)
            
            return jsonify({
                'success': True,
                'chart': chart_base64,
                'chart_type': chart_type
            })
        else:
            return jsonify({'error': 'Prediction failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance chart"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        feature_importance = model.get_feature_importance()
        fig = create_feature_importance_chart(feature_importance)
        chart_base64 = fig_to_base64(fig)
        
        return jsonify({
            'success': True,
            'chart': chart_base64,
            'feature_importance': convert_numpy_types(feature_importance)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/patterns', methods=['POST'])
def analyze_patterns():
    """Analyze energy consumption patterns"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date parameters are required'}), 400
        
        # Generate predictions for analysis
        result_df = model.predict_date_range(start_date, end_date, freq='H')
        
        if result_df is not None and not result_df.empty:
            # Create charts
            hourly_fig = create_hourly_pattern_chart(result_df)
            weekly_fig = create_weekly_pattern_chart(result_df)
            prediction_fig = create_prediction_chart(result_df, title="Energy Consumption Analysis")
            
            # Convert to base64
            charts = {
                'hourly_pattern': fig_to_base64(hourly_fig),
                'weekly_pattern': fig_to_base64(weekly_fig),
                'time_series': fig_to_base64(prediction_fig)
            }
            
            # Calculate pattern statistics
            hourly_stats = result_df.groupby(result_df.index.hour)['prediction'].agg(['mean', 'std']).to_dict()
            weekly_stats = result_df.groupby(result_df.index.dayofweek)['prediction'].agg(['mean', 'std']).to_dict()
            
            return jsonify({
                'success': True,
                'charts': charts,
                'statistics': {
                    'hourly': hourly_stats,
                    'weekly': weekly_stats,
                    'overall': {
                        'mean': float(result_df['prediction'].mean()),
                        'std': float(result_df['prediction'].std()),
                        'max': float(result_df['prediction'].max()),
                        'min': float(result_df['prediction'].min())
                    }
                }
            })
        else:
            return jsonify({'error': 'Analysis failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis', methods=['POST'])
def analysis():
    """Generate analysis for a date range - simplified version for dashboard"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date parameters are required'}), 400
        
        # Use the existing patterns endpoint functionality
        result_df = model.predict_date_range(start_date, end_date, freq='H')
        
        if result_df is not None and not result_df.empty:
            response_data = {'success': True}
            
            # Generate hourly pattern chart
            try:
                hourly_fig = create_hourly_pattern_chart(result_df)
                if hourly_fig:
                    response_data['hourly_pattern_chart'] = fig_to_base64(hourly_fig)
            except Exception as e:
                print(f"Error creating hourly pattern chart: {e}")
            
            # Generate weekly pattern chart  
            try:
                weekly_fig = create_weekly_pattern_chart(result_df)
                if weekly_fig:
                    response_data['weekly_pattern_chart'] = fig_to_base64(weekly_fig)
            except Exception as e:
                print(f"Error creating weekly pattern chart: {e}")
            
            return jsonify(response_data)
        else:
            return jsonify({'error': 'Analysis failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Energy Forecasting API...")
    
    # Initialize model
    if init_model():
        print("🚀 Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize model. Please check model files.")