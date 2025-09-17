import numpy as np
import pandas as pd 
import re




def clean_numeric(text):
    if pd.isna(text):
        return np.nan
    
    text = str(text).replace(",","")

    if "K" in text:
        return int(float(text.replace("K","").replace("+", "")) * 100)
    elif "M" in text:
        return int(float(text.replace("M", "").replace("+", "") * 1000000))

    return pd.to_numeric(re.sub(r"[^0-9.]", "", text), errors="coerce")


def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # clean rating 
    df["rating"] = df["rating"].str.extract(r"([0-9.]+)").astype(float)
    
    # clean reviews & sales 
    df["number_of_reviews"] = df["number_of_reviews"].apply(clean_numeric)
    df["bought_in_last_mounth"] = df["bought_in_last_mounth"].apply(clean_numeric)

    # prices
    for col in ["current/discounted_price", "listed_price"]:
        df[col] = df[col].astype(str).str.replace(r"[^0-9.]", "", regex = True)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # boolean features
    df["is_best_seller"] = df["is_best_seller"].apply(lambda x: 1 if "Best Seller" in str(x) else 0)
    df["is_sponsored"] = df["is_sponsored"].apply(lambda x: 1 if "Sponsored" in str(x) else 0)
    df["is_couponed"] = df["is_couponed"].apply(lambda x: 1 if "Coupon" in str(x) else 0)

    # discount feature 
    df["discount"] = df["listed_price"] - df["current/discounted_price"]

    df.to_csv(output_path, index=False)
    print(f"Data preprocessed and saved to {output_path}")

