import pandas as pd 
import numpy as np 
import os 
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from xgboost import XGBRegressor


def run_regression(input_path, output_dir):
    """Goal -> bought in last month  """

    df = pd.read_csv(input_path)

    os.makedirs(output_dir, exist_ok=True)

    features = ["rating", "number_of_reviews", "current/discounted_price", "listed_price", "discount", "is_best_seller", "is_couponed", "is_sponsored"]
    target = "bought_in_last_month"

    data = df[features + [target]].dropna()

    X = data[features]
    y = data[target]
    
    results = []

    # train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Linear Regression (baseline)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    results["Linear Regression"] = {
        "RMSE": np.sqrt(mse),  
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred)
    }
    joblib.dump(linreg, f"{output_dir}/linear_regression.pkl")


    # Random Forest 
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    results["Random Forest"] = {
        "RMSE": np.sqrt(mse),  
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred)
    }
    joblib.dump(rf, f"{output_dir}/random_forest.pkl")
    

    # XGBoost 
    xgb = XGBRegressor(n_estimators=300, learning_rate=0.1, random_state=42)
    xgb.fit(X_train, y_train)
    y_pred = xgb.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    results["XGBoost"] = {
        "RMSE": np.sqrt(mse),  
        "MAE": mean_absolute_error(y_test, y_pred),
        "R2": r2_score(y_test, y_pred)
    }
    joblib.dump(xgb, f"{output_dir}/xgboost.pkl")



    # Save results
    results_df = pd.DataFrame(results).T
    results_df.to_csv(f"{output_dir}/regression_metrics.csv")

    print("✅ Regression models trained and results saved")
    print(results_df)




















