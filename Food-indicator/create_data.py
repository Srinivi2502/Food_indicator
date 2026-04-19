import pandas as pd
import numpy as np

np.random.seed(42)
data_size = 2000 # Increased to 2000 for better variety

data = {
    'Rainfall_mm': np.random.randint(200, 2000, data_size),
    'Crop_Yield_MT': np.random.uniform(1, 10, data_size),
    'Food_Price_Index': np.random.randint(80, 280, data_size),
    'Population_Density': np.random.randint(50, 600, data_size)
}

df = pd.DataFrame(data)

def calculate_balanced_risk(row):
    # Score formula: Higher = More Risk
    score = (
        (row['Food_Price_Index'] * 0.4) + 
        (row['Population_Density'] * 0.3) - 
        (row['Rainfall_mm'] * 0.08) - # Reduced weight slightly
        (row['Crop_Yield_MT'] * 4)
    )
    
    # NEW BALANCED THRESHOLDS
    if score > 85:
        return 'High Risk'
    elif 30 <= score <= 85: # Wider range for Moderate
        return 'Moderate Risk'
    else:
        return 'Low Risk'

df['Risk_Level'] = df.apply(calculate_balanced_risk, axis=1)
df.to_csv('food_security_data.csv', index=False)

print("Balanced Dataset Created!")
print(df['Risk_Level'].value_counts()) # Ensure you see 'Moderate Risk' here!