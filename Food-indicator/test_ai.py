import joblib
import pandas as pd

# Load the brain
model = joblib.load('model.pkl')

# Create a fake "High Risk" scenario: 
# Low Rainfall (200), Low Yield (1), High Price (250), High Pop (500)
sample_data = pd.DataFrame([[200, 1, 250, 500]], 
                           columns=['Rainfall_mm', 'Crop_Yield_MT', 'Food_Price_Index', 'Population_Density'])

prediction = model.predict(sample_data)
print(f"The AI predicts this region is: {prediction[0]}")