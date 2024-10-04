# 🎉 Celebrity Face Detection using CNN

Welcome to the **Celebrity Face Detection** project! This repository contains a complete pipeline for detecting celebrity faces using Convolutional Neural Networks (CNN). The project involves web scraping, data preprocessing, augmentation, exploratory data analysis (EDA), and training a CNN model.

## 🚀 Table of Contents
- [🔍 Overview](#-overview)
- [💻 File Structure](#-file-structure)
- [🛠 Installation](#-installation)
- [📂 Workflow](#-workflow)
- [📈 Model Performance](#-model-performance)

## 🔍 Overview
This project aims to create a robust face detection model that can identify various celebrities. The approach includes:
- Web scraping to collect celebrity images.
- Data cleaning, including converting images to grayscale and cropping.
- Data augmentation to improve model robustness.
- Addressing class imbalance using SMOTE.
- Training a CNN model for face detection.

## 💻 File Structure
```plaintext
Model
├── data_cleaning.py           # Script for cleaning data (grayscale & cropping)
├── downloading_images.py       # Script for web scraping celebrity images
├── augment_dataset.py          # Script for augmenting the dataset
├── eda.py                      # Script for exploratory data analysis
├── handle_ClassImbalance.py    # Script for handling class imbalance using SMOTE
├── split_data.py               # Script for splitting data into training and testing sets
└── train_model.py              # Script for training the CNN model
Web Scrapping
├── downloading_images.py       # Script for training the CNN model
└── README.md                   # Project documentation
```

## 📂 Workflow
Web Scraping: Use downloading_images.py to scrape images of celebrities from the web.

Data Cleaning: Run data_cleaning.py to convert images to grayscale and crop them based on detected eyes.

Data Augmentation: Execute augment_dataset.py to apply various augmentations to the images for enhancing the dataset.

Exploratory Data Analysis: Perform EDA in eda.py to understand the dataset and identify class imbalances.

Handle Class Imbalance: Use handle_ClassImbalance.py to apply SMOTE and create a balanced dataset.

Split Data: Split the dataset into training and testing sets using split_data.py.

Train Model: Train the CNN model using train_model.py and save the model.

## 📈 Model Performance
After training the model, we achieved a test accuracy of 80.45%. This indicates a strong ability to classify celebrity faces accurately.
```plaintext
Classification Report:
              precision    recall  f1-score   support

ArianaGrande       0.90      0.72      0.80        39
     Beyonce       0.82      0.79      0.81        39
   BrunoMars       0.76      0.79      0.78        39
   EdSheeran       0.73      0.82      0.77        39
 SalenaGomez       0.88      0.77      0.82        39
 ShawnMendes       0.74      0.87      0.80        39
 TaylorSwift       0.81      0.87      0.84        39
   ZyanMalik       0.86      0.79      0.83        39

    accuracy                           0.80       312
   macro avg       0.81      0.80      0.80       312
weighted avg       0.81      0.80      0.80       312
```
