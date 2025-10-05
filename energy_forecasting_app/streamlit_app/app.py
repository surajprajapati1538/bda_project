"""
Energy Forecasting Streamlit Application
Interactive web app for energy consumption forecasting
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import sys
import os

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from model_utils import EnergyForecastingModel, create_prediction_chart, create_feature_importance_chart, create_hourly_pattern_chart, create_weekly_pattern_chart

# Page configuration
st.set_page_config(
    page_title="Energy Forecasting Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stSelectbox label {
        font-weight: bold;
    }
    .stDateInput label {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load the energy forecasting model"""
    try:
        model = EnergyForecastingModel()
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">Energy Forecasting Dashboard</h1>', unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    if model is None:
        st.error("Failed to load the forecasting model. Please check if model files exist.")
        return
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Single Prediction", "Date Range Prediction", "Analysis", "Feature Importance"])
    
    with tab1:
        st.header("Single DateTime Prediction")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # DateTime input
            selected_date = st.date_input(
                "Select Date:",
                value=datetime.now().date(),
                min_value=datetime(2020, 1, 1).date(),
                max_value=datetime(2030, 12, 31).date()
            )
            
            selected_time = st.time_input(
                "Select Time:",
                value=datetime.now().time()
            )
            
            # Combine date and time
            selected_datetime = datetime.combine(selected_date, selected_time)
            
            if st.button("Make Prediction", type="primary"):
                with st.spinner("Making prediction..."):
                    result = model.predict_single_datetime(selected_datetime.strftime('%Y-%m-%d %H:%M:%S'))
                    
                    if result:
                        st.success("Prediction completed!")
                        
                        # Display prediction
                        st.metric(
                            "Predicted Energy Consumption",
                            f"{result['prediction']:.2f} MW",
                            delta=None
                        )
                        
                        # Display features used
                        with st.expander("View Feature Values"):
                            feature_df = pd.DataFrame([result['features']])
                            st.dataframe(feature_df, use_container_width=True)
                    else:
                        st.error("Failed to make prediction")
        
        with col2:
            st.info("""
            **How to use:**
            1. Select a date and time
            2. Click 'Make Prediction'
            3. View the predicted energy consumption
            
            The model uses time-based features like hour, day of week, month, etc.
            """)
    
    with tab2:
        st.header("Date Range Prediction")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            start_date = st.date_input(
                "Start Date:",
                value=datetime.now().date(),
                key="start_date"
            )
        
        with col2:
            end_date = st.date_input(
                "End Date:",
                value=(datetime.now() + timedelta(days=7)).date(),
                key="end_date"
            )
        
        with col3:
            frequency = st.selectbox(
                "Frequency:",
                options=['H', 'D', '6H', '12H'],
                format_func=lambda x: {'H': 'Hourly', 'D': 'Daily', '6H': '6 Hours', '12H': '12 Hours'}[x],
                index=0
            )
        
        if start_date <= end_date:
            if st.button("Generate Predictions", type="primary", key="range_predict"):
                with st.spinner("Generating predictions..."):
                    result_df = model.predict_date_range(start_date, end_date, freq=frequency)
                    
                    if result_df is not None and not result_df.empty:
                        st.success(f"Generated {len(result_df)} predictions!")
                        
                        # Create and display chart
                        fig = create_prediction_chart(
                            result_df, 
                            title=f"Energy Consumption Prediction ({start_date} to {end_date})"
                        )
                        st.pyplot(fig)
                        
                        # Summary statistics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Average", f"{result_df['prediction'].mean():.2f} MW")
                        with col2:
                            st.metric("Maximum", f"{result_df['prediction'].max():.2f} MW")
                        with col3:
                            st.metric("Minimum", f"{result_df['prediction'].min():.2f} MW")
                        with col4:
                            st.metric("Std Dev", f"{result_df['prediction'].std():.2f} MW")
                        
                        # Download predictions
                        csv = result_df[['prediction']].to_csv()
                        st.download_button(
                            label="Download Predictions as CSV",
                            data=csv,
                            file_name=f'energy_predictions_{start_date}_to_{end_date}.csv',
                            mime='text/csv'
                        )
                        
                        # Show data table
                        with st.expander("View Prediction Data"):
                            st.dataframe(result_df[['prediction']], use_container_width=True)
                    else:
                        st.error("Failed to generate predictions")
        else:
            st.error("End date must be after start date")
    
    with tab3:
        st.header("Pattern Analysis")
        
        # Generate sample data for analysis
        analysis_start = st.date_input(
            "Analysis Start Date:",
            value=(datetime.now() - timedelta(days=30)).date(),
            key="analysis_start"
        )
        
        analysis_end = st.date_input(
            "Analysis End Date:",
            value=datetime.now().date(),
            key="analysis_end"
        )
        
        if st.button("Generate Analysis", type="primary"):
            with st.spinner("Generating analysis..."):
                # Generate hourly predictions for analysis period
                analysis_df = model.predict_date_range(analysis_start, analysis_end, freq='H')
                
                if analysis_df is not None and not analysis_df.empty:
                    # Hourly pattern
                    st.subheader("Hourly Usage Pattern")
                    hourly_fig = create_hourly_pattern_chart(analysis_df)
                    st.pyplot(hourly_fig)
                    
                    # Weekly pattern
                    st.subheader("Weekly Usage Pattern")
                    weekly_fig = create_weekly_pattern_chart(analysis_df)
                    st.pyplot(weekly_fig)
                    
                    # Time series
                    st.subheader("Time Series View")
                    time_fig = create_prediction_chart(
                        analysis_df, 
                        title=f"Energy Consumption Pattern ({analysis_start} to {analysis_end})"
                    )
                    st.pyplot(time_fig)
                else:
                    st.error("Failed to generate analysis")
    
    with tab4:
        st.header("Feature Importance")
        
        # Get feature importance
        feature_importance = model.get_feature_importance()
        
        # Create chart
        importance_fig = create_feature_importance_chart(feature_importance)
        st.pyplot(importance_fig)
        
        # Feature importance table
        st.subheader("Feature Importance Values")
        importance_df = pd.DataFrame([
            {"Feature": feature, "Importance": importance}
            for feature, importance in feature_importance.items()
        ]).sort_values("Importance", ascending=False)
        
        st.dataframe(importance_df, use_container_width=True)
        
        # Feature explanations
        st.subheader("Feature Explanations")
        feature_explanations = {
            'hour': 'Hour of the day (0-23)',
            'dayofweek': 'Day of the week (0=Monday, 6=Sunday)',
            'month': 'Month of the year (1-12)',
            'quarter': 'Quarter of the year (1-4)',
            'year': 'Year',
            'dayofyear': 'Day of the year (1-365)',
            'weekofyear': 'Week of the year (1-53)',
            'dayofmonth': 'Day of the month (1-31)'
        }
        
        for feature, explanation in feature_explanations.items():
            if feature in feature_importance:
                st.write(f"**{feature}**: {explanation}")

if __name__ == "__main__":
    main()