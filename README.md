# AI-Based Placement Prediction and Skill Gap Analysis System

A college mini project implementing machine learning to evaluate student employability, predict campus placement outcomes, benchmark student performance against historical cohort data, and provide personalized skill gap analysis with targeted learning resources.

---

## 📁 Project Structure

```
AI_Placement_Prediction/
├── dataset/
│   └── placement.csv             # Historical placement dataset (7,225 records)
├── models/
│   ├── placement_model.pkl       # Trained Random Forest classifier pipeline (Day 1)
│   └── model_metadata.pkl        # Feature metadata and evaluation metrics (Day 1)
├── src/
│   ├── __init__.py
│   ├── data_utils.py             # Dataset loader, aggregations, and sample presets
│   ├── model_utils.py            # Model loader, input validation, and inference
│   └── skill_gap.py              # Skill gap logic wrapper
├── .streamlit/
│   └── config.toml               # Professional blue-and-white theme configuration
├── app.py                        # Streamlit web application with sticky top nav (6 pages)
├── skill_gap.py                  # Skill gap analysis, role requirements & resources
├── test_cohort_analytics.py      # Automated unit tests for all cohort dimensions
├── test_skill_gap.py             # Automated unit tests for all 5 job roles
├── inspect_dataset.py            # Dataset exploration script
├── train_model.py                # Model training script
├── test_model.py                 # CLI model test script
└── requirements.txt              # Project dependencies
```

---

## 🚀 How to Run the Application

### 1. Open Terminal in the Project Directory
```powershell
cd E:\AI_Placement_Prediction
```

### 2. Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(Or in Command Prompt: `venv\Scripts\activate.bat`)*

### 3. Launch the Streamlit Frontend
```powershell
streamlit run app.py
```

The web application will open automatically in your default browser at:
`http://localhost:8501`

### 4. Run Automated Unit Tests (Optional)
```powershell
python test_cohort_analytics.py
python test_skill_gap.py
python test_model.py
```

---

## 🌟 Application Features

### 1. Modern Sticky Top Navigation & Independent Scrolling
* Replaces sidebar navigation with a fixed horizontal top navigation bar:
  `Home | Student Details | Placement Prediction | Dashboard | Skill Gap Analysis | Cohort Analytics`.
* Pure CSS sticky positioning with backdrop blur ensures the top navigation remains fixed at the top of the viewport during scrolling.
* Main page contents scroll independently beneath the navbar with zero layout shifts or horizontal scrollbars.

### 2. Home Page
* Executive overview of the system architecture and decision-support pipeline.
* High-level metric highlights (79.19% model accuracy, 200 trees, 10 feature dimensions).
* Fast navigation buttons to Student Details, Skill Gap Analysis, and Analytics Dashboard.

### 2. Student Details Form
* Card-based form for entering 10 academic and behavioral parameters:
  * **Academic Record**: CGPA, 10th (SSC) Marks, 12th (HSC) Marks.
  * **Practical Exposure**: Internships, Technical Projects, Workshops & Certifications.
  * **Readiness & Personal Skills**: Aptitude Test Score, Soft Skills Rating, Extracurriculars, Placement Training.
* 1-click **Quick Profile Presets** for easy testing.

### 3. Placement Prediction
* Integration with the trained **Random Forest model** (`placement_model.pkl`).
* Displays outcome (`Placed` vs `Not Placed`) with probability confidence gauge.
* Comparative table benchmarking student scores against cohort averages.

### 4. Skill Gap Analysis & Recommendations (Day 3 Feature)
* **5 Target Job Roles**:
  * **Java Developer**: Java, SQL, HTML, CSS, JavaScript, Spring Boot, Hibernate, REST API, Git.
  * **Python Developer**: Python, SQL, HTML, CSS, Django, Flask, REST API, Git.
  * **Web Developer**: HTML, CSS, JavaScript, React, SQL, REST API, Git.
  * **Data Analyst**: Python, SQL, Excel, Power BI, Statistics, Pandas, NumPy, Data Visualization.
  * **Machine Learning Engineer**: Python, SQL, Statistics, NumPy, Pandas, Scikit-learn, Machine Learning, Deep Learning.
* **Streamlit Multiselect**: Allows students to select their acquired technical competencies with 1-click role presets.
* **Skill Match Calculation**:
  $$\text{Skill Match \%} = \frac{\text{Matched Skills}}{\text{Total Required Skills}} \times 100$$
* **Visual Status Indicators**:
  * Plotly gauge meter with color-coded readiness tiers (High / Moderate / Foundational).
  * Horizontal skill coverage breakdown chart.
  * Green badge tags for matched skills (`✓`).
  * Red badge tags for missing skills (`✗`).
  * Blue badge tags for bonus/additional skills (`★`).
* **Personalized Learning Roadmap**: 4-phase structured action plan (Foundations $\rightarrow$ Frameworks $\rightarrow$ APIs & Tooling $\rightarrow$ Capstone Projects).
* **Curated Learning Resources**: Direct links to official documentation (Oracle Java, Python.org, MDN Web Docs, Spring.io, React.dev, Microsoft Learn, Scikit-learn, etc.) for missing skills.

### 6. Analytics Dashboard
* Key placement statistics across 7,225 records.
* Interactive filters and Plotly visualizations (Placement distribution donut, CGPA boxplot, Aptitude vs Soft Skills scatter plot, Internship impact, and Random Forest Gini feature importances).
* Data table explorer with CSV export.

### 7. Cohort Analytics (New Feature)
* Cohort-level empirical analysis over all 7,225 student records in `dataset/placement.csv`.
* **Summary KPI Cards**: Total Students (7,225), Placed Students (3,032), Unplaced Students (4,193), Placement Rate (41.97%), Average CGPA (7.70).
* **6 Selectable Cohort Dimensions**:
  * CGPA Ranges (< 6.5, 6.5 - 7.5, 7.5 - 8.5, 8.5 - 9.0, 9.0+)
  * Internships Completed (0, 1, 2+)
  * Technical Projects (0, 1, 2, 3+)
  * Placement Training (Completed vs Not Completed)
  * Aptitude Score Tiers (Tier 1 to Tier 4)
  * Workshops & Certifications (0, 1, 2, 3+)
* **Interactive Visualizations**:
  * Dual-metric cohort success rate bar chart with percentage labels.
  * Stacked outcome distribution chart (Placed vs Not Placed volume).
* **Statistical Performance Matrix**: Granular breakdown of student counts, placed counts, placement rate, average CGPA, and average aptitude scores per cohort.
* **Empirical Observations Callout**: Automated institutional insights derived directly from historical data (e.g. impact of $\ge 2$ internships yielding > 80% placement rates).
