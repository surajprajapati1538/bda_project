# System Architecture for Energy Forecasting Project

## Problem Statement

**Objective:** Design and implement an intelligent energy consumption forecasting system that provides accurate predictions through multiple interfaces while maintaining scalability, reliability, and user-friendly access patterns.

**Core Challenge:** Transform time-series energy consumption data into actionable predictions using machine learning, delivered through both interactive dashboards and programmatic APIs.

## System Architecture Components

### 1. Data Layer
```
┌─────────────────────────────────────────┐
│             DATA SOURCES                │
├─────────────────────────────────────────┤
│ • AEP_hourly.csv (Historical Data)      │
│ • Time-series Energy Consumption        │
│ • Date Range: 2004-2018                 │
│ • Frequency: Hourly Measurements        │
│ • Size: ~121,000 Records                │
└─────────────────────────────────────────┘
```

### 2. Model Layer
```
┌─────────────────────────────────────────┐
│          MACHINE LEARNING CORE          │
├─────────────────────────────────────────┤
│ XGBoost Regression Engine               │
│ ├── energy_model.pkl                    │
│ ├── create_features.pkl                 │
│ └── model_config.pkl                    │
│                                         │
│ Feature Engineering Pipeline            │
│ ├── Time-based Features                 │
│ ├── Temporal Decomposition              │
│ └── Statistical Transformations         │
└─────────────────────────────────────────┘
```

### 3. Service Layer
```
┌─────────────────────────────────────────┐
│           CORE SERVICES                 │
├─────────────────────────────────────────┤
│ EnergyForecastingModel Class            │
│ ├── predict_single_datetime()           │
│ ├── predict_date_range()                │
│ ├── get_feature_importance()            │
│ └── create_features()                   │
│                                         │
│ Utility Services                        │
│ ├── Chart Generation                    │
│ ├── Data Validation                     │
│ └── Error Handling                      │
└─────────────────────────────────────────┘
```

### 4. Application Layer
```
┌─────────────────────────────────────────┐
│        WEB APPLICATIONS                 │
├─────────────────────────────────────────┤
│ Streamlit Dashboard                     │
│ ├── Interactive UI Components           │
│ ├── Real-time Predictions              │
│ ├── Data Visualization                 │
│ └── User Input Forms                   │
│                                         │
│ Flask Web Application                   │
│ ├── REST API Endpoints                 │
│ ├── Interactive Dashboard              │
│ ├── AJAX-based Updates                 │
│ └── Professional UI                    │
└─────────────────────────────────────────┘
```

### 5. Presentation Layer
```
┌─────────────────────────────────────────┐
│           USER INTERFACES               │
├─────────────────────────────────────────┤
│ Web Browser Access                      │
│ ├── Streamlit: localhost:8501          │
│ ├── Flask: localhost:5000              │
│ └── Mobile-Responsive Design           │
│                                         │
│ API Access                              │
│ ├── REST Endpoints                      │
│ ├── JSON Responses                      │
│ └── Programmatic Integration            │
└─────────────────────────────────────────┘
```

## Process Flow Steps

### Step 1: Data Ingestion and Preprocessing
1. **Load Historical Data** → AEP_hourly.csv into pandas DataFrame
2. **Data Validation** → Check for missing values, outliers, data types
3. **Time Index Creation** → Convert datetime strings to pandas datetime index
4. **Data Cleaning** → Handle missing values and anomalies

### Step 2: Feature Engineering Pipeline
1. **Temporal Feature Extraction**
   - Hour of day (0-23)
   - Day of week (0-6)
   - Month of year (1-12)
   - Day of year (1-365)
   - Quarter (1-4)
   - Week of year (1-52)

2. **Feature Transformation**
   - Cyclical encoding for temporal features
   - Statistical aggregations
   - Lag feature creation

3. **Feature Selection**
   - Correlation analysis
   - Feature importance ranking
   - Dimensionality optimization

### Step 3: Model Training and Validation
1. **Data Splitting**
   - Training set: 80%
   - Validation set: 20%
   - Time-based splitting

2. **Model Training**
   - XGBoost hyperparameter tuning
   - Cross-validation
   - Performance optimization

3. **Model Serialization**
   - Save trained model → energy_model.pkl
   - Save feature pipeline → create_features.pkl
   - Save configuration → model_config.pkl

### Step 4: Service Layer Implementation
1. **Model Loading**
   - Deserialize pickle files
   - Initialize prediction service
   - Validate model integrity

2. **Prediction Services**
   - Single datetime prediction
   - Date range batch prediction
   - Feature importance analysis
   - Pattern analysis

3. **Utility Services**
   - Chart generation (matplotlib/seaborn)
   - Data validation
   - Error handling and logging

### Step 5: Web Application Development

#### Streamlit Application Flow:
1. **User Interface Rendering**
   - Tab-based navigation
   - Input form components
   - Interactive widgets

2. **User Input Processing**
   - Form data validation
   - DateTime parsing
   - Parameter extraction

3. **Model Invocation**
   - Service layer calls
   - Prediction generation
   - Result formatting

4. **Results Display**
   - Metric visualization
   - Chart rendering
   - Data tables

#### Flask Application Flow:
1. **Route Handling**
   - Dashboard route (/)
   - API endpoint routing
   - Template rendering

2. **Request Processing**
   - JSON payload parsing
   - Input validation
   - Error handling

3. **Service Integration**
   - Model service calls
   - Data transformation
   - Response formatting

4. **Response Generation**
   - JSON API responses
   - Chart base64 encoding
   - Error message handling

### Step 6: User Interaction Flow

#### Single Prediction Workflow:
```
User Input → Date/Time Selection → Validation → 
Feature Engineering → Model Prediction → 
Chart Generation → Result Display
```

#### Range Prediction Workflow:
```
User Input → Date Range + Frequency → Validation → 
Batch Feature Engineering → Batch Prediction → 
Statistical Analysis → Chart Generation → 
Summary Display
```

#### Pattern Analysis Workflow:
```
User Input → Analysis Parameters → Data Aggregation → 
Pattern Detection → Visualization → Insights Display
```

## System Integration Points

### 1. Data Flow Integration
- **CSV → DataFrame → Features → Model → Predictions**
- **Bidirectional data transformation between layers**

### 2. Service Integration
- **Model services ↔ Web applications**
- **Shared utility functions across applications**

### 3. API Integration
- **REST endpoints for external system integration**
- **JSON-based data exchange**

### 4. User Interface Integration
- **Multiple access patterns (interactive vs. programmatic)**
- **Consistent user experience across interfaces**

## Deployment Architecture

### Development Environment
```
Local Machine → Virtual Environment → Python Services → 
Web Browser Access
```

### Production Considerations
```
Container Orchestration → Load Balancer → 
Application Servers → Database Layer → 
Monitoring & Logging
```

## Quality Attributes

### Performance
- **Response Time:** < 2 seconds for single predictions
- **Throughput:** 100+ predictions per minute
- **Scalability:** Horizontal scaling ready

### Reliability
- **Availability:** 99.9% uptime target
- **Error Handling:** Graceful degradation
- **Data Validation:** Input sanitization

### Security
- **Input Validation:** SQL injection prevention
- **Error Masking:** Sensitive information protection
- **CORS:** Cross-origin request handling

### Maintainability
- **Modular Design:** Loosely coupled components
- **Documentation:** Comprehensive API docs
- **Version Control:** Git-based development workflow

This architecture provides a clear foundation for creating system diagrams with distinct layers, clear data flows, and well-defined integration points.