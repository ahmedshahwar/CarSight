# CarSight 🚗💡  
**Used Cars Price and Model Assessment in the Pakistani Market**

CarSight is an intelligent mobile application designed to transform the used car market in Pakistan by utilizing cutting-edge machine learning and image recognition technologies. The project provides accurate price assessments by analyzing vehicle characteristics and market trends, addressing inconsistencies and subjectivity in traditional pricing methods.

---

## Table of Contents  
- [Features](#features-🌟)  
- [Technology Stack](#technology-stack-🛠️)  
- [Dataset](#dataset-📊)  
- [Model Performance](#model-performance-📈)  
- [Installation and Setup](#installation-and-setup-🚀)  
- [Demo Video](#demo-video-🎥)  
- [Future Scope](#future-scope-🔮)  
- [Contact](#contact-📧)  
 

---

## Features 🌟  
1. **Image-Based Vehicle Identification**  
   - Uses YOLOv8 to identify a vehicle’s make, model, variant, year, and condition from uploaded images.  
2. **Odometer Reading Detection**  
   - Utilizes EasyOCR integrated with YOLOv8 for accurate mileage extraction.  
3. **Localized Price Estimation**  
   - Employs XGBoost and LightGBM models tailored for the Pakistani market, achieving high accuracy in price prediction.  
4. **Damage Detection**  
   - Identifies scratches, dents, and other damages on vehicles for a comprehensive assessment.  
5. **User-Friendly Interface**  
   - Provides a seamless experience for uploading images, viewing vehicle details, and obtaining instant price estimates.

---

## Technology Stack 🛠️  

### Frontend  
- **Flutter**: Cross-platform development for Android and iOS.  

### Backend  
- **Flask**: API for seamless integration with machine learning models.  
- **AWS**: Hosting backend services for scalability and reliability.  

### Machine Learning  
- **YOLOv8**: Vehicle identification, odometer detection, and damage assessment.  
- **EasyOCR**: Text extraction for odometer readings.  
- **XGBoost & LightGBM**: Price prediction based on car details and market trends.  

---

## Dataset 📊  
- **Vehicle Identification**: 12,000 images for make, model, variant, and year detection.  
- **Odometer Region Detection**: 1,250 images for mileage extraction.  
- **Damage Detection**: 9,500 images for identifying vehicle damage.  
- **Price Prediction**: 21,000 records, including car specifications, historical prices, and market data.  

---

## Model Performance 📈  

### Vehicle Identification  
- **Precision**: 90%  
- **mAP@0.5**: 94.9%  

### Odometer Detection  
- **Precision**: 94%  
- **mAP@0.5**: 94.9%  

### Damage Detection  
- **Precision**: 93.4%  
- **mAP@0.5**: 90.5%  

### Price Prediction  
- **XGBoost R-Squared**: 0.98  
- **Mean Absolute Error (MAE)**: Lowest in all tests.  

---

## Installation and Setup 🚀  

### Prerequisites  
- Python 3.8+  
- Node.js (for Flutter)  
- Firebase CLI  

### Step 1: Clone the Repository  
```bash
git clone https://github.com/ahmedshahwar/carsight.git  
cd carsight
```
### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```
### Step 3: Run the app
```bash
python app.py
```

---

## Demo Video 🎥  
Watch the demonstration of CarSight in action:  
[Click here to view the demo video](https://drive.google.com/drive/u/1/folders/1tVvnyqa0YtbSb-fnXsxFLUWdl9gbjuSq)

---

## Future Scope 🔮  
- **Market Demand Analysis**: Incorporate real-time demand and supply trends.  
- **Integration**: Collaborate with financing, insurance, and maintenance services.  
- **Expanded Features**: Include real-time pricing updates and market statistics.  

---

## Contact 📧  
For questions or contributions, reach out:  
- **Ahmed Shahwar**: ahmedshahwarr@gmail.com  
- **Aymen Zahid**: aymenzahid12@gmail.com  

---

### 🚀 Redefining the Used Car Market in Pakistan with AI! 
