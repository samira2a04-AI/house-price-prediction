# 🏙️ PropIQ • Real Estate AI

**AI-Powered House Price Prediction for the USA**

An end-to-end machine learning project that predicts real estate prices using a rich USA housing dataset (483K+ listings). Includes extensive data preprocessing, feature engineering, model training, and a beautiful **Streamlit web application** for instant valuations.

![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![XGBoost/LightGBM](https://img.shields.io/badge/Model-XGBoost%20%7C%20LightGBM-orange?style=for-the-badge)

## ✨ Features

- **Robust Data Pipeline**: Cleaning, hierarchical imputation, outlier handling, and feature engineering
- **Advanced Modeling**: Tree-based models (XGBoost / LightGBM) with Group K-Fold validation by ZIP code
- **Rich Feature Set**: Property attributes + location intelligence + engineered features (luxury score, density, ratios, etc.)
- **Interactive Web App**: Modern, dark-luxury UI for instant price predictions
- **High Coverage**: 99.85% of U.S. ZIP codes supported

## 📊 Model Performance

| Metric          | Value     | Description                  |
|-----------------|-----------|------------------------------|
| R² Score        | 0.82      | Excellent fit                |
| MAE             | ~$92K     | Mean Absolute Error          |
| Dataset Size    | 483K+     | Training listings            |
| ZIP Coverage    | 99.85%    | U.S. coverage                |

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/samira2a04-AI/house-price-prediction.git
cd house-price-prediction
