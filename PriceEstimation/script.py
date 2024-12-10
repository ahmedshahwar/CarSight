import pickle
import pandas as pd
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import lightgbm as lgbm
from pathlib import Path

script_dir = Path(__file__).resolve().parent

# Load models and preprocessor
with open(str(script_dir/'preprocessor.pkl'), 'rb') as f:
    preprocessor = pickle.load(f)

model_xgb = xgb.Booster()
model_xgb.load_model(str(script_dir/'xgb.booster'))

model_lgbm = lgbm.Booster(model_file=str(script_dir/'lgbm.booster'))

# Make DataFrame of all features
def dataframe(make, model, variant, year, mileage, engine_cc, engine_type, transmission, reg_city):
    data = {'Make': [make],
            'Model': [model],
            'Variant': [variant],
            'Year': [year],
            'Mileage': [mileage],
            'Engine Capacity': [engine_cc],
            'Engine Type': [engine_type],
            'Transmission': [transmission],
            'Registered City': [reg_city]}
    df = pd.DataFrame(data)
    return df

# Pipeline to Predict Result
def piepline(make, model, variant, year, mileage, engine_cc, engine_type, transmission, reg_city):
    df = dataframe(make, model, variant, year, mileage, engine_cc, engine_type, transmission, reg_city)
    processed = preprocessor.transform(df)
    dM = xgb.DMatrix(processed)
    pred_xgb = model_xgb.predict(dM)
    pred_lgb = model_lgbm.predict(processed)

    return int((pred_xgb + pred_lgb) / 2)
