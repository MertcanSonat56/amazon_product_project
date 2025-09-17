import pandas as pd 
import seaborn as sns 
#import logging
#logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import matplotlib.pyplot as plt 
import os 


def run_eda(input_path, output_dir):
    df = pd.read_csv(input_path)

    os.makedirs(output_dir, exist_ok=True)

    # Histograms
    features = ["rating", "current/discounted_price", "listed_price", "bought_in_last_month"]
    for col in features:
        if col in df.columns:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[col].dropna(), bins=30, kde=True)
            
            plt.title(f"Distribution of {col}")
            plt.savefig(f"{output_dir}/{col}_hist.png")
            plt.close()


     # 2. Correlation Heatmap
    numeric_cols = ["rating", "number_of_reviews", "current/discounted_price","listed_price", "bought_in_last_month"]
    corr = df[numeric_cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    
    plt.title("Correlation Heatmap")
    plt.savefig(f"{output_dir}/correlation_heatmap.png")
    plt.close()

    # 3. Best Seller Distribution
    if "is_best_seller" in df.columns:
        plt.figure(figsize=(6, 4))
        sns.countplot(x="is_best_seller", data=df)
        
        plt.title("Best Seller vs Non-Best Seller")
        plt.savefig(f"{output_dir}/best_seller_distribution.png")
  
    print(f"EDA plots saved in {output_dir}")










