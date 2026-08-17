# 📊 AI Data Quality Engine

An intelligent data-quality platform that automatically analyzes uploaded datasets, identifies quality issues, detects anomalies, recommends improvements, and performs automated data cleaning.

## 🎯 Problem Statement

Real-world datasets often contain missing values, duplicate records, invalid values, inconsistent data, and unusual observations.

Poor-quality data can negatively affect data analysis and machine-learning models.

The AI Data Quality Engine provides an automated workflow for assessing and improving dataset quality.

## 💡 Proposed Solution

The system allows a user to upload a CSV or Excel dataset and automatically:

1. Profile the dataset
2. Detect missing values and duplicates
3. Calculate a data-quality score
4. Apply data-validation rules
5. Detect unusual records using Machine Learning
6. Recommend appropriate data-quality actions
7. Clean common data-quality problems
8. Compare data quality before and after cleaning
9. Generate a quality report

## 🚀 Main Features

### 📂 Dataset Upload
- CSV support
- Excel support

### 🔍 Data Profiling
- Number of rows and columns
- Data types
- Missing values
- Unique values
- Duplicate records
- Numeric and categorical columns

### ⭐ Data Quality Score

The system evaluates:

- Completeness — 30%
- Uniqueness — 20%
- Validity — 30%
- Consistency — 20%

The final score is represented on a 0–100 scale.

### 🛡️ Data Validation

The rules engine can check applicable fields such as:

- Age ranges
- Salary values
- Email formats
- ID uniqueness

### 🤖 ML-Based Anomaly Detection

Isolation Forest is used to identify unusual observations in numeric data.

### 🧹 Automated Data Cleaning

The system can perform common cleaning operations such as:

- Numeric missing-value imputation
- Categorical missing-value imputation
- Duplicate removal

### 📊 Before vs After Analysis

The system compares:

- Missing values
- Duplicate records
- Quality score

before and after cleaning.

### 💡 Recommendations

The system identifies detected issues and provides suggested actions with priority levels.

### 📄 Quality Reports

Users can generate downloadable quality reports and PDF reports.

## 🏗️ System Workflow

```text
Upload Dataset
      ↓
Data Profiling
      ↓
Quality Assessment
      ↓
Validation Rules
      ↓
ML Anomaly Detection
      ↓
Recommendations
      ↓
Automated Cleaning
      ↓
Before vs After Comparison
      ↓
Quality Report