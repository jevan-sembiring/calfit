import joblib
import os
import pandas as pd

class ObesityModelWrapper:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "obesity_model.pkl")
        self.pipeline = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            raise FileNotFoundError("File obesity_model.pkl tidak ditemukan!")

    def predict(self, age: int, gender: str, height_cm: float, weight_kg: float) -> str:
        height_m = height_cm / 100.0 
        
        input_data = pd.DataFrame([{
            'Age': age,
            'Gender': gender,
            'Height': height_m,
            'Weight': weight_kg
        }])
        
        prediction = self.pipeline.predict(input_data)
        return prediction[0]