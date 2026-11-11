"""
Automated Unit Tests for Cohort Analytics
AI-Based Placement Prediction and Skill Gap Analysis System
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from src.data_utils import load_placement_dataset, get_dataset_summary, get_cohort_analysis


def test_cohort_analytics():
    print("\n--- 1. Testing Dataset & Basic Cohort Stats ---")
    df = load_placement_dataset()
    assert len(df) == 7225, f"Expected 7225 records, got {len(df)}"
    print(f"✅ Verified 7,225 records in dataset.")

    summary = get_dataset_summary()
    assert summary["total_students"] == 7225
    assert summary["placed_count"] == 3032
    assert summary["not_placed_count"] == 4193
    assert summary["placement_rate"] == 41.97
    assert summary["placed_avg_cgpa"] > summary["not_placed_avg_cgpa"]
    print(f"✅ Summary verified: Placed={summary['placed_count']}, Rate={summary['placement_rate']}%, Placed CGPA={summary['placed_avg_cgpa']}")

    print("\n--- 2. Testing All Cohort Dimensions ---")
    dimensions = [
        "CGPA Ranges",
        "Internships Completed",
        "Technical Projects",
        "Placement Training",
        "Aptitude Score Tiers",
        "Workshops & Certifications",
    ]

    for dim in dimensions:
        cdf = get_cohort_analysis(dim)
        assert not cdf.empty, f"Cohort analysis for '{dim}' returned empty dataframe!"
        assert "Cohort" in cdf.columns
        assert "Placement Rate (%)" in cdf.columns
        assert "Total Students" in cdf.columns
        total_in_cohorts = cdf["Total Students"].sum()
        assert total_in_cohorts == 7225, f"Sum of cohorts for '{dim}' ({total_in_cohorts}) does not equal 7225!"
        print(f"✅ Dimension '{dim}': {len(cdf)} cohorts, total students={total_in_cohorts}")

    print("\n🎉 ALL COHORT ANALYTICS TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_cohort_analytics()
