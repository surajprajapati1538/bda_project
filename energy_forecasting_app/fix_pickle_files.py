"""
Script to fix and regenerate pickle files for the energy forecasting model
"""

import pickle
import pandas as pd
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define the feature engineering function properly
def create_features(df):
    """
    Create time series features based on time series index.
    """
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

# Load the existing model (this should work)
models_path = r"F:\bda-project\models"

try:
    print("Loading existing model...")
    with open(os.path.join(models_path, 'energy_model.pkl'), 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")
    
    print("Loading model config...")
    with open(os.path.join(models_path, 'model_config.pkl'), 'rb') as f:
        config = pickle.load(f)
    print("Config loaded successfully")
    
    # Save the function with proper module context
    print("Saving feature function...")
    with open(os.path.join(models_path, 'create_features.pkl'), 'wb') as f:
        pickle.dump(create_features, f)
    print("Feature function saved successfully")
    
    print("\nAll pickle files are now fixed!")
    print(f"Model RMSE: {config['performance']['rmse']:.2f}")
    print(f"Features: {config['features']}")
    
    # Test the function
    print("\nTesting the feature function...")
    test_dates = pd.date_range('2024-01-01', periods=2, freq='H')
    test_df = pd.DataFrame({'AEP_MW': [100, 200]}, index=test_dates)
    result = create_features(test_df)
    print("Feature function test passed!")
    print(f"Generated features: {[col for col in result.columns if col != 'AEP_MW']}")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nPlease make sure to run the notebook first to generate the pickle files!")