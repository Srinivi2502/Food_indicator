import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load the balanced data
try:
    df = pd.read_csv('food_security_data.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: food_security_data.csv not found. Run create_data.py first.")
    exit()

# 2. Separate Features (X) and Target (y)
X = df[['Rainfall_mm', 'Crop_Yield_MT', 'Food_Price_Index', 'Population_Density']]
y = df['Risk_Level']

# 3. Split the data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train the Model
# We use 200 trees and 'balanced' class weight to help the AI learn 'Moderate' better
model = RandomForestClassifier(
    n_estimators=200, 
    random_state=42, 
    class_weight='balanced'
)

print("Training the AI model...")
model.fit(X_train, y_train)

# 5. Evaluate the Model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\n" + "="*30)
print(f"MODEL ACCURACY: {accuracy * 100:.2f}%")
print("="*30)

# This report shows if 'Moderate' is being predicted correctly
print("\nDetailed Performance Report:")
print(classification_report(y_test, predictions))

# 6. Save the Model
joblib.dump(model, 'model.pkl')
print("\nModel saved as 'model.pkl'!")