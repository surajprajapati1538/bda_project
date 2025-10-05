"""
Energy Forecasting Model Utilities
Provides functions for loading models and making predictions
"""

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

class EnergyForecastingModel:
    """Class to handle energy forecasting model operations"""
    
    def __init__(self, models_path=None):
        if models_path is None:
            # Auto-detect models path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            models_path = os.path.join(os.path.dirname(current_dir), "..", "models")
            models_path = os.path.abspath(models_path)
        
        self.models_path = models_path
        self.model = None
        self.create_features_func = None
        self.config = None
        self.load_model_components()
    
    def load_model_components(self):
        """Load all model components from pickle files"""
        try:
            # Load the trained model
            with open(os.path.join(self.models_path, 'energy_model.pkl'), 'rb') as f:
                self.model = pickle.load(f)
            
            # Don't load function from pickle, use the one defined in this module
            self.create_features_func = self.create_features_local
            
            # Load model configuration
            with open(os.path.join(self.models_path, 'model_config.pkl'), 'rb') as f:
                self.config = pickle.load(f)
            
            print("✅ All model components loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model components: {e}")
            raise
    
    def create_features_local(self, df):
        """Create time-based features from datetime index"""
        df = df.copy()
        df['hour'] = df.index.hour
        df['dayofweek'] = df.index.dayofweek
        df['quarter'] = df.index.quarter
        df['month'] = df.index.month
        df['year'] = df.index.year
        df['dayofyear'] = df.index.dayofyear
        df['dayofmonth'] = df.index.day
        df['weekofyear'] = df.index.isocalendar().week
        return df
    
    def create_features(self, df):
        """Create time-based features from datetime index"""
        return self.create_features_func(df)
    
    def predict_single_datetime(self, datetime_str, energy_value=None):
        """Predict energy consumption for a single datetime"""
        try:
            # Create datetime index
            dt = pd.to_datetime(datetime_str)
            
            # Create dummy dataframe
            dummy_data = {'AEP_MW': [energy_value or 0]}
            df = pd.DataFrame(dummy_data, index=[dt])
            
            # Create features
            df_features = self.create_features(df)
            
            # Extract features for prediction
            X = df_features[self.config['features']]
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            
            return {
                'datetime': datetime_str,
                'prediction': float(prediction),
                'features': X.iloc[0].to_dict()
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
    
    def predict_date_range(self, start_date, end_date, freq='H'):
        """Predict energy consumption for a date range"""
        try:
            # Create date range
            date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
            
            # Create dummy dataframe
            df = pd.DataFrame({'AEP_MW': [0] * len(date_range)}, index=date_range)
            
            # Create features
            df_features = self.create_features(df)
            
            # Extract features for prediction
            X = df_features[self.config['features']]
            
            # Make predictions
            predictions = self.model.predict(X)
            
            # Create result dataframe
            result_df = df_features.copy()
            result_df['prediction'] = predictions
            
            return result_df
            
        except Exception as e:
            print(f"Error in batch prediction: {e}")
            return None
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        return self.config['feature_importance']
    
    def get_model_info(self):
        """Get model information"""
        return {
            'rmse': self.config['performance']['rmse'],
            'features': self.config['features'],
            'target': self.config['target'],
            'created_date': self.config['created_date']
        }

def create_prediction_chart(df, title="Energy Consumption Prediction"):
    """Create a prediction chart"""
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot predictions
    ax.plot(df.index, df['prediction'], 
           color='red', linewidth=2, label='Predicted')
    
    if 'AEP_MW' in df.columns and df['AEP_MW'].sum() > 0:
        ax.plot(df.index, df['AEP_MW'], 
               color='blue', linewidth=2, label='Actual')
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Datetime', fontsize=12)
    ax.set_ylabel('Energy Consumption (MW)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_feature_importance_chart(feature_importance):
    """Create feature importance chart"""
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    features = list(feature_importance.keys())
    importance = list(feature_importance.values())
    
    # Sort by importance
    sorted_idx = np.argsort(importance)
    features = [features[i] for i in sorted_idx]
    importance = [importance[i] for i in sorted_idx]
    
    ax.barh(features, importance, color='steelblue')
    ax.set_title('Feature Importance', fontsize=16, fontweight='bold')
    ax.set_xlabel('Importance', fontsize=12)
    
    plt.tight_layout()
    return fig

def create_hourly_pattern_chart(df):
    """Create hourly pattern chart"""
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Group by hour and calculate mean
    hourly_avg = df.groupby(df.index.hour)['prediction'].mean()
    
    ax.plot(hourly_avg.index, hourly_avg.values, 
           marker='o', linewidth=2, markersize=6, color='green')
    
    ax.set_title('Average Energy Consumption by Hour', fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Average Energy Consumption (MW)', fontsize=12)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_weekly_pattern_chart(df):
    """Create weekly pattern chart"""
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Group by day of week and calculate mean
    weekly_avg = df.groupby(df.index.dayofweek)['prediction'].mean()
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    ax.bar(days, weekly_avg.values, color='orange', alpha=0.7)
    
    ax.set_title('Average Energy Consumption by Day of Week', fontsize=16, fontweight='bold')
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Average Energy Consumption (MW)', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig