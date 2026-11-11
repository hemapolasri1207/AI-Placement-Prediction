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
    initial_sidebar_state="collapsed",
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

        /* Use the horizontal navigation; hide the unused sidebar */
        section[data-testid="stSidebar"] { display: none; }
        .block-container { padding-top: 1.5rem; max-width: 1500px; }
        .modern-card { height: auto !important; min-height: 250px; overflow: visible; }
        .modern-card h4 { line-height: 1.3; overflow-wrap: anywhere; }
        .modern-card p, .modern-card li { line-height: 1.55; overflow-wrap: anywhere; }

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
            """)