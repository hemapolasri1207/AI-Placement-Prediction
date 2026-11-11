"""
Skill Gap Analysis and Personalized Skill Recommendations Module
AI-Based Placement Prediction and Skill Gap Analysis System (Day 3)
"""

from typing import Dict, List, Any


# -----------------------------------------------------------------------------
# 1. REQUIRED SKILLS PER JOB ROLE
# -----------------------------------------------------------------------------
ROLE_REQUIREMENTS: Dict[str, List[str]] = {
    "Java Developer": [
        "Java",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Spring Boot",
        "Hibernate",
        "REST API",
        "Git",
    ],
    "Python Developer": [
        "Python",
        "SQL",
        "HTML",
        "CSS",
        "Django",
        "Flask",
        "REST API",
        "Git",
    ],
    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "SQL",
        "REST API",
        "Git",
    ],
    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Statistics",
        "Pandas",
        "NumPy",
        "Data Visualization",
    ],
    "Machine Learning Engineer": [
        "Python",
        "SQL",
        "Statistics",
        "NumPy",
        "Pandas",
        "Scikit-learn",
        "Machine Learning",
        "Deep Learning",
    ],
}


# -----------------------------------------------------------------------------
# 2. CURATED OFFICIAL & TRUSTED LEARNING RESOURCES
# -----------------------------------------------------------------------------
SKILL_RESOURCES: Dict[str, Dict[str, str]] = {
    "Java": {
        "title": "Oracle Official Java Documentation & Tutorials",
        "url": "https://docs.oracle.com/en/java/",
        "platform": "Oracle Docs",
        "category": "Core Language",
        "description": "Master object-oriented programming, JVM memory management, and modern Java features.",
    },
    "Python": {
        "title": "Python Official Documentation & Tutorials",
        "url": "https://docs.python.org/3/tutorial/",
        "platform": "Python.org",
        "category": "Core Language",
        "description": "Learn syntax, data structures, OOP, modules, and standard libraries.",
    },
    "SQL": {
        "title": "PostgreSQL & SQL Tutorial by W3Schools",
        "url": "https://www.w3schools.com/sql/",
        "platform": "W3Schools / PostgreSQL",
        "category": "Database & Querying",
        "description": "Practice relational database design, joins, subqueries, indexing, and aggregations.",
    },
    "HTML": {
        "title": "MDN Web Docs - HTML: Markup Language",
        "url": "https://developer.mozilla.org/en-US/docs/Web/HTML",
        "platform": "MDN Web Docs",
        "category": "Frontend Foundations",
        "description": "Understand semantic tags, document hierarchy, forms, and web accessibility.",
    },
    "CSS": {
        "title": "MDN Web Docs - CSS: Cascading Style Sheets",
        "url": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "platform": "MDN Web Docs",
        "category": "Frontend Foundations",
        "description": "Master Flexbox, CSS Grid, media queries, animations, and modern responsive design.",
    },
    "JavaScript": {
        "title": "MDN Web Docs - JavaScript Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "platform": "MDN Web Docs",
        "category": "Frontend Foundations",
        "description": "Learn ES6+ syntax, asynchronous JavaScript (Promises/Async-Await), DOM manipulation, and event handling.",
    },
    "Spring Boot": {
        "title": "Spring Boot Official Guides & Documentation",
        "url": "https://spring.io/guides",
        "platform": "Spring.io",
        "category": "Backend Framework",
        "description": "Build production-grade Java enterprise microservices, dependency injection, and REST endpoints.",
    },
    "Hibernate": {
        "title": "Hibernate ORM Official User Guide",
        "url": "https://hibernate.org/orm/documentation/",
        "platform": "Hibernate.org",
        "category": "Backend Framework",
        "description": "Object-relational mapping (ORM), entity lifecycle, JPQL queries, and caching mechanisms.",
    },
    "REST API": {
        "title": "RESTful API Design Best Practices - MDN",
        "url": "https://developer.mozilla.org/en-US/docs/Glossary/REST",
        "platform": "MDN Web Docs",
        "category": "Web Services & Architecture",
        "description": "Design stateless HTTP endpoints, CRUD operations, status codes, and API security.",
    },
    "Git": {
        "title": "Pro Git Book (Official Documentation)",
        "url": "https://git-scm.com/book/en/v2",
        "platform": "Git-SCM",
        "category": "DevOps & Version Control",
        "description": "Branching strategies, merging, pull requests, rebasing, and GitHub collaboration.",
    },
    "Django": {
        "title": "Django Web Framework Official Documentation",
        "url": "https://docs.djangoproject.com/en/stable/",
        "platform": "Django Project",
        "category": "Backend Framework",
        "description": "Rapid web development with MTV architecture, built-in ORM, admin panel, and user auth.",
    },
    "Flask": {
        "title": "Flask Web Development User's Guide",
        "url": "https://flask.palletsprojects.com/",
        "platform": "Pallets Projects",
        "category": "Backend Framework",
        "description": "Lightweight WSGI Python micro-framework for building performant microservices and APIs.",
    },
    "React": {
        "title": "React Official Documentation (Learn React)",
        "url": "https://react.dev/learn",
        "platform": "React.dev",
        "category": "Frontend Framework",
        "description": "Component-based architecture, JSX, hooks (useState, useEffect), state management, and Virtual DOM.",
    },
    "Excel": {
        "title": "Microsoft Excel Official Video Training & Guides",
        "url": "https://support.microsoft.com/en-us/excel",
        "platform": "Microsoft Support",
        "category": "Business Intelligence",
        "description": "Advanced formulas (XLOOKUP, INDEX/MATCH), Pivot Tables, Power Query, and business dashboards.",
    },
    "Power BI": {
        "title": "Microsoft Learn - Power BI Documentation",
        "url": "https://learn.microsoft.com/en-us/power-bi/",
        "platform": "Microsoft Learn",
        "category": "Business Intelligence",
        "description": "Data modeling, DAX calculations, interactive reporting, and enterprise BI dashboards.",
    },
    "Statistics": {
        "title": "Khan Academy - Probability and Statistics",
        "url": "https://www.khanacademy.org/math/statistics-probability",
        "platform": "Khan Academy",
        "category": "Mathematical Foundations",
        "description": "Descriptive statistics, hypothesis testing, p-values, distributions, and inferential analysis.",
    },
    "Pandas": {
        "title": "Pandas Data Analysis Official User Guide",
        "url": "https://pandas.pydata.org/docs/user_guide/index.html",
        "platform": "PyData.org",
        "category": "Data Engineering & Analytics",
        "description": "DataFrame wrangling, cleaning missing values, grouping, merging, and time-series analysis.",
    },
    "NumPy": {
        "title": "NumPy Numerical Computing User Guide",
        "url": "https://numpy.org/doc/stable/user/index.html",
        "platform": "NumPy.org",
        "category": "Data Engineering & Analytics",
        "description": "N-dimensional array operations, vectorization, linear algebra, and fast numeric computations.",
    },
    "Data Visualization": {
        "title": "Plotly Python Interactive Graphing Libraries",
        "url": "https://plotly.com/python/",
        "platform": "Plotly / Matplotlib",
        "category": "Data Presentation",
        "description": "Create publication-ready visual storytelling with Matplotlib, Seaborn, and interactive Plotly charts.",
    },
    "Scikit-learn": {
        "title": "Scikit-Learn Machine Learning in Python",
        "url": "https://scikit-learn.org/stable/user_guide.html",
        "platform": "Scikit-Learn.org",
        "category": "Machine Learning",
        "description": "Supervised & unsupervised algorithms, cross-validation, hyperparameter tuning, and evaluation metrics.",
    },
    "Machine Learning": {
        "title": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course",
        "platform": "Google Developers",
        "category": "Machine Learning",
        "description": "Foundations of regression, classification, bias-variance tradeoff, regularization, and model deployment.",
    },
    "Deep Learning": {
        "title": "PyTorch Official Deep Learning Tutorials",
        "url": "https://pytorch.org/tutorials/",
        "platform": "PyTorch.org",
        "category": "Machine Learning",
        "description": "Neural networks, backpropagation, CNNs for computer vision, RNNs/Transformers for NLP, and GPU acceleration.",
    },
}


# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS FOR SKILL GAP COMPARISON
# -----------------------------------------------------------------------------
def get_available_roles() -> List[str]:
    """Returns the list of available job roles."""
    return list(ROLE_REQUIREMENTS.keys())


def get_all_unique_skills() -> List[str]:
    """Returns a sorted list of all unique skills across all job roles."""
    all_skills = set()
    for role_skills in ROLE_REQUIREMENTS.values():
        all_skills.update(role_skills)
    return sorted(list(all_skills))


def get_required_skills(role: str) -> List[str]:
    """Returns the list of required skills for a given job role."""
    return ROLE_REQUIREMENTS.get(role, [])


def analyze_skill_gap(role: str, student_skills: List[str]) -> Dict[str, Any]:
    """
    Compares student's selected skills against the requirements for a job role.

    Returns a structured dictionary:
    - role: Chosen job role
    - total_required: Total count of required skills
    - matched_skills: List of skills the student possesses
    - missing_skills: List of skills the student needs to learn
    - additional_skills: Skills the student has that aren't strictly required
    - match_percentage: float (matched / total_required * 100)
    - readiness_level: String description of readiness tier
    - readiness_color: Hex color for UI badges
    - learning_recommendations: Tailored actionable roadmap
    - resource_links: Dict of learning resource details for missing skills
    """
    required_skills = get_required_skills(role)

    # Normalize for comparison
    student_skills_clean = [s.strip() for s in student_skills if s.strip()]
    student_skills_lower = {s.lower(): s for s in student_skills_clean}

    matched_skills: List[str] = []
    missing_skills: List[str] = []

    for req in required_skills:
        if req.lower() in student_skills_lower:
            matched_skills.append(req)
        else:
            missing_skills.append(req)

    # Additional skills that the student has which are not in the role's required list
    req_lower_set = {req.lower() for req in required_skills}
    additional_skills = [
        s for s in student_skills_clean if s.lower() not in req_lower_set
    ]

    total_required = len(required_skills)
    match_percentage = (
        round((len(matched_skills) / total_required) * 100, 1)
        if total_required > 0
        else 0.0
    )

    # Readiness tiers
    if match_percentage >= 80.0:
        readiness_level = "High Placement Readiness"
        readiness_badge = "Excellent Fit"
        readiness_color = "#059669"  # Green
        readiness_summary = (
            "Your profile closely matches the technical requirements for this role! "
            "Focus on polishing your missing skills and building real-world projects."
        )
    elif match_percentage >= 50.0:
        readiness_level = "Moderate Placement Readiness"
        readiness_badge = "Moderate Fit"
        readiness_color = "#D97706"  # Amber
        readiness_summary = (
            "You have established foundational competencies, but several key industry skills "
            "are missing. Following a structured 4-to-8 week upskilling plan is strongly advised."
        )
    else:
        readiness_level = "Foundational Stage (Skill Gap Identified)"
        readiness_badge = "Critical Upskilling Needed"
        readiness_color = "#DC2626"  # Red
        readiness_summary = (
            "Significant skill gaps exist for this role. Prioritize core foundational tools "
            "and frameworks before applying for active placement drives."
        )

    # Generate personalized learning recommendations
    recommendations = generate_personalized_recommendations(role, matched_skills, missing_skills)

    # Resource links for missing skills
    missing_resources = {}
    for skill in missing_skills:
        if skill in SKILL_RESOURCES:
            missing_resources[skill] = SKILL_RESOURCES[skill]
        else:
            missing_resources[skill] = {
                "title": f"{skill} Official Guide & Documentation",
                "url": f"https://www.google.com/search?q={skill}+official+documentation+tutorial",
                "platform": "Online Documentation",
                "category": "Technical Skill",
                "description": f"Learn foundational and advanced concepts in {skill}.",
            }

    return {
        "role": role,
        "total_required": total_required,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "match_percentage": match_percentage,
        "readiness_level": readiness_level,
        "readiness_badge": readiness_badge,
        "readiness_color": readiness_color,
        "readiness_summary": readiness_summary,
        "recommendations": recommendations,
        "missing_resources": missing_resources,
    }


