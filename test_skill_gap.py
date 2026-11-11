"""
Automated Unit Tests for Day 3 Skill Gap Analysis
AI-Based Placement Prediction and Skill Gap Analysis System
"""

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import sys
from skill_gap import (
    ROLE_REQUIREMENTS,
    SKILL_RESOURCES,
    get_available_roles,
    get_all_unique_skills,
    get_required_skills,
    analyze_skill_gap,
)


def test_roles_and_requirements():
    print("\n--- 1. Testing Role Definitions & Required Skills ---")
    expected_roles = [
        "Java Developer",
        "Python Developer",
        "Web Developer",
        "Data Analyst",
        "Machine Learning Engineer",
    ]
    roles = get_available_roles()
    assert roles == expected_roles, f"Expected {expected_roles}, got {roles}"
    print(f"✅ Verified 5 job roles: {roles}")

    # Verify skill lists match exact user requirements
    assert ROLE_REQUIREMENTS["Java Developer"] == [
        "Java", "SQL", "HTML", "CSS", "JavaScript", "Spring Boot", "Hibernate", "REST API", "Git"
    ]
    assert ROLE_REQUIREMENTS["Python Developer"] == [
        "Python", "SQL", "HTML", "CSS", "Django", "Flask", "REST API", "Git"
    ]
    assert ROLE_REQUIREMENTS["Web Developer"] == [
        "HTML", "CSS", "JavaScript", "React", "SQL", "REST API", "Git"
    ]
    assert ROLE_REQUIREMENTS["Data Analyst"] == [
        "Python", "SQL", "Excel", "Power BI", "Statistics", "Pandas", "NumPy", "Data Visualization"
    ]
    assert ROLE_REQUIREMENTS["Machine Learning Engineer"] == [
        "Python", "SQL", "Statistics", "NumPy", "Pandas", "Scikit-learn", "Machine Learning", "Deep Learning"
    ]
    print("✅ Verified exact required skills per job role.")


def test_all_five_roles_skill_gap():
    print("\n--- 2. Testing Skill Gap Analysis Across All 5 Job Roles ---")

    test_scenarios = [
        # (Role, Student Skills, Expected Match Count, Expected Pct)
        (
            "Java Developer",
            ["Java", "SQL", "Git", "REST API"],
            4,
            round(4 / 9 * 100, 1),
        ),
        (
            "Python Developer",
            ["Python", "SQL", "HTML", "CSS", "Django", "Flask", "REST API", "Git"],
            8,
            100.0,
        ),
        (
            "Web Developer",
            ["HTML", "CSS", "JavaScript", "React"],
            4,
            round(4 / 7 * 100, 1),
        ),
        (
            "Data Analyst",
            ["Python", "SQL", "Excel", "Pandas", "NumPy"],
            5,
            round(5 / 8 * 100, 1),
        ),
        (
            "Machine Learning Engineer",
            ["Python", "SQL", "Statistics", "NumPy", "Pandas", "Scikit-learn"],
            6,
            round(6 / 8 * 100, 1),
        ),
    ]

    for role, student_skills, exp_matched_count, exp_pct in test_scenarios:
        res = analyze_skill_gap(role, student_skills)
        req = get_required_skills(role)

        assert len(res["matched_skills"]) == exp_matched_count, (
            f"Failed on {role}: expected {exp_matched_count} matched, got {len(res['matched_skills'])}"
        )
        assert res["match_percentage"] == exp_pct, (
            f"Failed on {role}: expected {exp_pct}%, got {res['match_percentage']}%"
        )
        assert len(res["matched_skills"]) + len(res["missing_skills"]) == len(req), (
            f"Failed on {role}: matched + missing must equal total required ({len(req)})"
        )
        assert len(res["recommendations"]) > 0, f"Expected learning recommendations for {role}"

        print(f"✅ {role}: {len(res['matched_skills'])}/{len(req)} matched ({res['match_percentage']}%) | Missing: {len(res['missing_skills'])}")


def test_resource_links_coverage():
    print("\n--- 3. Testing Learning Resource Coverage for All Skills ---")
    all_skills = get_all_unique_skills()
    print(f"Total unique skills across roles: {len(all_skills)}")

    for skill in all_skills:
        assert skill in SKILL_RESOURCES, f"Missing learning resource definition for skill '{skill}'"
        res = SKILL_RESOURCES[skill]
        assert "url" in res and res["url"].startswith("http"), f"Invalid resource URL for '{skill}'"
        assert "platform" in res and len(res["platform"]) > 0, f"Missing platform for '{skill}'"
        assert "description" in res and len(res["description"]) > 0, f"Missing description for '{skill}'"

    print("✅ Verified 100% learning resource link coverage for all 22 required skills.")


def test_edge_cases():
    print("\n--- 4. Testing Edge Cases ---")
    # Case A: Empty student skills
    for role in get_available_roles():
        res = analyze_skill_gap(role, [])
        assert res["match_percentage"] == 0.0
        assert len(res["matched_skills"]) == 0
        assert len(res["missing_skills"]) == len(get_required_skills(role))

    # Case B: Unknown / extra skills
    res_extra = analyze_skill_gap("Web Developer", ["HTML", "CSS", "Docker", "Kubernetes", "C++"])
    assert len(res_extra["matched_skills"]) == 2
    assert "Docker" in res_extra["additional_skills"]
    assert "Kubernetes" in res_extra["additional_skills"]

    # Case C: Case-insensitivity
    res_case = analyze_skill_gap("Python Developer", ["python", "sql", "git"])
    assert len(res_case["matched_skills"]) == 3

    print("✅ Verified empty skills, additional bonus skills, and case insensitivity.")


if __name__ == "__main__":
    test_roles_and_requirements()
    test_all_five_roles_skill_gap()
    test_resource_links_coverage()
    test_edge_cases()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Day 3 implementation is robust.")
