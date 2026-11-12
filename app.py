import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.model_utils import (
    load_model_and_metadata,
    validate_student_inputs,
    predict_placement,
    get_feature_importances,
)
from src.data_utils import (
    load_placement_dataset,
    get_dataset_summary,
    get_sample_student_profiles,
)

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM BLUE-WHITE THEME CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Placement Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom styling for a modern, responsive, blue & white UI
st.markdown(
    """
    <style>
        /* Overall page background & text */
        .stApp {
            background-color: #F8FAFC;
            color: #0F172A;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        /* Top header bar */
        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* Card container styles */
        .modern-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
        }
        .modern-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
            border-color: #CBD5E1;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #3B82F6 100%);
            color: #FFFFFF;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
        }
        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #DBEAFE;
            max-width: 800px;
            line-height: 1.5;
            margin-bottom: 16px;
        }

        /* Metric badge */
        .metric-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 9999px;
            padding: 6px 14px;
            font-size: 0.85rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-right: 8px;
            margin-bottom: 8px;
        }

        /* Result cards */
        .placed-card {
            background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
            color: #FFFFFF;
            border-radius: 16px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 10px 20px -5px rgba(5, 150, 105, 0.3);
            margin-bottom: 20px;
        }
        .not-placed-card {
            background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%);
            color: #FFFFFF;
            border-radius: 16px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 10px 20px -5px rgba(220, 38, 38, 0.3);
            margin-bottom: 20px;
        }

        /* Section headers */
        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* KPI small card */
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 16px 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #1D4ED8;
            margin: 4px 0;
        }
        .kpi-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Custom buttons styling */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%);
            color: #FFFFFF;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.25);
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
            box-shadow: 0 6px 12px -2px rgba(37, 99, 235, 0.35);
            transform: translateY(-1px);
        }

        /* Clean tabs & inputs */
        .stTextInput, .stNumberInput, .stSelectbox {
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "student_data" not in st.session_state:
    st.session_state["student_data"] = {
        "CGPA": 7.7,
        "Internships": 1,
        "Projects": 2,
        "Workshops/Certifications": 1,
        "AptitudeTestScore": 80,
        "SoftSkillsRating": 4.2,
        "ExtracurricularActivities": "Yes",
        "PlacementTraining": "Yes",
        "SSC_Marks": 75,
        "HSC_Marks": 75,
    }

if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = None

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"


def navigate_to(page_name: str):
    st.session_state["current_page"] = page_name
    st.rerun()


# -----------------------------------------------------------------------------
# ROLE-BASED SKILL REQUIREMENTS
# -----------------------------------------------------------------------------
ROLE_SKILLS = {
    "Python Developer": [
        "Python", "SQL", "HTML", "CSS", "Django",
        "Flask", "REST API", "Git"
    ],
    "Java Developer": [
        "Java", "SQL", "HTML", "CSS", "JavaScript",
        "Spring Boot", "Hibernate", "REST API", "Git"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "SQL", "REST API", "Git"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI",
        "Statistics", "Pandas", "NumPy", "Data Visualization"
    ],
    "ML Engineer": [
        "Python", "SQL", "Statistics", "NumPy",
        "Pandas", "Scikit-learn", "Machine Learning",
        "Deep Learning"
    ],
}

ALL_SKILLS = sorted({
    skill
    for skills in ROLE_SKILLS.values()
    for skill in skills
})

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 12px 0 20px 0;">
            <div style="background: #EFF6FF; width: 64px; height: 64px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 10px; border: 1px solid #BFDBFE;">
                <span style="font-size: 32px;">🎓</span>
            </div>
            <h2 style="font-size: 1.2rem; font-weight: 800; color: #1E3A8A; margin: 0;">Placement AI</h2>
            <p style="font-size: 0.8rem; color: #64748B; margin: 2px 0 0 0;">Prediction & Analytics System</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🧭 Navigation")

    nav_options = [
        "Home",
        "Student Details",
        "Placement Prediction",
        "Dashboard",
        "Skill Gap Analysis",
    ]

    selected_page = st.radio(
        label="Select Page",
        options=nav_options,
        index=nav_options.index(st.session_state["current_page"])
        if st.session_state["current_page"] in nav_options
        else 0,
        label_visibility="collapsed",
    )

    if selected_page != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Model Specification")
    try:
        _, metadata = load_model_and_metadata()
        acc = metadata.get("accuracy", 0.7919) * 100
        st.markdown(
            f"""
            <div style="background: #F1F5F9; border-radius: 8px; padding: 12px; font-size: 0.82rem; color: #334155;">
                <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 4px;">Random Forest Classifier</div>
                <div>• Estimators: <b>200 Trees</b></div>
                <div>• Test Accuracy: <b>{acc:.2f}%</b></div>
                <div>• Input Features: <b>10 Dimensions</b></div>
                <div>• Status: <span style="color: #059669; font-weight: 600;">Active & Loaded</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.warning(f"Model status: {e}")

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-size: 0.75rem; color: #94A3B8; padding-top: 10px;">
            <b>College Mini Project</b><br>
            AI-Based Placement Prediction<br>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 4. PAGE 1: HOME (PROJECT OVERVIEW)
# -----------------------------------------------------------------------------
def render_home_page():
    # Hero Section
    st.markdown(
        """
        <div class="hero-banner">
            <div class="metric-badge">⚡ AI & Machine Learning Solution</div>
            <div class="metric-badge">🎯 Random Forest Pipeline</div>
            <div class="metric-badge">📊 7,200+ Student Benchmark</div>
            <h1 class="hero-title">AI-Based Placement Prediction System</h1>
            <p class="hero-subtitle">
                An intelligent academic decision-support platform designed to evaluate graduating students' 
                employability, predict campus placement outcomes with machine learning, and empower learners 
                with data-driven academic and professional benchmarking.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action callouts
    col_btn1, col_btn2, _ = st.columns([1.5, 1.5, 3])
    with col_btn1:
        if st.button("📝 Enter Student Details", use_container_width=True):
            navigate_to("Student Details")
    with col_btn2:
        if st.button("📊 Explore Dataset Dashboard", use_container_width=True):
            navigate_to("Dashboard")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Core System Pillars
    st.markdown('<div class="section-title">🏛️ System Architecture & Workflow</div>', unsafe_allow_html=True)

    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown(
            """
<div class="modern-card" style="min-height: 250px; height: auto;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">📂</div>
                <h4 style="color: #1E3A8A; margin-bottom: 6px;">1. Data Ingestion</h4>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.4;">
                    Historical records tracking 10 comprehensive metrics across academics, technical projects, internships, and interpersonal competencies.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step2:
        st.markdown(
            """
  <div class="modern-card" style="min-height: 250px; height: auto;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">⚙️</div>
                <h4 style="color: #1E3A8A; margin-bottom: 6px;">2. ML Pipeline</h4>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.4;">
                    Trained Random Forest ensemble with 200 trees, median numeric imputation, one-hot categorical encoding, and balanced class weights.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step3:
        st.markdown(
            """
            <div class="modern-card" style="min-height: 250px; height: auto;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">🎯</div>
                <h4 style="color: #1E3A8A; margin-bottom: 6px;">3. Placement Outcome</h4>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.4;">
                    Instant classification into <b>Placed</b> or <b>Not Placed</b> with probability distribution scoring and metric-by-metric cohort comparison.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step4:
        st.markdown(
            """
           <div class="modern-card" style="min-height: 250px; height: auto;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">🚀</div>
                <h4 style="color: #1E3A8A; margin-bottom: 6px;">4. Skill Gap Phase</h4>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.4;">
                    Upcoming Day 3 milestone: Tailored skill gap identification, targeted learning roadmaps, and actionable career improvement pathways.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature Dimensions Overview
    st.markdown('<div class="section-title">🔍 Evaluated Performance Dimensions</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="modern-card">
                <h4 style="color: #2563EB; margin-bottom: 10px;">🎓 Academic Foundation</h4>
                <ul style="font-size: 0.88rem; color: #334155; line-height: 1.7; padding-left: 20px;">
                    <li><b>CGPA</b>: Undergraduate grade point average (6.5 - 10.0 scale)</li>
                    <li><b>SSC Marks</b>: 10th standard board percentage</li>
                    <li><b>HSC Marks</b>: 12th standard / pre-university board percentage</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="modern-card">
                <h4 style="color: #2563EB; margin-bottom: 10px;">💼 Hands-on Technical Experience</h4>
                <ul style="font-size: 0.88rem; color: #334155; line-height: 1.7; padding-left: 20px;">
                    <li><b>Internships</b>: Industry internships and real-world work experience</li>
                    <li><b>Projects</b>: Academic, capstone, and personal technical projects</li>
                    <li><b>Workshops & Certifications</b>: Professional courses and accredited workshops</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="modern-card">
                <h4 style="color: #2563EB; margin-bottom: 10px;">🧠 Evaluation & Professional Readiness</h4>
                <ul style="font-size: 0.88rem; color: #334155; line-height: 1.7; padding-left: 20px;">
                    <li><b>Aptitude Test Score</b>: Quantitative & logical reasoning test (0 - 100)</li>
                    <li><b>Soft Skills Rating</b>: Communication & team collaboration (1.0 - 5.0)</li>
                    <li><b>Placement Training & Extracurriculars</b>: Institutional career coaching</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# 5. PAGE 2: STUDENT DETAILS (INPUT FORM)
# -----------------------------------------------------------------------------
def render_student_details_page():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="color: #1E3A8A; font-weight: 800; margin-bottom: 4px;">📝 Student Profile & Performance Entry</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Provide the student's academic credentials, practical experience, and assessment scores.
                All 10 parameters are strictly aligned with the trained Random Forest model metadata.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Preset profiles loader for quick testing
    sample_profiles = get_sample_student_profiles()
    with st.expander("⚡ Quick Profile Presets (Click to Auto-fill Demo Data)", expanded=False):
        preset_cols = st.columns(len(sample_profiles))
        for idx, (p_name, p_data) in enumerate(sample_profiles.items()):
            with preset_cols[idx]:
                if st.button(f"Load {p_name.split()[1]}", key=f"btn_preset_{idx}", use_container_width=True):
                    st.session_state["student_data"] = p_data.copy()
                    st.success(f"Loaded '{p_name}' successfully!")
                    st.rerun()

    curr_data = st.session_state["student_data"]

    # Student Details Form
    with st.form("student_details_form"):
        col1, col2, col3 = st.columns(3)

        # Column 1: Academic Scores
        with col1:
            st.markdown('<div class="section-title">🎓 Academic Record</div>', unsafe_allow_html=True)
            cgpa = st.number_input(
                "College CGPA (out of 10.0)",
                min_value=0.0,
                max_value=10.0,
                value=float(curr_data.get("CGPA", 7.7)),
                step=0.05,
                help="Cumulative Grade Point Average across completed semesters.",
            )
            ssc_marks = st.number_input(
                "10th Standard (SSC) Marks (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(curr_data.get("SSC_Marks", 75)),
                step=0.5,
                help="Secondary School Certificate percentage score.",
            )
            hsc_marks = st.number_input(
                "12th Standard (HSC) Marks (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(curr_data.get("HSC_Marks", 75)),
                step=0.5,
                help="Higher Secondary Certificate percentage score.",
            )

        # Column 2: Practical Projects & Internships
        with col2:
            st.markdown('<div class="section-title">💼 Practical Exposure</div>', unsafe_allow_html=True)
            internships = st.number_input(
                "Number of Internships",
                min_value=0,
                max_value=10,
                value=int(curr_data.get("Internships", 1)),
                step=1,
                help="Number of completed industry internships or industrial training.",
            )
            projects = st.number_input(
                "Number of Technical Projects",
                min_value=0,
                max_value=10,
                value=int(curr_data.get("Projects", 2)),
                step=1,
                help="Academic capstones, software apps, or hardware projects built.",
            )
            workshops = st.number_input(
                "Workshops & Certifications",
                min_value=0,
                max_value=10,
                value=int(curr_data.get("Workshops/Certifications", 1)),
                step=1,
                help="Accredited skill courses, bootcamps, and technical certifications.",
            )

        # Column 3: Aptitude & Soft Skills
        with col3:
            st.markdown('<div class="section-title">🧠 Readiness & Behavioral</div>', unsafe_allow_html=True)
            aptitude = st.number_input(
                "Aptitude Test Score (0 - 100)",
                min_value=0,
                max_value=100,
                value=int(curr_data.get("AptitudeTestScore", 80)),
                step=1,
                help="Quantitative, logical reasoning, and verbal aptitude assessment score.",
            )
            soft_skills = st.slider(
                "Soft Skills Rating (1.0 to 5.0)",
                min_value=1.0,
                max_value=5.0,
                value=float(curr_data.get("SoftSkillsRating", 4.2)),
                step=0.1,
                help="Assessment rating on communication, leadership, and teamwork.",
            )

            extra_default = 0 if curr_data.get("ExtracurricularActivities") == "No" else 1
            training_default = 0 if curr_data.get("PlacementTraining") == "No" else 1

            extracurricular = st.selectbox(
                "Extracurricular Activities Participation",
                options=["No", "Yes"],
                index=extra_default,
                help="Active involvement in student clubs, sports, or collegiate events.",
            )
            training = st.selectbox(
                "Placement Training Attended",
                options=["No", "Yes"],
                index=training_default,
                help="Participation in institutional campus placement training programs.",
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        form_c1, form_c2, form_c3 = st.columns([1.5, 1.5, 3])

        with form_c1:
            submit_save = st.form_submit_button("💾 Save Profile Details", use_container_width=True)
        with form_c2:
            submit_predict = st.form_submit_button("🔮 Predict Placement Outcome", use_container_width=True)

    # Process Form Submission
    if submit_save or submit_predict:
        submitted_data = {
            "CGPA": float(cgpa),
            "Internships": int(internships),
            "Projects": int(projects),
            "Workshops/Certifications": int(workshops),
            "AptitudeTestScore": int(aptitude),
            "SoftSkillsRating": float(soft_skills),
            "ExtracurricularActivities": str(extracurricular),
            "PlacementTraining": str(training),
            "SSC_Marks": int(ssc_marks),
            "HSC_Marks": int(hsc_marks),
        }

        is_valid, error_msgs = validate_student_inputs(submitted_data)
        if not is_valid:
            for err in error_msgs:
                st.error(f"❌ {err}")
        else:
            st.session_state["student_data"] = submitted_data
            try:
                pred_result = predict_placement(submitted_data)
                st.session_state["prediction_result"] = pred_result
                st.success("✅ Student details saved and validated successfully!")

                if submit_predict:
                    navigate_to("Placement Prediction")
                else:
                    st.info("Profile updated! Navigate to 'Placement Prediction' or click Predict to view full analysis.")
            except Exception as e:
                st.error(f"Model prediction error: {e}")

    # Summary preview of currently loaded student profile
    st.markdown("---")
    st.markdown('<div class="section-title">📋 Current Profile Snapshot</div>', unsafe_allow_html=True)
    curr = st.session_state["student_data"]
    preview_col1, preview_col2, preview_col3, preview_col4 = st.columns(4)
    with preview_col1:
        st.metric(label="CGPA", value=f"{curr['CGPA']:.2f} / 10")
    with preview_col2:
        st.metric(label="Aptitude Score", value=f"{curr['AptitudeTestScore']} / 100")
    with preview_col3:
        st.metric(label="Projects / Internships", value=f"{curr['Projects']} P / {curr['Internships']} I")
    with preview_col4:
        st.metric(label="Soft Skills Rating", value=f"{curr['SoftSkillsRating']:.1f} / 5.0")


# -----------------------------------------------------------------------------
# 6. PAGE 3: PLACEMENT PREDICTION (RESULTS & BENCHMARKING)
# -----------------------------------------------------------------------------
def render_prediction_page():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="color: #1E3A8A; font-weight: 800; margin-bottom: 4px;">🎯 Placement Prediction & Evaluation</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Real-time prediction generated by the trained Random Forest Classifier, alongside probabilistic confidence 
                and cohort benchmarking against historical campus outcomes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    student_data = st.session_state.get("student_data")
    if not student_data:
        st.warning("⚠️ No student profile details found. Please enter student details first.")
        if st.button("Go to Student Details Form"):
            navigate_to("Student Details")
        return

    # Ensure prediction is calculated
    if st.session_state.get("prediction_result") is None:
        try:
            st.session_state["prediction_result"] = predict_placement(student_data)
        except Exception as e:
            st.error(f"Error computing prediction: {e}")
            return

    res = st.session_state["prediction_result"]
    is_placed = res["is_placed"]
    confidence = res["placement_probability"]
    pred_label = res["prediction"]

    # 1. Prediction Outcome Hero Card
    if is_placed:
        st.markdown(
            f"""
            <div class="placed-card">
                <div style="font-size: 2.8rem; margin-bottom: 8px;">🎉</div>
                <h1 style="color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin: 0;">PREDICTION: PLACED</h1>
                <p style="font-size: 1.15rem; color: #D1FAE5; margin-top: 6px; font-weight: 500;">
                    High Likelihood of Campus Placement Success
                </p>
                <div style="display: inline-block; background: rgba(255,255,255,0.2); padding: 8px 18px; border-radius: 9999px; margin-top: 10px; font-weight: 700; font-size: 1.1rem;">
                    Placement Confidence: {confidence:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        not_placed_prob = res["probabilities"].get("NotPlaced", 100.0 - confidence)
        st.markdown(
            f"""
            <div class="not-placed-card">
                <div style="font-size: 2.8rem; margin-bottom: 8px;">⚠️</div>
                <h1 style="color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin: 0;">PREDICTION: NOT PLACED</h1>
                <p style="font-size: 1.15rem; color: #FEE2E2; margin-top: 6px; font-weight: 500;">
                    Placement at Risk — Targeted Intervention & Skill Upgrading Recommended
                </p>
                <div style="display: inline-block; background: rgba(255,255,255,0.2); padding: 8px 18px; border-radius: 9999px; margin-top: 10px; font-weight: 700; font-size: 1.1rem;">
                    Placement Probability: {confidence:.1f}% | Risk Factor: {not_placed_prob:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Probability Gauge and Class Breakdown
    col_gauge, col_details = st.columns([1.2, 1.8])

    with col_gauge:
        st.markdown('<div class="section-title">📊 Confidence Meter</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=confidence,
                number={"suffix": "%", "font": {"size": 36, "color": "#1E3A8A"}},
                title={"text": "Placement Likelihood", "font": {"size": 16, "color": "#475569"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94A3B8"},
                    "bar": {"color": "#2563EB" if is_placed else "#DC2626", "thickness": 0.28},
                    "bgcolor": "#F1F5F9",
                    "borderwidth": 1,
                    "bordercolor": "#CBD5E1",
                    "steps": [
                        {"range": [0, 50], "color": "#FEE2E2"},
                        {"range": [50, 75], "color": "#FEF3C7"},
                        {"range": [75, 100], "color": "#DCFCE7"},
                    ],
                    "threshold": {
                        "line": {"color": "#1E3A8A", "width": 4},
                        "thickness": 0.75,
                        "value": 50,
                    },
                },
            )
        )
        fig_gauge.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_details:
        st.markdown('<div class="section-title">🔍 Probability Distribution</div>', unsafe_allow_html=True)
        prob_df = pd.DataFrame(
            [
                {"Outcome": "Placed", "Probability (%)": res["probabilities"].get("Placed", 0.0)},
                {"Outcome": "Not Placed", "Probability (%)": res["probabilities"].get("NotPlaced", 0.0)},
            ]
        )
        fig_prob = px.bar(
            prob_df,
            x="Probability (%)",
            y="Outcome",
            orientation="h",
            color="Outcome",
            color_discrete_map={"Placed": "#059669", "Not Placed": "#DC2626"},
            text="Probability (%)",
        )
        fig_prob.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        fig_prob.update_layout(
            height=260,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, 105], showgrid=True, gridcolor="#E2E8F0"),
            yaxis=dict(showgrid=False),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_prob, use_container_width=True)

    # 3. Benchmark Comparison against Dataset Average
    st.markdown("---")
    st.markdown('<div class="section-title">📈 Student Profile vs Historical Batch Average</div>', unsafe_allow_html=True)

    summary = get_dataset_summary()
    comp_data = [
        {"Metric": "College CGPA", "Student Value": float(student_data["CGPA"]), "Batch Average": summary["avg_cgpa"], "Unit": "Scale of 10"},
        {"Metric": "Aptitude Score", "Student Value": float(student_data["AptitudeTestScore"]), "Batch Average": summary["avg_aptitude"], "Unit": "Marks (0-100)"},
        {"Metric": "Soft Skills Rating", "Student Value": float(student_data["SoftSkillsRating"]), "Batch Average": summary["avg_soft_skills"], "Unit": "Scale of 5.0"},
        {"Metric": "Internships Completed", "Student Value": float(student_data["Internships"]), "Batch Average": summary["avg_internships"], "Unit": "Count"},
        {"Metric": "Technical Projects", "Student Value": float(student_data["Projects"]), "Batch Average": summary["avg_projects"], "Unit": "Count"},
        {"Metric": "10th SSC Marks", "Student Value": float(student_data["SSC_Marks"]), "Batch Average": summary["avg_ssc"], "Unit": "Percentage (%)"},
        {"Metric": "12th HSC Marks", "Student Value": float(student_data["HSC_Marks"]), "Batch Average": summary["avg_hsc"], "Unit": "Percentage (%)"},
    ]

    comp_df = pd.DataFrame(comp_data)

    def status_flag(row):
        diff = row["Student Value"] - row["Batch Average"]
        if diff >= 0:
            return f"✅ Above (+{diff:.2f})"
        else:
            return f"⚠️ Below ({diff:.2f})"

    comp_df["Cohort Comparison"] = comp_df.apply(status_flag, axis=1)

    # Display comparison table
    st.dataframe(
        comp_df,
        column_config={
            "Metric": st.column_config.TextColumn("Parameter", width="medium"),
            "Student Value": st.column_config.NumberColumn("Student's Score", format="%.2f"),
            "Batch Average": st.column_config.NumberColumn("Historical Cohort Avg", format="%.2f"),
            "Cohort Comparison": st.column_config.TextColumn("Status vs Benchmark", width="medium"),
            "Unit": st.column_config.TextColumn("Scale / Unit", width="small"),
        },
        use_container_width=True,
        hide_index=True,
    )

    # Next Steps navigation
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    c_back, c_dash, _ = st.columns([1.5, 1.5, 3])
    with c_back:
        if st.button("✏️ Modify Student Profile", use_container_width=True):
            navigate_to("Student Details")
    with c_dash:
        if st.button("📊 Explore Placement Dashboard", use_container_width=True):
            navigate_to("Dashboard")




# -----------------------------------------------------------------------------
# 8. PAGE 5: ROLE-BASED SKILL GAP ANALYSIS
# -----------------------------------------------------------------------------
def render_skill_gap_page():

    st.markdown(
        """
        <h2 style="color:#1E3A8A;">🚀 Role-Based Skill Gap Analysis</h2>
        <p style="color:#64748B;">
        Identify your matching skills, missing skills and personalized
        learning roadmap based on your target career.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Select job role
    selected_role = st.selectbox(
        "🎯 Select Your Target Job Role",
        list(ROLE_SKILLS.keys())
    )

    required_skills = ROLE_SKILLS[selected_role]

    st.markdown("### 💻 Select the skills you already know")

    student_skills = st.multiselect(
        "Choose your existing technical skills",
        options=ALL_SKILLS,
        placeholder="Search and select your skills..."
    )

    # Compare skills
    matched_skills = [
        skill for skill in required_skills
        if skill in student_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in student_skills
    ]

    total_skills = len(required_skills)
    match_percentage = (
        len(matched_skills) / total_skills
    ) * 100

    st.markdown("---")
    st.markdown("### 📊 Your Skill Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Required Skills", total_skills)

    with col2:
        st.metric("Matching Skills", len(matched_skills))

    with col3:
        st.metric("Missing Skills", len(missing_skills))

    st.markdown("#### Skill Match Percentage")

    st.progress(int(match_percentage))
    st.subheader(f"{match_percentage:.1f}% Match")

    # Matched skills
    st.markdown("---")
    st.markdown("### ✅ Your Matching Skills")

    if matched_skills:
        for skill in matched_skills:
            st.success(f"✓ {skill}")
    else:
        st.info("No matching skills selected yet.")

    # Missing skills
    st.markdown("### ⚠️ Skills You Need to Learn")

    if missing_skills:
        for skill in missing_skills:
            st.warning(f"• {skill}")
    else:
        st.success("Excellent! You have selected all required skills.")

    # Learning roadmap
    st.markdown("---")
    st.markdown("### 🗺️ Personalized Learning Roadmap")

    if missing_skills:
        chunk_size = max(1, (len(missing_skills) + 3) // 4)

        roadmap_weeks = [
            missing_skills[i:i + chunk_size]
            for i in range(0, len(missing_skills), chunk_size)
        ]

        for week_number, week_skills in enumerate(roadmap_weeks, 1):
            with st.expander(
                f"📅 Week {week_number} - Learning Plan",
                expanded=(week_number == 1)
            ):
                for skill in week_skills:
                    st.markdown(f"**{skill}**")
                    st.write(
                        f"• Learn the fundamentals of {skill}."
                    )
                    st.write(
                        f"• Follow tutorials and practise examples."
                    )
                    st.write(
                        f"• Complete a small practical task using {skill}."
                    )

        st.info(
            "Tip: Practise each skill regularly and build one "
            "real-world project to strengthen your portfolio."
        )

    else:
        st.balloons()
        st.success(
            f"You have matched all the listed requirements for "
            f"{selected_role}!"
        )

    st.markdown("---")
    st.caption(
        "Skill match is calculated from the skills selected by the "
        "student and the predefined requirements for the chosen role."
    )
# PAGE 4: DASHBOARD
def render_dashboard_page():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="color: #1E3A8A; font-weight: 800; margin-bottom: 4px;">📊 Campus Placement Analytics Dashboard</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Exploratory data analysis and interactive visual insights derived from the 7,225 historical student records.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df = load_placement_dataset()
    except Exception as e:
        st.error(f"Failed to load dataset: {e}")
        return

    summary = get_dataset_summary()

    # Top KPI Metrics Row
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Students</div>
                <div class="kpi-value">{summary['total_students']:,}</div>
                <div style="font-size: 0.78rem; color: #64748B;">Historical Records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Placement Rate</div>
                <div class="kpi-value">{summary['placement_rate']}%</div>
                <div style="font-size: 0.78rem; color: #059669;">{summary['placed_count']:,} Placed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Average CGPA</div>
                <div class="kpi-value">{summary['avg_cgpa']}</div>
                <div style="font-size: 0.78rem; color: #64748B;">Range: 6.5 - 9.1</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Avg Aptitude</div>
                <div class="kpi-value">{summary['avg_aptitude']}</div>
                <div style="font-size: 0.78rem; color: #64748B;">Out of 100 Marks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Avg HSC (12th)</div>
                <div class="kpi-value">{summary['avg_hsc']}%</div>
                <div style="font-size: 0.78rem; color: #64748B;">Secondary Benchmark</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Interactive Filter Bar
    with st.expander("🔍 Interactive Data Filters", expanded=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            status_filter = st.selectbox(
                "Placement Status Filter",
                options=["All Records", "Placed", "NotPlaced"],
                index=0,
            )
        with f_col2:
            min_cgpa, max_cgpa = float(df["CGPA"].min()), float(df["CGPA"].max())
            cgpa_range = st.slider(
                "Filter CGPA Range",
                min_value=min_cgpa,
                max_value=max_cgpa,
                value=(min_cgpa, max_cgpa),
                step=0.1,
            )
        with f_col3:
            training_filter = st.selectbox(
                "Placement Training Filter",
                options=["All Students", "Attended (Yes)", "Not Attended (No)"],
                index=0,
            )

    # Apply filters
    filtered_df = df.copy()
    if status_filter != "All Records":
        filtered_df = filtered_df[filtered_df["PlacementStatus"] == status_filter]

    filtered_df = filtered_df[
        (filtered_df["CGPA"] >= cgpa_range[0]) & (filtered_df["CGPA"] <= cgpa_range[1])
    ]

    if training_filter == "Attended (Yes)":
        filtered_df = filtered_df[filtered_df["PlacementTraining"] == "Yes"]
    elif training_filter == "Not Attended (No)":
        filtered_df = filtered_df[filtered_df["PlacementTraining"] == "No"]

    st.caption(f"Showing **{len(filtered_df):,}** out of {len(df):,} student records based on selected filters.")

    # Charts Section
    st.markdown('<div class="section-title">📈 Statistical Visualizations</div>', unsafe_allow_html=True)

    # Row 1: Placement Distribution Donut & CGPA Box Plot
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            '<div class="modern-card" style="padding: 16px;"><h4 style="color: #1E3A8A; margin-bottom: 8px;">Placement Status Distribution</h4>',
            unsafe_allow_html=True,
        )
        dist_counts = filtered_df["PlacementStatus"].value_counts().reset_index()
        dist_counts.columns = ["Status", "Count"]

        fig_pie = px.pie(
            dist_counts,
            values="Count",
            names="Status",
            hole=0.55,
            color="Status",
            color_discrete_map={"Placed": "#2563EB", "NotPlaced": "#94A3B8"},
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            height=320,
            showlegend=True,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown(
            '<div class="modern-card" style="padding: 16px;"><h4 style="color: #1E3A8A; margin-bottom: 8px;">CGPA Distribution by Placement Outcome</h4>',
            unsafe_allow_html=True,
        )
        fig_box = px.box(
            filtered_df,
            x="PlacementStatus",
            y="CGPA",
            color="PlacementStatus",
            color_discrete_map={"Placed": "#059669", "NotPlaced": "#DC2626"},
            points="outliers",
        )
        fig_box.update_layout(
            height=320,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
            xaxis=dict(title="Placement Status"),
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2: Aptitude vs Soft Skills Scatter & Internships/Projects Impact
    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.markdown(
            '<div class="modern-card" style="padding: 16px;"><h4 style="color: #1E3A8A; margin-bottom: 8px;">Aptitude Score vs Soft Skills Rating</h4>',
            unsafe_allow_html=True,
        )
        # Sample for smooth responsive plotting if dataset is large
        sample_plot = filtered_df.sample(min(1200, len(filtered_df)), random_state=42) if len(filtered_df) > 1200 else filtered_df

        fig_scatter = px.scatter(
            sample_plot,
            x="AptitudeTestScore",
            y="SoftSkillsRating",
            color="PlacementStatus",
            color_discrete_map={"Placed": "#2563EB", "NotPlaced": "#F59E0B"},
            opacity=0.65,
            hover_data=["CGPA", "Projects", "Internships"],
        )
        fig_scatter.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Aptitude Test Score (0 - 100)", showgrid=True, gridcolor="#E2E8F0"),
            yaxis=dict(title="Soft Skills Rating (1 - 5)", showgrid=True, gridcolor="#E2E8F0"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col4:
        st.markdown(
            '<div class="modern-card" style="padding: 16px;"><h4 style="color: #1E3A8A; margin-bottom: 8px;">Internship Experience vs Placement Status</h4>',
            unsafe_allow_html=True,
        )
        intern_grouped = (
            filtered_df.groupby(["Internships", "PlacementStatus"]).size().reset_index(name="Count")
        )
        fig_bar = px.bar(
            intern_grouped,
            x="Internships",
            y="Count",
            color="PlacementStatus",
            barmode="group",
            color_discrete_map={"Placed": "#059669", "NotPlaced": "#94A3B8"},
        )
        fig_bar.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Number of Internships Completed", tickmode="linear"),
            yaxis=dict(title="Number of Students", showgrid=True, gridcolor="#E2E8F0"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 3: Random Forest Feature Importance
    st.markdown('<div class="section-title">🌲 Random Forest Feature Importance Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="modern-card" style="padding: 20px;">
            <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 12px;">
                Direct Gini-importance weights computed by the 200 Decision Trees in the trained Random Forest classifier.
                Features at the top exercise the greatest predictive power during evaluation.
            </p>
        """,
        unsafe_allow_html=True,
    )
    df_imp = get_feature_importances()
    if not df_imp.empty:
        fig_imp = px.bar(
            df_imp.sort_values(by="Importance", ascending=True),
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale=["#BFDBFE", "#2563EB", "#1E3A8A"],
            text="Importance",
        )
        fig_imp.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_imp.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Feature Importance Score (Gini Weight)", showgrid=True, gridcolor="#E2E8F0"),
            yaxis=dict(title=""),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Row 4: Raw Dataset Explorer
    st.markdown('<div class="section-title">📑 Dataset Records Explorer</div>', unsafe_allow_html=True)
    with st.expander("View Filtered Data Table & Download", expanded=False):
        st.dataframe(filtered_df, use_container_width=True, height=300)
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="placement_filtered_records.csv",
            mime="text/csv",
        )


# -----------------------------------------------------------------------------
# 8. MAIN ROUTER
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# 9. MAIN ROUTER
# -----------------------------------------------------------------------------
def main():
    current_page = st.session_state.get("current_page", "Home")

    if current_page == "Home":
        render_home_page()

    elif current_page == "Student Details":
        render_student_details_page()

    elif current_page == "Placement Prediction":
        render_prediction_page()

    elif current_page == "Dashboard":
        render_dashboard_page()

    elif current_page == "Skill Gap Analysis":
        render_skill_gap_page()

    else:
        render_home_page()


if __name__ == "__main__":
    main()