def generate_personalized_recommendations(
    role: str, matched_skills: List[str], missing_skills: List[str]
) -> List[Dict[str, str]]:
    """
    Generates a structured, phased learning roadmap based on missing competencies.
    """
    if not missing_skills:
        return [
            {
                "phase": "Phase 1: Advanced Mastery & System Design",
                "action": f"You have acquired all {len(matched_skills)} core technical skills for {role}!",
                "detail": "Proceed to end-to-end full stack / production system architecture, performance optimization, and mock technical interviews.",
            },
            {
                "phase": "Phase 2: Portfolio & Capstone Projects",
                "action": "Build 2 industry-grade capstone repositories on GitHub.",
                "detail": "Include comprehensive README files, automated CI/CD workflows, unit testing, and deployed live demonstrations.",
            },
            {
                "phase": "Phase 3: Placement Drive Strategy",
                "action": "Solve domain interview challenges and behavioral preparation.",
                "detail": "Focus on data structures, algorithmic complexity, architectural trade-offs, and resume storytelling.",
            },
        ]

    recommendations = []

    # Identify foundational vs framework vs tools
    foundational_pool = {"Python", "Java", "SQL", "HTML", "CSS", "Statistics", "Excel"}
    framework_pool = {"Spring Boot", "Hibernate", "Django", "Flask", "React", "Scikit-learn", "Pandas", "NumPy", "Deep Learning", "Machine Learning"}
    tools_pool = {"Git", "REST API", "Power BI", "Data Visualization", "JavaScript"}

    foundational_missing = [s for s in missing_skills if s in foundational_pool]
    framework_missing = [s for s in missing_skills if s in framework_pool]
    tools_missing = [s for s in missing_skills if s in tools_pool]
    other_missing = [s for s in missing_skills if s not in foundational_pool and s not in framework_pool and s not in tools_pool]

    # Step 1: Foundations
    if foundational_missing:
        recommendations.append({
            "phase": "Phase 1: Master Foundational Requisites (Weeks 1 - 3)",
            "action": f"Focus immediately on core syntax and concepts: {', '.join(foundational_missing)}.",
            "detail": "Strong fundamentals are critical prerequisites during initial technical screening and written coding tests.",
        })
    else:
        recommendations.append({
            "phase": "Phase 1: Foundational Checkpoint (Completed ✅)",
            "action": "You have solid foundational language and database coverage.",
            "detail": "Maintain syntax fluency through daily competitive programming or practical coding practice.",
        })

    # Step 2: Frameworks & Core Tech
    if framework_missing:
        recommendations.append({
            "phase": "Phase 2: Framework & Applied Development (Weeks 4 - 6)",
            "action": f"Implement hands-on applications using: {', '.join(framework_missing)}.",
            "detail": "Recruiters evaluate candidates on their ability to build practical solutions with modern industry frameworks.",
        })

    # Step 3: Tools, Collaboration & Deployment
    missing_devops_tools = tools_missing + other_missing
    if missing_devops_tools:
        recommendations.append({
            "phase": "Phase 3: Tooling, Workflows & APIs (Weeks 7 - 8)",
            "action": f"Adopt standard industry tools and protocols: {', '.join(missing_devops_tools)}.",
            "detail": "Version control (Git) and RESTful API integrations are mandatory skills across almost all modern hiring assessments.",
        })

    # Capstone recommendation
    recommendations.append({
        "phase": "Phase 4: Capstone Portfolio Project",
        "action": f"Build a comprehensive {role} showcase project incorporating your learned skills.",
        "detail": "Document your repository with clear setup instructions, architecture diagrams, and highlight it on your resume.",
    })

    return recommendations
