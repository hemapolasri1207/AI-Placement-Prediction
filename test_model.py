import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import joblib
import pandas as pd

# Load model and metadata
model = joblib.load("models/placement_model.pkl")
metadata = joblib.load("models/model_metadata.pkl")

# Example student details
student = {
    "CGPA": 8.2,
    "Internships": 2,
    "Projects": 3,
    "Workshops/Certifications": 2,
    "AptitudeTestScore": 85,
    "SoftSkillsRating": 4.5,
    "ExtracurricularActivities": "Yes",
    "PlacementTraining": "Yes",
    "SSC_Marks": 80,
    "HSC_Marks": 82
}

# Create input using the exact dataset feature order
student_df = pd.DataFrame(
    [student],
    columns=metadata["feature_columns"]
)

# Predict placement status
prediction = model.predict(student_df)

print("\n========== STUDENT PLACEMENT PREDICTION ==========")
print("Predicted Placement Status:", prediction[0])