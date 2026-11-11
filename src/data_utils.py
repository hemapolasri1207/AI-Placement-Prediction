import os
import pandas as pd
import streamlit as st

DATASET_PATH = os.path.join("dataset", "placement.csv")


@st.cache_data(show_spinner=False)
def load_placement_dataset() -> pd.DataFrame:
    """
    Loads and cleans the placement historical dataset.
    """
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset file not found at: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    df.columns = df.columns.astype(str).str.strip()
    return df


@st.cache_data(show_spinner=False)
def get_dataset_summary() -> dict:
    """
    Computes key statistical metrics from the placement dataset.
    """
    df = load_placement_dataset()
    total = len(df)
    placed_df = df[df["PlacementStatus"] == "Placed"]
    not_placed_df = df[df["PlacementStatus"] == "NotPlaced"]

    placed_count = len(placed_df)
    not_placed_count = len(not_placed_df)
    placement_rate = (placed_count / total * 100) if total > 0 else 0.0

    return {
        "total_students": total,
        "placed_count": placed_count,
        "not_placed_count": not_placed_count,
        "placement_rate": round(placement_rate, 2),
        "avg_cgpa": round(float(df["CGPA"].mean()), 2),
        "placed_avg_cgpa": round(float(placed_df["CGPA"].mean()), 2) if not placed_df.empty else 0.0,
        "not_placed_avg_cgpa": round(float(not_placed_df["CGPA"].mean()), 2) if not not_placed_df.empty else 0.0,
        "avg_aptitude": round(float(df["AptitudeTestScore"].mean()), 1),
        "placed_avg_aptitude": round(float(placed_df["AptitudeTestScore"].mean()), 1) if not placed_df.empty else 0.0,
        "not_placed_avg_aptitude": round(float(not_placed_df["AptitudeTestScore"].mean()), 1) if not not_placed_df.empty else 0.0,
        "avg_soft_skills": round(float(df["SoftSkillsRating"].mean()), 2),
        "avg_ssc": round(float(df["SSC_Marks"].mean()), 1),
        "avg_hsc": round(float(df["HSC_Marks"].mean()), 1),
        "avg_internships": round(float(df["Internships"].mean()), 2),
        "avg_projects": round(float(df["Projects"].mean()), 2),
    }


@st.cache_data(show_spinner=False)
def get_cohort_analysis(dimension: str = "CGPA Ranges") -> pd.DataFrame:
    """
    Groups the 7,225 student dataset records into comparative cohorts based on
    the selected dimension and computes detailed academic and placement metrics.
    """
    df = load_placement_dataset().copy()

    col_name = "Cohort_Group"
    if dimension == "CGPA Ranges":
        df[col_name] = pd.cut(
            df["CGPA"],
            bins=[0, 7.0, 7.5, 8.0, 8.5, 10.0],
            labels=["< 7.0 (Pass / Second Class)", "7.0 - 7.49 (First Class)", "7.5 - 7.99 (Distinction Entry)", "8.0 - 8.49 (High Distinction)", "8.5+ (Merit Cohort)"],
        )
    elif dimension == "Internships Completed":
        df[col_name] = df["Internships"].apply(lambda x: f"{x} Internship{'s' if x != 1 else ''}")
    elif dimension == "Technical Projects":
        df[col_name] = df["Projects"].apply(lambda x: f"{x} Technical Project{'s' if x != 1 else ''}")
    elif dimension == "Placement Training":
        df[col_name] = df["PlacementTraining"].apply(lambda x: "Attended Training (Yes)" if str(x).strip().lower() == "yes" else "Did Not Attend (No)")
    elif dimension == "Aptitude Score Tiers":
        df[col_name] = pd.cut(
            df["AptitudeTestScore"],
            bins=[0, 70, 78, 85, 100],
            labels=["< 70 Marks (Developing)", "70 - 77 Marks (Average)", "78 - 84 Marks (Proficient)", "85+ Marks (Exemplary)"],
        )
    elif dimension == "Workshops & Certifications":
        df[col_name] = df["Workshops/Certifications"].apply(lambda x: f"{x} Workshop / Cert{'s' if x != 1 else ''}")
    else:
        df[col_name] = df["PlacementStatus"]

    rows = []
    total_records = len(df)
    for cohort_val, group in df.groupby(col_name, observed=False):
        cohort_count = len(group)
        if cohort_count == 0:
            continue
        placed_count = len(group[group["PlacementStatus"] == "Placed"])
        not_placed_count = len(group[group["PlacementStatus"] == "NotPlaced"])
        rate = round((placed_count / cohort_count * 100), 2)
        share = round((cohort_count / total_records * 100), 1)

        rows.append({
            "Cohort": str(cohort_val),
            "Total Students": cohort_count,
            "Cohort Share (%)": share,
            "Placed Students": placed_count,
            "Not Placed": not_placed_count,
            "Placement Rate (%)": rate,
            "Avg CGPA": round(float(group["CGPA"].mean()), 2),
            "Avg Aptitude": round(float(group["AptitudeTestScore"].mean()), 1),
            "Avg SSC (%)": round(float(group["SSC_Marks"].mean()), 1),
            "Avg HSC (%)": round(float(group["HSC_Marks"].mean()), 1),
        })

    return pd.DataFrame(rows)


def get_sample_student_profiles() -> dict:
    """
    Predefined student profile presets for quick demonstration and testing.
    """
    return {
        "🌟 Top Achiever (High Chance)": {
            "CGPA": 8.7,
            "Internships": 2,
            "Projects": 3,
            "Workshops/Certifications": 2,
            "AptitudeTestScore": 88,
            "SoftSkillsRating": 4.6,
            "ExtracurricularActivities": "Yes",
            "PlacementTraining": "Yes",
            "SSC_Marks": 84,
            "HSC_Marks": 86,
        },
        "⚖️ Average Competitor (Moderate)": {
            "CGPA": 7.6,
            "Internships": 1,
            "Projects": 2,
            "Workshops/Certifications": 1,
            "AptitudeTestScore": 76,
            "SoftSkillsRating": 4.1,
            "ExtracurricularActivities": "Yes",
            "PlacementTraining": "Yes",
            "SSC_Marks": 70,
            "HSC_Marks": 72,
        },
        "⚠️ Skill-Building Candidate (Needs Focus)": {
            "CGPA": 6.8,
            "Internships": 0,
            "Projects": 1,
            "Workshops/Certifications": 0,
            "AptitudeTestScore": 64,
            "SoftSkillsRating": 3.4,
            "ExtracurricularActivities": "No",
            "PlacementTraining": "No",
            "SSC_Marks": 60,
            "HSC_Marks": 62,
        },
    }
