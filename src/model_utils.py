import os
import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = os.path.join("models", "placement_model.pkl")
METADATA_PATH = os.path.join("models", "model_metadata.pkl")


@st.cache_resource(show_spinner=False)
def load_model_and_metadata():
    """
    Loads the trained Random Forest pipeline and metadata from the models directory.
    Uses st.cache_resource to avoid redundant file I/O on every rerun.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Metadata file not found at: {METADATA_PATH}")

    model = joblib.load(MODEL_PATH)
    metadata = joblib.load(METADATA_PATH)
    return model, metadata


def validate_student_inputs(student_data: dict) -> tuple[bool, list[str]]:
    """
    Validates student inputs against acceptable domain boundaries.
    Returns (is_valid, list_of_error_messages).
    """
    errors = []

    # CGPA check
    cgpa = student_data.get("CGPA")
    if cgpa is None or not (0.0 <= float(cgpa) <= 10.0):
        errors.append("CGPA must be between 0.0 and 10.0.")

    # SSC Marks
    ssc = student_data.get("SSC_Marks")
    if ssc is None or not (0 <= float(ssc) <= 100):
        errors.append("10th (SSC) Marks percentage must be between 0 and 100%.")

    # HSC Marks
    hsc = student_data.get("HSC_Marks")
    if hsc is None or not (0 <= float(hsc) <= 100):
        errors.append("12th (HSC) Marks percentage must be between 0 and 100%.")

    # Aptitude Score
    aptitude = student_data.get("AptitudeTestScore")
    if aptitude is None or not (0 <= float(aptitude) <= 100):
        errors.append("Aptitude Test Score must be between 0 and 100.")

    # Soft Skills Rating
    soft_skills = student_data.get("SoftSkillsRating")
    if soft_skills is None or not (1.0 <= float(soft_skills) <= 5.0):
        errors.append("Soft Skills Rating must be between 1.0 and 5.0.")

    # Count fields
    for field in ["Internships", "Projects", "Workshops/Certifications"]:
        val = student_data.get(field)
        if val is None or int(val) < 0:
            errors.append(f"{field} count cannot be negative.")

    # Categorical fields
    for field in ["ExtracurricularActivities", "PlacementTraining"]:
        val = student_data.get(field)
        if val not in ["Yes", "No"]:
            errors.append(f"{field} must be either 'Yes' or 'No'.")

    return (len(errors) == 0, errors)


def predict_placement(student_data: dict) -> dict:
    """
    Predicts student placement status using the existing trained model pipeline.
    Ensures input features strictly adhere to metadata['feature_columns'].
    """
    model, metadata = load_model_and_metadata()
    feature_cols = metadata["feature_columns"]

    # Verify all expected columns are present
    missing_cols = [col for col in feature_cols if col not in student_data]
    if missing_cols:
        raise ValueError(f"Missing required feature inputs: {missing_cols}")

    # Prepare DataFrame matching exact column names and ordering
    input_df = pd.DataFrame([student_data], columns=feature_cols)

    # Cast to proper data types
    numeric_cols = [
        "CGPA",
        "Internships",
        "Projects",
        "Workshops/Certifications",
        "AptitudeTestScore",
        "SoftSkillsRating",
        "SSC_Marks",
        "HSC_Marks",
    ]
    for col in numeric_cols:
        if col in input_df.columns:
            input_df[col] = pd.to_numeric(input_df[col], errors="coerce")

    # Execute prediction
    prediction_label = model.predict(input_df)[0]

    # Predict probabilities if supported
    probabilities = {}
    placed_prob = 0.0
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        classes = list(model.classes_)
        for cls_name, prob in zip(classes, probs):
            probabilities[str(cls_name)] = round(float(prob) * 100, 2)
        placed_prob = probabilities.get("Placed", 0.0)
    else:
        placed_prob = 100.0 if str(prediction_label).lower() == "placed" else 0.0
        probabilities = {str(prediction_label): 100.0}

    is_placed = str(prediction_label).strip().lower() == "placed"

    return {
        "prediction": str(prediction_label).strip(),
        "is_placed": is_placed,
        "placement_probability": placed_prob,
        "probabilities": probabilities,
        "input_features": student_data,
        "accuracy": metadata.get("accuracy", 0.7919),
    }


@st.cache_data(show_spinner=False)
def get_feature_importances() -> pd.DataFrame:
    """
    Extracts and ranks feature importances from the trained Random Forest pipeline.
    """
    model, _ = load_model_and_metadata()
    try:
        raw_names = model.named_steps["preprocessor"].get_feature_names_out()
        importances = model.named_steps["classifier"].feature_importances_

        # Clean names for user-friendly presentation
        clean_names = []
        for name in raw_names:
            name = name.replace("numeric__", "").replace("categorical__", "")
            name = name.replace("_Yes", " (Yes)").replace("_No", " (No)")
            name = name.replace("Workshops/Certifications", "Workshops / Certs")
            name = name.replace("AptitudeTestScore", "Aptitude Score")
            name = name.replace("SoftSkillsRating", "Soft Skills Rating")
            name = name.replace("ExtracurricularActivities", "Extracurricular")
            name = name.replace("PlacementTraining", "Placement Training")
            clean_names.append(name)

        df_imp = pd.DataFrame(
            {"Feature": clean_names, "Importance": importances}
        )
        df_imp = df_imp.sort_values(by="Importance", ascending=False).reset_index(
            drop=True
        )
        return df_imp
    except Exception:
        return pd.DataFrame()
