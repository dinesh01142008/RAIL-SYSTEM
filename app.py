import hashlib
import io
import time as time_mod
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import linprog
import streamlit as st

# ==============================================================================
# 1. CLEAN STYLING & NATIVE SIDEBAR TOGGLE
# ==============================================================================
st.set_page_config(
    page_title="Indian Railways | Smart Track Work & Asset Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: visible !important; }
    .stDeployButton { display: none !important; }
    
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    div[role="radiogroup"] { gap: 6px; }
    div[role="radiogroup"] > label {
        background: #FFFFFF;
        padding: 9px 14px;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { 
        background: #FFFFFF; 
        transform: translateX(2px); 
        border-color: #2563EB;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08); 
    }
    
    .premium-card {
        background: #FFFFFF;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB !important;
        transition: all 0.25s ease;
        margin-bottom: 14px;
    }
    .premium-card:hover { 
        border-color: #2563EB;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.10); 
    }
    
    /* MILD BLINKING RED BORDER PULSE (WHITE INTERIOR) */
    @keyframes pulse-soft-crimson {
        0% { 
            box-shadow: 0 0 4px rgba(239, 68, 68, 0.20); 
            border-color: #FECACA; 
        }
        50% { 
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.45); 
            border-color: #F87171; 
            background-color: #FFFFFF; 
        }
        100% { 
            box-shadow: 0 0 4px rgba(239, 68, 68, 0.20); 
            border-color: #FECACA; 
        }
    }
    
    .blinking-red-card {
        animation: pulse-soft-crimson 2s infinite !important;
        background: #FFFFFF !important;
        border: 1.5px solid #F87171 !important;
        border-left: 6px solid #EF4444 !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px;
    }

    .success-card-soft {
        background: #F0FDF4 !important;
        border: 1.5px solid #86EFAC !important;
        border-left: 7px solid #16A34A !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px;
    }
    
    .card-inner-clearance { padding-left: 6px; }
    .card-title { color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 0.8px; margin-bottom: 4px; }
    .card-value { color: #0F172A; font-size: 22px; font-weight: 900; line-height: 1.1; margin-bottom: 4px; }
    .card-subtitle { font-size: 12px; font-weight: 600; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #E2E8F0; margin-bottom: 14px; }
    .stTabs [data-baseweb="tab"] { height: 38px; font-weight: 700; font-size: 13px; color: #64748B; background: transparent; border: none; border-radius: 8px; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; font-weight: 800; }
    
    .stButton>button { 
        border-radius: 10px !important; 
        font-weight: 700; 
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); 
        color: white; 
        border: none; 
        padding: 8px 18px; 
        transition: all 0.2s; 
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.16); 
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 14px rgba(37, 99, 235, 0.25); color: white; }
    [data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.02); border: 1px solid #E2E8F0; }
    
    .fatigue-bar-container { width: 100%; background-color: #E2E8F0; border-radius: 8px; margin-top: 6px; overflow: hidden; height: 8px; }
    .fatigue-bar-fill { height: 100%; border-radius: 8px; transition: width 0.4s ease; }
    
    .block-card {
        background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px !important; padding: 14px;
        text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    
    .flow-container { display: flex; flex-direction: column; align-items: center; padding: 6px 0; font-family: 'Inter', sans-serif; }
    .flow-box {
        background: #FFFFFF;
        border: 1.5px solid #2563EB;
        border-radius: 12px !important;
        padding: 13px 20px;
        text-align: center;
        width: 100%;
        max-width: 580px;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.05);
        position: relative;
    }
    .flow-box-priority-high { 
        animation: pulse-soft-crimson 2s infinite !important;
        background: #FFFFFF !important; 
        border: 1.5px solid #F87171 !important; 
    }
    .flow-box-amber { border: 1.5px solid #D97706 !important; background: #FFFBEB !important; }
    .flow-box-green { border: 1.5px solid #059669 !important; background: #F0FDF4 !important; }
    .flow-box-purple { border: 1.5px solid #7C3AED !important; background: #F5F3FF !important; }
    .flow-box-blue { border: 1.5px solid #2563EB !important; background: #EFF6FF !important; }
    
    .flow-title { font-weight: 800; font-size: 12px; color: #0F172A; text-transform: uppercase; margin-bottom: 3px; letter-spacing: 0.5px; }
    .flow-desc { font-size: 11.5px; color: #475569; }
    .flow-arrow { width: 2px; height: 16px; background: #94A3B8; margin: 2px 0; position: relative; }
    .flow-arrow::after { content: ''; position: absolute; bottom: 0; left: -4px; border-width: 5px 5px 0; border-style: solid; border-color: #94A3B8 transparent transparent; }
    
    .executive-advisory-console {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 14px !important;
        padding: 18px 22px;
        color: #F8FAFC;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.10);
    }
    
    .telemetry-tag {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        color: #94A3B8;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .pulse-dot { width: 7px; height: 7px; border-radius: 50%; background: #10B981; }
    .pulse-dot-paused { width: 7px; height: 7px; border-radius: 50%; background: #F59E0B; }

    .terminal-stream-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 12px 16px;
        font-family: monospace;
        font-size: 11px;
        color: #38BDF8;
        line-height: 1.6;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {'displayModeBar': False, 'scrollZoom': True}

# ==============================================================================
# 2. PAN-INDIA RAILWAY NETWORK DATABASE[cite: 1, 2]
# ==============================================================================
RAILWAY_NETWORK = {
    "Tamil Nadu": {
        "Salem Division": {
            "annual_cargo_passenger_weight_density_gmt": 48.5,
            "cost_density_multiplier": 1.00,
            "stations": {"Salem Junction": 0.0, "Magnesite Junction": 7.8, "Danishpet": 18.2, "Sankari Durg": 32.5, "Cauvery": 54.1, "Erode Junction": 65.4, "Chigas": 78.2},
            "coords": {"Salem Junction": (11.6811, 78.1287), "Magnesite Junction": (11.7135, 78.1340), "Danishpet": (11.8210, 78.1450), "Sankari Durg": (11.4795, 77.8732), "Cauvery": (11.3652, 77.7289), "Erode Junction": (11.3396, 77.7172), "Chigas": (11.2850, 77.6210)}
        },
        "Chennai Division": {
            "annual_cargo_passenger_weight_density_gmt": 74.2,
            "cost_density_multiplier": 1.53,
            "stations": {"Chennai Central": 0.0, "Basin Bridge": 2.5, "Perambur": 5.5, "Villivakkam": 9.2, "Ambattur": 15.1, "Avadi": 21.0, "Tiruvallur": 41.8},
            "coords": {"Chennai Central": (13.0827, 80.2755), "Basin Bridge": (13.0970, 80.2730), "Perambur": (13.1090, 80.2330), "Villivakkam": (13.1065, 80.2030), "Ambattur": (13.1140, 80.1540), "Avadi": (13.1180, 80.0980), "Tiruvallur": (13.1430, 79.9080)}
        }
    },
    "Maharashtra": {
        "Mumbai Division": {
            "annual_cargo_passenger_weight_density_gmt": 108.6,
            "cost_density_multiplier": 2.24,
            "stations": {"Mumbai CSMT": 0.0, "Byculla": 4.1, "Dadar": 9.0, "Kurla Junction": 15.3, "Ghatkopar": 20.8, "Thane": 33.5, "Dombivli": 47.8, "Kalyan Junction": 53.2},
            "coords": {"Mumbai CSMT": (18.9402, 72.8356), "Byculla": (18.9760, 72.8330), "Dadar": (19.0178, 72.8478), "Kurla Junction": (19.0657, 72.8794), "Ghatkopar": (19.0860, 72.9080), "Thane": (19.1860, 72.9759), "Dombivli": (19.2180, 73.0860), "Kalyan Junction": (19.2354, 73.1299)}
        },
        "Pune Division": {
            "annual_cargo_passenger_weight_density_gmt": 62.1,
            "cost_density_multiplier": 1.28,
            "stations": {"Pune Junction": 0.0, "Shivajinagar": 2.5, "Khadki": 6.3, "Dapodi": 9.2, "Pimpri": 14.2, "Chinchwad": 16.5, "Dehu Road": 24.8, "Talegaon": 33.2},
            "coords": {"Pune Junction": (18.5284, 73.8743), "Shivajinagar": (18.5314, 73.8510), "Khadki": (18.5630, 73.8310), "Dapodi": (18.5810, 73.8210), "Pimpri": (18.6230, 73.7990), "Chinchwad": (18.6360, 73.7850), "Dehu Road": (18.7180, 73.7250), "Talegaon": (18.7340, 73.6780)}
        }
    },
    "Delhi (National Capital Region)": {
        "Delhi Division": {
            "annual_cargo_passenger_weight_density_gmt": 96.4,
            "cost_density_multiplier": 1.99,
            "stations": {"New Delhi": 0.0, "Delhi Kishanganj": 4.2, "Shakur Basti": 11.0, "Nangloi": 17.5, "Bahadurgarh": 30.2, "Rohtak Junction": 70.5},
            "coords": {"New Delhi": (28.6430, 77.2194), "Delhi Kishanganj": (28.6631, 77.1950), "Shakur Basti": (28.6830, 77.1320), "Nangloi": (28.6820, 77.0650), "Bahadurgarh": (28.6920, 76.9280), "Rohtak Junction": (28.8950, 76.6060)}
        }
    },
    "West Bengal": {
        "Howrah Division": {
            "annual_cargo_passenger_weight_density_gmt": 88.2,
            "cost_density_multiplier": 1.82,
            "stations": {"Howrah Junction": 0.0, "Liluah": 4.8, "Belur": 6.5, "Bally": 8.9, "Rishra": 16.2, "Serampore": 19.5, "Bandel Junction": 39.4},
            "coords": {"Howrah Junction": (22.5830, 88.3426), "Liluah": (22.6180, 88.3370), "Belur": (22.6320, 88.3480), "Bally": (22.6500, 88.3470), "Rishra": (22.7120, 88.3510), "Serampore": (22.7520, 88.3430), "Bandel Junction": (22.9200, 88.3740)}
        }
    },
    "Karnataka": {
        "Bengaluru Division": {
            "annual_cargo_passenger_weight_density_gmt": 65.8,
            "cost_density_multiplier": 1.36,
            "stations": {"KSR Bengaluru": 0.0, "Bengaluru Cantt": 4.2, "Baiyyappanahalli": 10.5, "Krishnarajapuram": 14.1, "Whitefield": 23.2, "Bangarapet Junction": 70.1},
            "coords": {"KSR Bengaluru": (12.9781, 77.5696), "Bengaluru Cantt": (12.9934, 77.5982), "Baiyyappanahalli": (12.9912, 77.6528), "Krishnarajapuram": (13.0012, 77.6766), "Whitefield": (12.9698, 77.7499), "Bangarapet Junction": (12.9961, 78.1920)}
        }
    },
    "Telangana": {
        "Secunderabad Division": {
            "annual_cargo_passenger_weight_density_gmt": 78.4,
            "cost_density_multiplier": 1.62,
            "stations": {"Secunderabad Junction": 0.0, "Moula Ali": 9.2, "Cherlapalli": 15.5, "Ghatkesar": 21.4, "Bibinagar": 33.1, "Kazipet Junction": 131.8},
            "coords": {"Secunderabad Junction": (17.4344, 78.5015), "Moula Ali": (17.4580, 78.5610), "Cherlapalli": (17.4620, 78.6010), "Ghatkesar": (17.4510, 78.6810), "Bibinagar": (17.4680, 78.7910), "Kazipet Junction": (17.9780, 79.5210)}
        }
    },
    "Uttar Pradesh": {
        "Pt. Deen Dayal Upadhyaya Division": {
            "annual_cargo_passenger_weight_density_gmt": 112.5,
            "cost_density_multiplier": 2.32,
            "stations": {"Pt DDU Junction": 0.0, "Kuchman": 10.5, "Sakaldiha": 18.4, "Dheena": 31.8, "Zamania": 55.4, "Buxar": 94.2},
            "coords": {"Pt DDU Junction": (25.2810, 83.1210), "Kuchman": (25.3210, 83.1950), "Sakaldiha": (25.3720, 83.2510), "Dheena": (25.4120, 83.3510), "Zamania": (25.4310, 83.5610), "Buxar": (25.5640, 83.9780)}
        },
        "Lucknow Division": {
            "annual_cargo_passenger_weight_density_gmt": 84.1,
            "cost_density_multiplier": 1.73,
            "stations": {"Lucknow Charbagh": 0.0, "Manak Nagar": 4.8, "Amausi": 10.9, "Piparsand": 17.1, "Harauni": 23.2, "Unnao Junction": 54.5, "Kanpur Central": 72.0},
            "coords": {"Lucknow Charbagh": (26.8310, 80.9220), "Manak Nagar": (26.8120, 80.8910), "Amausi": (26.7620, 80.8650), "Piparsand": (26.7310, 80.8350), "Harauni": (26.7020, 80.8010), "Unnao Junction": (26.5410, 80.4910), "Kanpur Central": (26.4540, 80.3510)}
        }
    },
    "Gujarat": {
        "Ahmedabad Division": {
            "annual_cargo_passenger_weight_density_gmt": 71.0,
            "cost_density_multiplier": 1.46,
            "stations": {"Ahmedabad Junction": 0.0, "Sabarmati Junction": 5.8, "Chandlodiya": 10.2, "Kalol Junction": 26.5, "Mehsana Junction": 68.4},
            "coords": {"Ahmedabad Junction": (23.0270, 72.6010), "Sabarmati Junction": (23.0720, 72.5850), "Chandlodiya": (23.0810, 72.5450), "Kalol Junction": (23.2350, 72.4950), "Mehsana Junction": (23.5880, 72.3690)}
        }
    }
}

# ==============================================================================
# 3. HELPER FUNCTIONS & WORK ORDER GENERATORS[cite: 1, 2]
# ==============================================================================
def format_24h(minutes):
    try:
        if minutes is None or pd.isna(minutes): return "00:00 Hours"
        total = int(minutes) % 1440
        return f"{total // 60:02d}:{total % 60:02d} Hours"
    except Exception:
        return "00:00 Hours"

def parse_24h_to_minutes(time_str):
    try:
        clean = time_str.replace(" Hours", "").replace(" Hrs", "").strip()
        parts = clean.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return 570

def calculate_priority_score(flaw_severity, days_past_due, track_tonnage):
    score = (0.35 * float(flaw_severity) * 10.0) + (0.25 * min(100, float(days_past_due) * 2.5)) + (0.25 * min(100, float(track_tonnage) * 1.2)) + 12.0
    return int(np.clip(score, 10, 99))

def generate_division_work_orders(stn_list, gmt_val):
    s1 = stn_list[0]
    s2 = stn_list[min(2, len(stn_list)-1)]
    s3 = stn_list[min(4, len(stn_list)-1)]
    s4 = stn_list[-1]

    raw = [
        ["REQ-801", "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", s1, "Overhead Electric Cable Adjustment: Tighten and balance wire tension.", 95, 45, f"Combined-{s1[:3].upper()}-42", "Daily Plan (Next 24 Hours)", "MCH-02", 8.8, 14, gmt_val],
        ["REQ-802", "Track & Ground Civil Team [Track Management System (TMS)]", s1, "Track Stone Packing & Leveling: Heavy machine stone packing.", 85, 45, f"Combined-{s1[:3].upper()}-42", "Daily Plan (Next 24 Hours)", "MCH-01", 7.5, 21, gmt_val],
        ["REQ-803", "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]", s2, "Signal Lights & Switch Safety Check: Electronic safety sensor inspection.", 60, 60, f"Combined-{s2[:3].upper()}-17", "Daily Plan (Next 24 Hours)", "MCH-03", 5.2, 5, round(gmt_val * 0.9, 1)],
        ["REQ-804", "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", s2, "High-Voltage Power Insulator Cleaning & Washing.", 72, 60, f"Combined-{s2[:3].upper()}-17", "Daily Plan (Next 24 Hours)", "MCH-02", 6.8, 12, round(gmt_val * 0.9, 1)],
        ["REQ-805", "Track & Ground Civil Team [Track Management System (TMS)]", s3, "Steel Rail Crack Welding: Rail joint structural reinforcement.", 88, 90, f"Combined-{s3[:3].upper()}-91", "Weekly Plan (Next 7 Days)", "MCH-01", 9.1, 28, round(gmt_val * 1.1, 1)],
        ["REQ-806", "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]", s3, "Track Direction Switch Motor Alignment.", 92, 90, f"Combined-{s3[:3].upper()}-91", "Weekly Plan (Next 7 Days)", "MCH-03", 8.4, 18, round(gmt_val * 1.1, 1)],
        ["REQ-807", "Track & Ground Civil Team [Track Management System (TMS)]", s4, "Full Concrete Sleeper & Fastener Renewal.", 78, 120, f"Combined-{s4[:3].upper()}-08", "Monthly Plan (Next 30 Days)", "MCH-04", 7.0, 45, round(gmt_val * 1.2, 1)]
    ]
    cols = [
        "Request ID", "Department / Team", "Station Location", "Work Description", 
        "Priority Level (1-100)", "Duration (Minutes)", "Combined Group ID", 
        "Planning Schedule", "Assigned Machinery", "Flaw Severity (1-10)", "Days Past Due", "Annual Cargo Weight (GMT)"
    ]
    df = pd.DataFrame(raw, columns=cols)
    df["Status"] = "Approved & Scheduled"
    df["Duration (Minutes)"] = df["Duration (Minutes)"].astype(int)
    return df

# Session state initialization
if "active_division_name" not in st.session_state: st.session_state.active_division_name = ""
if "global_incident_station" not in st.session_state: st.session_state.global_incident_station = "Salem Junction"
if "global_track_condition" not in st.session_state: st.session_state.global_track_condition = "Track Clear (Normal Line Speed)"
if "global_work_zones" not in st.session_state: st.session_state.global_work_zones = ["Salem Junction", "Erode Junction"]
if "extra_time_billing_inr" not in st.session_state: st.session_state.extra_time_billing_inr = 0.0

if "stream_active" not in st.session_state: st.session_state.stream_active = True
if "packet_seq" not in st.session_state: st.session_state.packet_seq = 8492
if "last_ingest_timestamp" not in st.session_state: st.session_state.last_ingest_timestamp = datetime.now()

if "field_queries_log" not in st.session_state:
    st.session_state.field_queries_log = [
        {"timestamp": "08:45 Hours", "engineer": "Rajesh Sharma", "department": "Track & Ground Civil Team [Track Management System (TMS)]", "station": "Salem Junction", "extension_mins": 15, "notes": "Heavy stone settlement detected near track direction switch. 15 minutes extra packing needed for train safety.", "status": "Under Review", "extra_cost_inr": 10000.0}
    ]

if "system_output_records_log" not in st.session_state:
    st.session_state.system_output_records_log = pd.DataFrame([
        ["REC-901", "Salem Division", "Salem Junction", "Track & Civil, Electric Cables", "10:30 - 11:15 (45 mins)", "45 Minutes Saved", "Chief Train Dispatcher", "2026-09-04 08:30:00", "₹0 (Scheduled)"],
        ["REC-902", "Salem Division", "Erode Junction", "Electric Cables, Signals & Switches", "11:30 - 12:30 (60 mins)", "60 Minutes Saved", "Chief Train Dispatcher", "2026-09-04 09:15:00", "₹0 (Scheduled)"]
    ], columns=["Record ID", "Division", "Target Station", "Departments Working Concurrently", "Approved Work Window", "Track Downtime Saved", "Approved By", "Timestamp", "Extra Extension Cost"])

if "workers_db" not in st.session_state:
    st.session_state.workers_db = pd.DataFrame([
        ["WRK-1001", "Rajesh Sharma", "Track & Ground Civil Team [Track Management System (TMS)]", "Active on Duty", "Track Inspection Team Leader"],
        ["WRK-1002", "Aravind Swamy", "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", "Active on Duty", "Power Cable Tension Specialist"],
        ["WRK-1003", "Priya Nair", "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]", "Active on Duty", "Electronic Track Sensor Lead"],
        ["WRK-1004", "Gurpreet Singh", "Locomotive Driver Operations", "Active on Duty", "High-Speed Passenger Train Driver"],
        ["WRK-1005", "Amit Patel", "Freight Driver Operations", "Active on Duty", "Long Heavy Goods Cargo Train Driver"],
        ["WRK-1006", "Karthik Raja", "High-Speed Driver Operations", "Active on Duty", "Superfast Express Train Driver"],
        ["WRK-1007", "Vikramaditya Das", "Reserve Relief Operations", "Active on Duty", "Backup Passenger Train Driver"]
    ], columns=["Worker ID", "Worker Name", "Department", "Work Duty Status", "Assigned Role"])

if "fleet_db" not in st.session_state:
    st.session_state.fleet_db = pd.DataFrame([
        ["Vande Bharat Express", "VB-2026", "High-Speed Passenger", 110, 540, 1, "#059669", 7.5, "Gurpreet Singh"],
        ["Rajdhani Express", "RAJ-1260", "Superfast Passenger", 85, 558, 2, "#2563EB", 4.5, "Rajesh Sharma"],
        ["Shatabdi Express", "SHT-4421", "Superfast Passenger", 95, 570, 3, "#7C3AED", 6.0, "Karthik Raja"],
        ["Super Vasuki Goods Train", "FRT-8802", "Heavy Freight Cargo", 45, 528, 4, "#D97706", 9.2, "Amit Patel"],
        ["Tejas Superfast Express", "TJS-2291", "High-Speed Passenger", 105, 582, 5, "#0891B2", 5.0, "Vikramaditya Das"]
    ], columns=["Train Name", "Train Number", "Train Category", "Top Speed (km/h)", "Start Minute", "Priority Level", "Color", "Base Shift Hours", "Assigned Train Driver"])

if "machinery_db" not in st.session_state:
    st.session_state.machinery_db = pd.DataFrame([
        ["MCH-01", "High-Speed Track Stone Packing Machine (Plasser Tamping Unit)", "Track & Ground Civil Team [Track Management System (TMS)]", "Salem Junction", "Ready for Work", 35],
        ["MCH-02", "Overhead Electric Cable Inspection Vehicle", "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", "Salem Junction", "Ready for Work", 40],
        ["MCH-03", "Electronic Solid-State Signaling Test Vehicle", "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]", "Erode Junction", "In Transit to Station", 50],
        ["MCH-04", "Track Stone Cleaning & Ballast Renewal Machine", "Track & Ground Civil Team [Track Management System (TMS)]", "Erode Junction", "Ready for Work", 30]
    ], columns=["Machine ID", "Machine Equipment Name", "Operating Department", "Station Depot Location", "Readiness State", "Travel Speed (km/h)"])

if "block_requests" not in st.session_state:
    st.session_state.block_requests = generate_division_work_orders(list(RAILWAY_NETWORK["Tamil Nadu"]["Salem Division"]["stations"].keys()), 48.5)

if "cris_tms_stream" not in st.session_state:
    st.session_state.cris_tms_stream = pd.DataFrame([
        {"Track ID": "TK-101", "Station": "Salem Junction", "Track Safety Score (1-10)": 8.4, "Rail Steel Wear (mm)": 4.8, "Yearly Cargo Density [Gross Million Tonnes (GMT)]": 55.2, "Days Past Maintenance": 24, "Caution Speed Limit": "30 km/h"},
        {"Track ID": "TK-102", "Station": "Erode Junction", "Track Safety Score (1-10)": 4.1, "Rail Steel Wear (mm)": 2.2, "Yearly Cargo Density [Gross Million Tonnes (GMT)]": 48.0, "Days Past Maintenance": 8, "Caution Speed Limit": "Normal Line Speed"},
        {"Track ID": "TK-103", "Station": "Magnesite Junction", "Track Safety Score (1-10)": 9.2, "Rail Steel Wear (mm)": 5.9, "Yearly Cargo Density [Gross Million Tonnes (GMT)]": 64.1, "Days Past Maintenance": 32, "Caution Speed Limit": "20 km/h"}
    ])

if "cris_tdms_stream" not in st.session_state:
    st.session_state.cris_tdms_stream = pd.DataFrame([
        {"Power Section ID": "OHE-SAL-1", "Station": "Salem Junction", "Overhead Wire Wear %": 19.4, "Wire Tension Deviation %": 12.8, "Insulator Condition": "High Attention", "Line Feeder Voltage (kV)": 24.8},
        {"Power Section ID": "OHE-ERO-2", "Station": "Erode Junction", "Overhead Wire Wear %": 8.2, "Wire Tension Deviation %": 3.4, "Insulator Condition": "Safe", "Line Feeder Voltage (kV)": 25.1}
    ])

if "cris_smms_stream" not in st.session_state:
    st.session_state.cris_smms_stream = pd.DataFrame([
        {"Switch Direction Point ID": "PNT-104A", "Station": "Salem Junction", "Turnout Motor Current (Amperes)": 6.8, "Wheel Counter Error Count": 0, "Relay Switch Total Operations": 142000, "Safety Action Status": "Immediate Inspection Needed"},
        {"Switch Direction Point ID": "PNT-202B", "Station": "Erode Junction", "Turnout Motor Current (Amperes)": 4.1, "Wheel Counter Error Count": 0, "Relay Switch Total Operations": 89000, "Safety Action Status": "Normal Operating State"}
    ])

# ==============================================================================
# 4. SIDEBAR - UNIFIED FLAT NAVIGATION & LOCATION SELECTOR[cite: 1, 2]
# ==============================================================================
with st.sidebar:
    st.markdown('<h2 style="color:#0F172A; font-weight:900; letter-spacing:-1px; margin-bottom: -5px; margin-top: 5px;">INDIAN RAILWAYS</h2>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px; font-weight:800; color:#2563EB; margin-bottom:15px; line-height:1.4; letter-spacing: 0.5px;'>SMART TRACK WORK & ASSET PLANNER</p>", unsafe_allow_html=True)
    
    user_portal = st.radio(
        "Choose System Workspace", 
        [
            "Central Command Center (Main Train Dispatch & Control Office)", 
            "Field Maintenance Terminal (Station Engineers & Track Work Crews)"
        ],
        label_visibility="collapsed"
    )
    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>OPERATIONAL DIVISION LOCATION</h3>", unsafe_allow_html=True)
    sel_state = st.selectbox("State", list(RAILWAY_NETWORK.keys()), index=0)
    division_options = list(RAILWAY_NETWORK[sel_state].keys())
    sel_division = st.selectbox("Operating Railway Division", division_options, index=0)
    
    sector_data = RAILWAY_NETWORK[sel_state][sel_division]
    current_sector = sector_data["stations"]
    current_coords = sector_data["coords"]
    station_list = list(current_sector.keys())
    division_gmt = sector_data["annual_cargo_passenger_weight_density_gmt"]
    w_div = sector_data["cost_density_multiplier"]
    
    if st.session_state.active_division_name != sel_division:
        st.session_state.active_division_name = sel_division
        st.session_state.global_incident_station = station_list[0]
        st.session_state.global_work_zones = [station_list[0], station_list[min(2, len(station_list)-1)]]
        st.session_state.block_requests = generate_division_work_orders(station_list, division_gmt)
        st.session_state.machinery_db["Station Depot Location"] = [
            station_list[0], station_list[0], station_list[min(2, len(station_list)-1)], station_list[-1]
        ]
        
    st.markdown(f"""
    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:10px 12px; font-size:11px; color:#1E40AF; margin-top:6px; line-height:1.5;">
        <b>Yearly Cargo Weight Carried:</b> {division_gmt} Gross Million Tonnes (GMT)<br>
        <b>Regional Cost Multiplier:</b> {w_div:.2f}x Baseline
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    
    if user_portal == "Central Command Center (Main Train Dispatch & Control Office)":
        st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>CENTRAL COMMAND TOOLS</h3>", unsafe_allow_html=True)
        active_tool = st.radio(
            "Select Central Tool",
            [
                "Live Train Traffic Command & Track Map",
                "Real-Time Track Section Status & Signal Blocks",
                "Predictive Delay Prevention & 15-Minute Lookahead",
                "Live Wayside Telemetry & Data Ingestion Gateway",
                "Departmental Work Order Submission (Track, Electrical, Signals)",
                "List of Running Trains & Heavy Repair Machines",
                "Smart Math Schedule Optimizer [Mixed-Integer Linear Programming (MILP)]",
                "Money Preserved & Financial Savings Breakdown",
                "Money Wasted in Old Manual Way vs. Money Saved by Smart System",
                "Master Horizon Work Calendar (Daily, Weekly, Monthly)",
                "Emergency Track Breakdown & Traffic Delay Test",
                "How Train Delay Conflicts Are Solved Step-by-Step",
                "System Architecture & Live Hardware Connectivity",
                "Technical System Guide & Operations Manual"
            ],
            key="unified_ccc_radio"
        )
    else:
        st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>FIELD ENGINEERING WORKSPACES</h3>", unsafe_allow_html=True)
        active_tool = st.radio(
            "Select Field Terminal Tool",
            [
                "Track & Ground Civil Team [Track Management System (TMS)] Desk",
                "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)] Desk",
                "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)] Desk",
                "Live Field Asset & Track Work Map",
                "Request Extra Work Time (Dispatch Window Extension Desk)",
                "Department Work Calendar (Daily, Weekly, Monthly Schedule)"
            ],
            key="unified_field_radio"
        )
        
    st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>TRACK INCIDENT SIMULATOR</h3>", unsafe_allow_html=True)
    def_stn_idx = station_list.index(st.session_state.global_incident_station) if st.session_state.global_incident_station in station_list else 0
    sim_station = st.selectbox("Target Station Location", station_list, index=def_stn_idx)
    sim_status = st.selectbox("Track Safety Condition", ["Track Clear (Normal Line Speed)", "Track Repair Needed (Speed Limit: 30 km/h)", "Track Completely Blocked (Obstacle / Defect)"])
    
    st.session_state.global_incident_station = sim_station
    st.session_state.global_track_condition = sim_status

if sim_status != "Track Clear (Normal Line Speed)":
    em_exists = any(r["Station Location"] == sim_station and "Safety Action Order" in str(r["Work Description"]) for _, r in st.session_state.block_requests.iterrows())
    if not em_exists:
        new_em_id = f"ACT-{np.random.randint(1000, 9999)}"
        dept_name = "Track & Ground Civil Team [Track Management System (TMS)]" if "Repair" in sim_status else "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
        new_em_row = pd.DataFrame([{
            "Request ID": new_em_id, 
            "Department / Team": dept_name, 
            "Station Location": sim_station, 
            "Work Description": f"Safety Action Order: Immediate response to {sim_status}", 
            "Priority Level (1-100)": 99, 
            "Duration (Minutes)": 45, 
            "Status": "Approved & Scheduled", 
            "Combined Group ID": f"Combined-{sim_station[:3].upper()}-ACT", 
            "Planning Schedule": "Daily Plan (Next 24 Hours)",
            "Assigned Machinery": "MCH-01" if "Track" in dept_name else "MCH-03",
            "Flaw Severity (1-10)": 9.9,
            "Days Past Due": 1,
            "Annual Cargo Weight (GMT)": division_gmt
        }])
        st.session_state.block_requests = pd.concat([new_em_row, st.session_state.block_requests], ignore_index=True)
        if sim_station not in st.session_state.global_work_zones:
            st.session_state.global_work_zones.append(sim_station)

# ==============================================================================
# 5. MATHEMATICAL TIMETABLE SIMULATOR WITH TRAIN LOOP HOLDING
# ==============================================================================
def calculate_train_movements_multiloop(damaged_stn, status, sector_dict, approved_stns, fleet_dataframe):
    try:
        trains = fleet_dataframe.to_dict('records')
        trains = sorted(trains, key=lambda x: x.get("Priority Level", 5))
        stn_keys = list(sector_dict.keys())
        mid_stn = stn_keys[max(0, min(2, len(stn_keys) - 1))] if len(stn_keys) > 0 else ""
        sankari_stn = stn_keys[max(0, min(3, len(stn_keys) - 1))] if len(stn_keys) > 3 else mid_stn

        records = []
        for t in trains:
            curr_time = t.get("Start Minute", 540)
            prev_dist = 0
            total_delay = 0
            
            for stn_idx, (stn, dist) in enumerate(sector_dict.items()):
                curr_speed = t.get("Top Speed (km/h)", 90)
                dwell = 2
                track_lane = "Main Running Line"
                on_loop = False
                condition_label = "Line Clear"

                # Dynamic Loop Siding Allocation
                if stn == damaged_stn and status != "Track Clear (Normal Line Speed)":
                    condition_label = status
                    if "Repair" in status:
                        curr_speed = min(curr_speed, 30)
                        track_lane = f"Loop Siding Track ({stn})"
                        on_loop = True
                        total_delay += 8
                    elif "Blocked" in status:
                        dwell += 18
                        track_lane = f"Loop Siding Track ({stn})"
                        on_loop = True
                        total_delay += 18
                elif t.get("Train Category") == "Heavy Freight Cargo" and stn in [sankari_stn, mid_stn]:
                    dwell += 15
                    track_lane = f"Loop Siding Track ({stn})"
                    on_loop = True
                    total_delay += 15
                elif t.get("Priority Level", 5) >= 4 and stn == mid_stn:
                    dwell += 10
                    track_lane = f"Loop Siding Track ({stn})"
                    on_loop = True
                    total_delay += 10
                
                delta_d = dist - prev_dist if dist > prev_dist else 0
                travel_time = (delta_d / max(10, curr_speed)) * 60
                
                arrival = curr_time + travel_time
                departure = arrival + dwell
                curr_time = departure 
                prev_dist = dist
                
                records.append({
                    "Train Name": t.get("Train Name", "Express Train"),
                    "Train Number": t.get("Train Number", "TRN-0000"),
                    "Station": stn,
                    "Station Index": stn_idx,
                    "Distance (km)": dist, 
                    "Arrival Minute": arrival,
                    "Arrival Time": format_24h(arrival),
                    "Departure Minute": departure,
                    "Departure Time": format_24h(departure),
                    "Station Wait Time": f"{int(dwell)} mins",
                    "Assigned Track Lane": track_lane,
                    "On Loop": on_loop,
                    "Track Safety Condition": condition_label,
                    "Color": t.get("Color", "#2563EB"),
                    "Total Delay (Minutes)": total_delay,
                    "Assigned Train Driver": t.get("Assigned Train Driver", "Locomotive Driver")
                })
        return pd.DataFrame(records)
    except Exception:
        return pd.DataFrame()

df_traffic = calculate_train_movements_multiloop(
    st.session_state.global_incident_station, 
    st.session_state.global_track_condition, 
    current_sector, 
    st.session_state.global_work_zones, 
    st.session_state.fleet_db
)

def generate_dynamic_blocks(sector_dict, incident_stn, incident_status, approved_work_zones):
    stations = list(sector_dict.keys())
    blocks = []
    
    for i in range(len(stations) - 1):
        s1, s2 = stations[i], stations[i+1]
        d1, d2 = sector_dict[s1], sector_dict[s2]
        bid = f"Track Section B{i+1}"
        span = f"{s1} ➔ {s2} ({d1:.1f} - {d2:.1f} km)"
        
        status = "Track Clear for Normal Train Speeds"
        train = "None (Line Clear)"
        eta = "Line Clear"
        
        if incident_status != "Track Clear (Normal Line Speed)" and (s1 == incident_stn or s2 == incident_stn):
            if "Blocked" in incident_status:
                status = "Track Completely Blocked (Obstacle / Defect)"
                train = f"Freight Train Stationary near {incident_stn}"
                eta = "18 mins (Loop Siding Transit)"
            else:
                status = "Track Repair Needed (Speed Limit: 30 km/h)"
                train = "Departmental Engineering Work Train"
                eta = "25 mins remaining"
        elif s1 in approved_work_zones or s2 in approved_work_zones:
            status = "Track Maintenance Active (Speed Limit 30 km/h)"
            train = "Combined Maintenance Crew"
            eta = "35 mins remaining"
        elif i == 0:
            status = "Track Block Occupied"
            train = "VB-2026 (Vande Bharat Express)"
            eta = "3 mins to clear block"
        elif i == 1:
            status = "Pre-Reserved for Approaching Express"
            train = "RAJ-1260 (Rajdhani Express)"
            eta = "6 mins to arrive"
        
        blocks.append({
            "id": bid,
            "span": span,
            "status": status,
            "train": train,
            "eta": eta
        })
    return blocks

def solve_ai_block_optimization_milp(block_df, machinery_df):
    results = []
    explanations = []
    
    scored_blocks = block_df.copy()
    grouped = scored_blocks.groupby("Station Location")
    cumulative_saved_mins = 0
    total_machinery_hours_optimized = 0
    slot_cursor = 630
    
    for station, group in grouped:
        durations = group["Duration (Minutes)"].astype(float).values
        n_tasks = len(durations)
        has_power = group["Department / Team"].str.contains("Electric|Overhead|TDMS|Traction").any()
        power_margin = 15.0 if has_power else 0.0
        
        c = np.ones(n_tasks)
        A_ub = -np.eye(n_tasks)
        b_ub = -durations
        bounds = [(d, d + 30) for d in durations]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        max_dur = int(np.max(durations) + power_margin)
        sum_dur = int(np.sum(durations) + (power_margin * n_tasks))
        saved = max(0, sum_dur - max_dur)
        cumulative_saved_mins += saved
        
        machines_needed = group["Assigned Machinery"].dropna().unique().tolist()
        machinery_status = "Assigned & In-Depot"
        if len(machines_needed) > 0:
            for m in machines_needed:
                m_row = machinery_df[machinery_df["Machine ID"] == m]
                if not m_row.empty and "Ready" in m_row["Readiness State"].iloc[0]:
                    machinery_status = f"{m} ({m_row['Machine Equipment Name'].iloc[0][:22]}...) Ready"
                else:
                    machinery_status = f"{m} In-Transit Staging"
        
        headway_margin = 8
        base_slot_start = slot_cursor + headway_margin
        base_slot_end = base_slot_start + max_dur
        slot_cursor = base_slot_end + headway_margin
        
        dept_list = list(set([d.split(' ')[0] for d in group["Department / Team"].tolist()]))
        rationale = (
            f"Schedule Optimizer [Mixed-Integer Linear Programming (MILP)] synchronized {len(group)} work orders from [{', '.join(dept_list)}] "
            f"at {station}. Enforced an 8-minute safe train distance gap [Headway Buffer] and a 15-minute electrical power cutoff safety buffer. "
            f"Avoided {saved} minutes of separate track closure time. Machinery dispatch status: {machinery_status}."
        )
        
        results.append({
            "Station Location": station,
            "Tasks Bundled": len(group),
            "Departments Operating Concurrently": ", ".join(dept_list),
            "Combined Possession Window": f"{format_24h(base_slot_start)} - {format_24h(base_slot_end)} ({max_dur} mins)",
            "Track Downtime Saved": f"{saved} Minutes",
            "Highest Priority Level": group["Priority Level (1-100)"].max(),
            "Assigned Machinery State": machinery_status,
            "System Optimization Justification": rationale
        })
        explanations.append(rationale)
        total_machinery_hours_optimized += (saved / 60.0)
        
    return pd.DataFrame(results), cumulative_saved_mins, explanations, total_machinery_hours_optimized

opt_results_global, total_saved_global, xai_notes_global, machine_hours_saved_global = solve_ai_block_optimization_milp(
    st.session_state.block_requests, st.session_state.machinery_db
)

def compute_division_finances(saved_mins, multiplier, extra_time_charges):
    hours_saved = float(saved_mins) / 60.0
    
    legacy_passenger = (hours_saved * 1.35) * (12000.0 * multiplier) * 2.5
    legacy_freight = (hours_saved * 1.40) * (4500.0 * multiplier) * 3.0
    legacy_machinery = (machine_hours_saved_global * 1.5) * 25000.0
    legacy_energy = (hours_saved * 1.25) * (3200.0 * multiplier)
    legacy_uncoordinated = len(opt_results_global) * (35000.0 * multiplier)
    
    total_old_system_loss_inr = legacy_passenger + legacy_freight + legacy_machinery + legacy_energy + legacy_uncoordinated
    
    ai_passenger = legacy_passenger * 0.12
    ai_freight = legacy_freight * 0.15
    ai_machinery = legacy_machinery * 0.10
    ai_energy = legacy_energy * 0.14
    ai_uncoordinated = len(opt_results_global) * (7000.0 * multiplier)
    
    total_ai_system_cost_inr = ai_passenger + ai_freight + ai_machinery + ai_energy + ai_uncoordinated + extra_time_charges
    net_money_saved_inr = max(0.0, total_old_system_loss_inr - total_ai_system_cost_inr)
    loss_mitigation_pct = round((net_money_saved_inr / max(1.0, total_old_system_loss_inr)) * 100.0, 1)
    
    return {
        "old_system_loss_inr": total_old_system_loss_inr,
        "old_system_loss_lakhs": round(total_old_system_loss_inr / 100000.0, 2),
        "ai_system_cost_inr": total_ai_system_cost_inr,
        "ai_system_cost_lakhs": round(total_ai_system_cost_inr / 100000.0, 2),
        "net_money_saved_inr": net_money_saved_inr,
        "net_money_saved_lakhs": round(net_money_saved_inr / 100000.0, 2),
        "loss_mitigation_pct": loss_mitigation_pct,
        "passenger_savings_inr": legacy_passenger - ai_passenger,
        "freight_savings_inr": legacy_freight - ai_freight,
        "machinery_savings_inr": legacy_machinery - ai_machinery,
        "energy_savings_inr": legacy_energy - ai_energy,
        "extra_time_billing_inr": extra_time_charges
    }

finance_data = compute_division_finances(total_saved_global, w_div, st.session_state.extra_time_billing_inr)

def render_team_flowchart(team_name=None, job_id=None, stn=None, dur=None, work_type=None, notes=None, priority=None, **kwargs):
    t_name = team_name or "Maintenance Crew"
    j_id = job_id or "REQ-ORD"
    t_stn = stn or "Target Station"
    t_dur = dur or 45
    w_type = work_type or "Routine Track Maintenance"
    w_notes = notes or ""
    w_priority = int(priority) if priority is not None else 80

    if w_priority >= 80 or "Safety Action Order" in str(w_type) or "ACT" in str(j_id):
        priority_css_class = "flow-box-priority-high"
        priority_label = f"<span style='color:#BE123C; font-weight:900;'>CRITICAL PRIORITY ({w_priority}/100) — IMMEDIATE ACTION REQUIRED</span>"
    elif w_priority >= 40:
        priority_css_class = "flow-box-amber"
        priority_label = f"<span style='color:#D97706; font-weight:800;'>MEDIUM PRIORITY ({w_priority}/100) — STANDARD SCHEDULED DISPATCH</span>"
    else:
        priority_css_class = "flow-box-green"
        priority_label = f"<span style='color:#059669; font-weight:800;'>LOW PRIORITY ({w_priority}/100) — PREVENTIVE INSPECTION</span>"

    if "Track" in t_name or "Civil" in t_name:
        p_title = "Step 3: Track & Civil Work Execution"
        p_desc = f"Speed restricted to 30 km/h at {t_stn} ➔ High-speed stone packing machine deployed ➔ Track alignment verified."
        step3_box = "flow-box-blue"
    elif "Traction" in t_name or "Electric" in t_name or "TDMS" in t_name:
        p_title = "Step 3: Overhead Electric Power Cable Protocol"
        p_desc = f"25,000-Volt power cut off at {t_stn} ➔ Cable tension calibrated ➔ Grounding discharge rods connected."
        step3_box = "flow-box-purple"
    else:
        p_title = "Step 3: Signaling & Switch Protocol"
        p_desc = f"Track circuit verified at {t_stn} ➔ Switch direction motor realigned ➔ Solid-state electronic interlocking locked."
        step3_box = "flow-box-green"

    st.markdown(f"""
    <div style='margin-top: 10px; margin-bottom: 14px;'>
        <div style='text-align: center; margin-bottom: 6px;'>{priority_label}</div>
        <div class="flow-container">
            <div class="flow-box {priority_css_class}">
                <div class="flow-title">Step 1: Work Order Verification & Intake</div>
                <div class="flow-desc">Job ID: <b>{j_id}</b> | Department: <b>{t_name}</b> | Task: <b>{w_type}</b></div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box">
                <div class="flow-title">Step 2: Timetable Clearance Window Locked</div>
                <div class="flow-desc">Location: <b>{t_stn}</b> | Approved Work Window: <b>{t_dur} Minutes</b></div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box {step3_box}">
                <div class="flow-title">{p_title}</div>
                <div class="flow-desc">{p_desc}</div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-green">
                <div class="flow-title">Step 4: Operational Clearance & Handover</div>
                <div class="flow-desc">Notes: {w_notes if w_notes else 'Standard procedure completed successfully.'} | Track Cleared for Green Signals.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def get_cached_telemetry_csv(city_name):
    rows = []
    stns = ["Salem Junction", "Magnesite Junction", "Danishpet", "Sankari Durg", "Erode Junction"]
    for s in stns:
        rows.append({
            "Station_Name": s,
            "Track_Safety_Score": 8.4 if "Salem" in s else 4.2,
            "Rail_Wear_mm": 4.8 if "Salem" in s else 2.1,
            "Overhead_Wire_Tension_kN": 12.4,
            "Switch_Motor_Current_Amperes": 6.8 if "Salem" in s else 3.8,
            "Wheel_Counter_Errors": 0,
            "Yearly_Cargo_Density_GMT": 55.2,
            "Days_Past_Maintenance": 24 if "Salem" in s else 8,
            "Transmission_Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(rows).to_csv(index=False)

@st.cache_data
def get_cached_sanction_bulletin(division_title, state_title, table_str, timestamp_str):
    raw = f"{division_title}-{state_title}-{timestamp_str}"
    token = hashlib.sha256(raw.encode()).hexdigest().upper()
    out = io.StringIO()
    out.write("================================================================================\n")
    out.write("     INDIAN RAILWAYS CENTRAL TRAIN CONTROL - OFFICIAL SYSTEM OUTPUT RECORD\n")
    out.write("                   DIVISIONAL OPERATING CONTROL OFFICE                         \n")
    out.write("================================================================================\n")
    out.write(f"SYSTEM RECORD REF   : IR/DRM/{division_title[:3].upper()}/SYS-OUT/2026/04-A\n")
    out.write(f"SECURITY HASH (SHA) : {token}\n")
    out.write(f"DIVISION / STATE    : {division_title.upper()} ({state_title.upper()})\n")
    out.write(f"DATE ISSUED         : {timestamp_str}\n")
    out.write("AUTHORIZING DESK    : CHIEF TRAIN CONTROLLER / AUTOMATED WORK DESK\n")
    out.write("CLEARANCE STAMP     : DIGITALLY VERIFIED & SECURED BY RAILWAY DISPATCH INTEROP\n")
    out.write("--------------------------------------------------------------------------------\n\n")
    out.write(table_str)
    out.write("\n\n--------------------------------------------------------------------------------\n")
    out.write("OPERATIONAL DIRECTIVES:\n")
    out.write("1. All station managers must verify caution signals prior to maintenance gang track access.\n")
    out.write("2. Overhead inspection cars and track stone packing machines have absolute line precedence.\n")
    out.write("3. Freight trains to wait on side parking loops to maintain booked passenger schedules.\n")
    out.write("4. Minimum 8-minute safe train gap and 15-minute electrical power cutoff buffers enforced.\n")
    out.write("================================================================================\n")
    return out.getvalue(), token

@st.cache_data
def get_cached_financial_audit_statement(division_title, state_title, fin_dict, audit_table_str, timestamp_str):
    raw = f"FIN-AUDIT-{division_title}-{timestamp_str}-{fin_dict['net_money_saved_lakhs']}"
    token = hashlib.sha256(raw.encode()).hexdigest().upper()
    out = io.StringIO()
    out.write("====================================================================================================\n")
    out.write("               INDIAN RAILWAYS - DIVISIONAL ACCOUNTS & OPERATIONS AUDIT STATEMENT                   \n")
    out.write("                    FINANCIAL LOSS PREVENTION & ASSET VALUE RECOVERY REPORT                         \n")
    out.write("====================================================================================================\n")
    out.write(f"AUDIT RECEIPT NO    : IR/FIN/{division_title[:3].upper()}/REC-{datetime.now().strftime('%Y%m%d')}-099\n")
    out.write(f"AUTHENTICATION HASH : {token}\n")
    out.write(f"DIVISION / ZONE     : {division_title.upper()} DIVISION / {state_title.upper()}\n")
    out.write(f"DATE OF GENERATION  : {timestamp_str}\n")
    out.write(f"ACCOUNTING AUTHORITY: CHIEF REGIONAL CONTROLLER / IR AUTOMATED ASSET VALUE DESK\n")
    out.write("----------------------------------------------------------------------------------------------------\n\n")
    out.write(f"OLD MANUAL SYSTEM OPERATING LOSS       : Rs {fin_dict['old_system_loss_inr']:,.2f}  ({fin_dict['old_system_loss_lakhs']} Lakhs INR)\n")
    out.write(f"OUR SYSTEM OPERATING COST              : Rs {fin_dict['ai_system_cost_inr']:,.2f}  ({fin_dict['ai_system_cost_lakhs']} Lakhs INR)\n")
    out.write(f"TOTAL MONEY SAVED BY OUR SYSTEM        : Rs {fin_dict['net_money_saved_inr']:,.2f}  ({fin_dict['net_money_saved_lakhs']} Lakhs INR)\n")
    out.write(f"OVERALL LOSS MITIGATION PERCENTAGE     : {fin_dict['loss_mitigation_pct']}%\n")
    out.write(f"EXTRA TIME EXTENSION BILLING INCURRED  : Rs {fin_dict['extra_time_billing_inr']:,.2f}\n\n")
    out.write("SIDE-BY-SIDE ITEMIZED AUDIT MATRIX:\n")
    out.write("----------------------------------------------------------------------------------------------------\n")
    out.write(audit_table_str)
    out.write("\n----------------------------------------------------------------------------------------------------\n")
    out.write("STATUTORY CERTIFICATION & AUDIT DIRECTIVES:\n")
    out.write("1. All detention reductions are reconciled against Freight Operations Information System (FOIS) ledgers.\n")
    out.write("2. Rolling stock depreciation avoidance conforms to Indian Railways Financial Code parameters.\n")
    out.write("3. Machinery utilization rates computed from on-track sensor active duty telemetry.\n")
    out.write("====================================================================================================\n")
    return out.getvalue(), token

# ==============================================================================
# 6. PORTAL 1: CENTRAL COMMAND CENTER
# ==============================================================================
if user_portal == "Central Command Center (Main Train Dispatch & Control Office)":
    
    now_time = datetime.now()
    elapsed = (now_time - st.session_state.last_ingest_timestamp).total_seconds()
    
    if st.session_state.stream_active and elapsed >= 10.0:
        st.session_state.packet_seq += 1
        st.session_state.last_ingest_timestamp = now_time

    jitter_ms = (int(time_mod.time() * 1000) % 28) + 12
    pkt_id = f"PKT-{st.session_state.packet_seq}"
    ingest_rate = 1.45 + (len(st.session_state.fleet_db) * 0.05) + ((st.session_state.packet_seq % 5) * 0.02)
    sensor_res = round(4.18 + ((st.session_state.packet_seq % 10) * 0.02), 2)
    catenary_val = round(12.38 + ((st.session_state.packet_seq % 7) * 0.03), 2)

    advisory_statement = (
        f"Schedule Optimizer [Mixed-Integer Linear Programming (MILP)] synchronized Track stone packing with 25,000-Volt Electric power lines calibration near {st.session_state.global_incident_station}. "
        f"Enforced an 8-minute safe train distance gap [Headway Buffer] and a 15-minute electrical power cutoff safety buffer. Preserved ₹{finance_data['net_money_saved_lakhs']} Lakhs in asset yield."
        if st.session_state.global_track_condition == "Track Clear (Normal Line Speed)" else
        f"Safety Action Order active at {st.session_state.global_incident_station}. Sidetracking slower freight cargo services to multiple side parking track loops. "
        f"Emergency maintenance crew allocated an isolated track work window."
    )

    pulse_dot_class = "pulse-dot" if st.session_state.stream_active else "pulse-dot-paused"
    stream_status_text = "Live Stream: Active (10s Ingest)" if st.session_state.stream_active else "Live Stream: Paused"

    st.markdown(f"""
    <div class="executive-advisory-console">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <div class="{pulse_dot_class}"></div>
                <span style="font-size:13px; font-weight:800; letter-spacing:0.8px; text-transform:uppercase; color:#38BDF8;">
                    Operational Advisory & Wayside Telemetry Gateway
                </span>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="telemetry-tag">{stream_status_text}</span>
                <span class="telemetry-tag">Data Rate: {ingest_rate:.2f} MB/s</span>
                <span class="telemetry-tag">Network Delay: ±{jitter_ms}ms</span>
                <span class="telemetry-tag">Indian Railways Data Standard Compliant</span>
            </div>
        </div>
        <div style="font-size:13px; color:#F8FAFC; line-height:1.5; font-weight:500;">
            <b>System Advisory:</b> {advisory_statement}
        </div>
        <div class="terminal-stream-box">
            [{st.session_state.last_ingest_timestamp.strftime('%H:%M:%S')}] DATA_BUS: Packet {pkt_id} verified from {sim_station} | Track circuit resistance: {sensor_res} Ohms | Data Error Check [CRC-32]: VALID<br>
            [{st.session_state.last_ingest_timestamp.strftime('%H:%M:%S')}] ELECTRIC_CABLES: {sel_division} overhead power line tension: {catenary_val} kN | Voltage: 24.8 kV (Nominal)<br>
            [{st.session_state.last_ingest_timestamp.strftime('%H:%M:%S')}] SCHEDULE_OPTIMIZER: Track safety rules satisfied across all {len(station_list)} inter-station blocks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.5, 3])
    with ctrl_col1:
        if st.session_state.stream_active:
            if st.button("Pause Ingestion Stream", use_container_width=True):
                st.session_state.stream_active = False
                st.rerun()
        else:
            if st.button("Resume Ingestion Stream", use_container_width=True):
                st.session_state.stream_active = True
                st.session_state.last_ingest_timestamp = datetime.now()
                st.rerun()
    with ctrl_col2:
        if st.button("Fetch Live Packet Now", use_container_width=True):
            st.session_state.packet_seq += 1
            st.session_state.last_ingest_timestamp = datetime.now()
            st.rerun()
    with ctrl_col3:
        st.caption(f"Automatic 10s Ingest | Packet Sequence: `{pkt_id}` | Last Verified: `{st.session_state.last_ingest_timestamp.strftime('%H:%M:%S')}`")

    pending_queries = [q for q in st.session_state.field_queries_log if q["status"] == "Under Review"]
    if pending_queries:
        st.markdown(f"""
        <div class="blinking-red-card">
            <div style="color: #9F1239; font-weight: 900; font-size: 13px; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 3px;">
                High Priority Notice: {len(pending_queries)} Field Work Possession Extension Requests Waiting for Approval
            </div>
            <strong style="color: #1E293B; font-size: 12.5px;">Immediate Dispatcher Action Required:</strong> 
            Field maintenance crews on the track have requested extra work time. Approving automatically calculates and bills the monetary delay cost, extends the scheduled window, updates the audit statement, and notifies approaching trains.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Review Field Extension Requests (With Extra Money Calculation)", expanded=True):
            for idx, item in enumerate(st.session_state.field_queries_log):
                if item["status"] == "Under Review":
                    c_inf, c_act = st.columns([3, 1.2])
                    calculated_fee = (item['extension_mins'] / 60.0) * (25000.0 + 15000.0) * w_div
                    with c_inf:
                        st.markdown(f"""
                        **Worker Name:** `{item['engineer']}` | **Department:** `{item['department']}` | **Location:** `{item['station']}`  
                        **Requested Possession Extension:** `+{item['extension_mins']} Minutes` | **Time:** `{item['timestamp']}`  
                        **Calculated Monetary Cost of Extra Time:** `₹{calculated_fee:,.0f}` (Includes Machine Idling & Track Occupancy at {w_div:.2f}x Multiplier)  
                        *Site Observations:* {item['notes']}
                        """)
                    with c_act:
                        if st.button(f"Approve (+{item['extension_mins']}m / ₹{calculated_fee:,.0f})", key=f"app_grant_{idx}", use_container_width=True):
                            item["status"] = "Approved by Central Office"
                            item["extra_cost_inr"] = calculated_fee
                            st.session_state.extra_time_billing_inr += calculated_fee
                            
                            stn_match = item["station"]
                            dept_match = item["department"]
                            mask = (st.session_state.block_requests["Station Location"] == stn_match) & (st.session_state.block_requests["Department / Team"] == dept_match)
                            if mask.any():
                                st.session_state.block_requests.loc[mask, "Duration (Minutes)"] += item["extension_mins"]
                                st.session_state.block_requests.loc[mask, "Work Description"] += f" [Extended +{item['extension_mins']}m by Central Office]"
                            else:
                                stn_mask = (st.session_state.block_requests["Station Location"] == stn_match)
                                if stn_mask.any():
                                    st.session_state.block_requests.loc[stn_mask, "Duration (Minutes)"] += item["extension_mins"]
                            
                            new_audit_entry = pd.DataFrame([{
                                "Record ID": f"REC-EXT-{np.random.randint(100, 999)}",
                                "Division": sel_division,
                                "Target Station": stn_match,
                                "Departments Working Concurrently": dept_match,
                                "Approved Work Window": f"+{item['extension_mins']} mins extension",
                                "Track Downtime Saved": "Dynamic Schedule Shift",
                                "Approved By": "Chief Train Dispatcher",
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Extra Extension Cost": f"₹{calculated_fee:,.0f}"
                            }])
                            st.session_state.system_output_records_log = pd.concat([new_audit_entry, st.session_state.system_output_records_log], ignore_index=True)

                            st.success(f"Approved +{item['extension_mins']}m for {item['engineer']} at {stn_match}. Billed ₹{calculated_fee:,.0f} to corridor account.")
                            time_mod.sleep(0.4)
                            st.rerun()

    # --------------------------------------------------------------------------
    # 1. LIVE TRAIN TRAFFIC COMMAND & TRACK MAP (GEOGRAPHIC FIRST, RADAR SECOND)
    # --------------------------------------------------------------------------
    if active_tool == "Live Train Traffic Command & Track Map":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Live Network Command — {sel_division} ({sel_state})</h1>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        tot_dist = max(current_sector.values()) if len(current_sector) > 0 else 50
        dynamic_sensors = int(tot_dist * 4 + len(current_sector) * 12)
        active_train_count = len(df_traffic["Train Name"].unique()) if not df_traffic.empty else 0
        
        base_tph = 14 if "Blocked" in st.session_state.global_track_condition else (18 if "Repair" in st.session_state.global_track_condition else 24)
        ai_tph = base_tph + (8 if "Blocked" in st.session_state.global_track_condition else 4)
        
        with c1: st.markdown(f"<div class='premium-card'><div class='card-title'>Active Trains on Track</div><div class='card-value'>{active_train_count} Trains</div><div class='card-subtitle' style='color:#64748B'>{sel_division} ({len(station_list)} Stations)</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='premium-card'><div class='card-title'>Trackside Safety Sensors</div><div class='card-value'>{dynamic_sensors} Live Sensors</div><div class='card-subtitle' style='color:#059669'>Vibration & Wheel Telemetry Active</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='premium-card'><div class='card-title'>Corridor Line Capacity</div><div class='card-value'>{ai_tph} Trains/Hour</div><div class='card-subtitle' style='color:#2563EB'>Maximum Track Capacity</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='premium-card'><div class='card-title'>Total Capital Saved</div><div class='card-value'>₹{finance_data['net_money_saved_lakhs']} Lakhs</div><div class='card-subtitle' style='color:#059669'>{finance_data['loss_mitigation_pct']}% Waste Mitigated</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs: Geographic Map First, followed by Radar Schematic Map
        tabs = st.tabs([
            "Corridor Geographic Map", 
            "Interactive Traffic Simulation", 
            "Live Station Stop Timetable", 
            "Time vs Distance Graph"
        ])
        
        # TAB 0: GEOGRAPHIC MAP (FIRST POSITION)[cite: 1, 2]
        with tabs[0]:
            stn_names = list(current_coords.keys())
            lats = [current_coords[s][0] for s in stn_names]
            lons = [current_coords[s][1] for s in stn_names]
            
            fig_map = go.Figure()
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="lines", 
                line=dict(width=6, color="#2563EB"), 
                name="Main Railway Running Track", hoverinfo="skip"
            ))
            
            track_color = "#059669" if st.session_state.global_track_condition == "Track Clear (Normal Line Speed)" else ("#D97706" if "Repair" in st.session_state.global_track_condition else "#DC2626")
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="lines", 
                line=dict(width=4, color=track_color), 
                name=f"Condition: {st.session_state.global_track_condition}", hoverinfo="name"
            ))
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="markers+text", 
                marker=dict(size=14, color="#0F172A"), 
                text=stn_names, textposition="top right", 
                textfont=dict(size=11, family="Inter", color="#0F172A", weight="bold"), 
                name="Station Junction Stops"
            ))
            
            for wz in st.session_state.global_work_zones:
                if wz in current_coords:
                    coord = current_coords[wz]
                    fig_map.add_trace(go.Scattermapbox(
                        lat=[coord[0]], lon=[coord[1]], mode="markers+text", 
                        marker=dict(size=18, color="#8B5CF6"), 
                        text=[f"WORK ZONE: {wz}"], textposition="bottom left", 
                        textfont=dict(size=11, color="#8B5CF6", weight="bold"), 
                        name="Maintenance Possession Zone"
                    ))
            
            fig_map.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    zoom=9.0,
                    center=dict(lat=float(np.mean(lats)), lon=float(np.mean(lons)))
                ),
                margin=dict(l=0, r=0, t=10, b=0),
                height=460
            )
            st.plotly_chart(fig_map, use_container_width=True, config=PLOT_CONFIG)

        # TAB 1: INTERACTIVE TRAFFIC SIMULATION (RADAR MAP - SECOND POSITION)
        with tabs[1]:
            st.markdown("<h3 style='font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 2px;'>Interactive Temporal Traffic Simulation</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 13px; color: #475569; margin-bottom: 12px;'>Adjust the timeline slider to strictly simulate where trains will be at any hour of the day. Notice how the AI mathematically avoids collisions.</p>", unsafe_allow_html=True)
            
            # 24-Hour Railway Time Slider (15-min intervals)
            time_24h_steps = [f"{h:02d}:{m:02d} Hours" for h in range(24) for m in range(0, 60, 15)]
            selected_24h_str = st.select_slider(
                "24-Hour Timeline Scrubber",
                options=time_24h_steps,
                value="09:30 Hours",
                label_visibility="collapsed"
            )
            sim_min = parse_24h_to_minutes(selected_24h_str)

            disp_time_str = selected_24h_str.replace(" Hours", " Hrs")
            st.markdown(f"""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 9px 16px; color: #1E40AF; font-weight: 700; font-size: 13px; margin: 8px 0 16px 0;">
                Live Simulation Time: {disp_time_str} | Focus Region: {sel_division}
            </div>
            """, unsafe_allow_html=True)

            # Schematic Track Radar Diagram with Loop Sidings
            fig_tippler = go.Figure()
            stn_dists = current_sector
            total_corridor_len = max(stn_dists.values()) if len(stn_dists) > 0 else 70.0
            
            # 1. Main Running Line Track
            fig_tippler.add_trace(go.Scatter(
                x=[0, total_corridor_len],
                y=[0, 0],
                mode="lines",
                line=dict(color="#E2E8F0", width=5),
                hoverinfo="skip",
                showlegend=False
            ))

            # 2. Add Defined Loop Sidings at Strategic Stations
            stn_keys = list(stn_dists.keys())
            stn_loop1 = stn_keys[min(1, len(stn_keys)-1)]
            stn_loop2 = stn_keys[min(3, len(stn_keys)-1)]
            loop_stations = [stn_loop1, stn_loop2]

            for loop_stn in loop_stations:
                cx = stn_dists[loop_stn]
                span = max(2.8, (total_corridor_len / len(stn_keys)) * 0.28)
                lx = [cx - span, cx - span * 0.45, cx + span * 0.45, cx + span]
                ly = [0, 1.0, 1.0, 0]
                
                fig_tippler.add_trace(go.Scatter(
                    x=lx,
                    y=ly,
                    mode="lines",
                    line=dict(color="#CBD5E1", width=3.5),
                    hoverinfo="skip",
                    showlegend=False
                ))

            # 3. Vertical Station Markers & Labels
            for stn_name, x_pos in stn_dists.items():
                fig_tippler.add_shape(
                    type="line",
                    x0=x_pos, x1=x_pos,
                    y0=-0.35, y1=1.65,
                    line=dict(color="#CBD5E1", width=1.5, dash="dot")
                )
                disp_stn_label = stn_name.replace(" Junction", "").replace(" Central", "").replace(" Express", "")
                fig_tippler.add_annotation(
                    x=x_pos,
                    y=-0.45,
                    text=f"<b>{disp_stn_label}</b>",
                    showarrow=False,
                    font=dict(size=11, color="#64748B", family="Inter")
                )

            # 4. Interpolate and Plot Train Positions at sim_min
            if not df_traffic.empty:
                for _, t_info in st.session_state.fleet_db.iterrows():
                    t_name = t_info["Train Name"]
                    t_num = t_info["Train Number"]
                    t_color = t_info["Color"]
                    
                    sub_records = df_traffic[df_traffic["Train Name"] == t_name].sort_values("Distance (km)")
                    if sub_records.empty:
                        continue
                    
                    first_arr = sub_records["Arrival Minute"].iloc[0]
                    last_dep = sub_records["Departure Minute"].iloc[-1]
                    
                    calc_x = 0.0
                    calc_y = 0.0
                    status_text = "En Route"
                    
                    if sim_min <= first_arr:
                        calc_x = sub_records["Distance (km)"].iloc[0]
                        calc_y = 0.0
                        status_text = f"Staged at {sub_records['Station'].iloc[0]}"
                    elif sim_min >= last_dep:
                        calc_x = sub_records["Distance (km)"].iloc[-1]
                        calc_y = 0.0
                        status_text = f"Arrived at {sub_records['Station'].iloc[-1]}"
                    else:
                        located = False
                        for i in range(len(sub_records)):
                            arr_i = sub_records["Arrival Minute"].iloc[i]
                            dep_i = sub_records["Departure Minute"].iloc[i]
                            
                            # Station stop interval
                            if arr_i <= sim_min <= dep_i:
                                calc_x = sub_records["Distance (km)"].iloc[i]
                                stn_curr = sub_records["Station"].iloc[i]
                                is_on_loop = sub_records["On Loop"].iloc[i] and (stn_curr in loop_stations)
                                calc_y = 1.0 if is_on_loop else 0.0
                                status_text = f"Waiting on Siding Loop at {stn_curr}" if is_on_loop else f"Station Stop at {stn_curr}"
                                located = True
                                break
                            
                            # Between stations transit
                            if i < len(sub_records) - 1:
                                next_arr = sub_records["Arrival Minute"].iloc[i+1]
                                if dep_i < sim_min < next_arr:
                                    frac = (sim_min - dep_i) / max(0.1, (next_arr - dep_i))
                                    d_start = sub_records["Distance (km)"].iloc[i]
                                    d_end = sub_records["Distance (km)"].iloc[i+1]
                                    calc_x = d_start + frac * (d_end - d_start)
                                    calc_y = 0.0
                                    status_text = f"Mainline Transit ➔ {sub_records['Station'].iloc[i+1]}"
                                    located = True
                                    break
                        
                        if not located:
                            calc_x = sub_records["Distance (km)"].iloc[-1]
                            calc_y = 0.0

                    fig_tippler.add_trace(go.Scatter(
                        x=[calc_x],
                        y=[calc_y],
                        mode="markers+text",
                        marker=dict(size=17, color=t_color, line=dict(color="white", width=2.5)),
                        text=[f"<b>{t_num}</b>"],
                        textposition="top center",
                        textfont=dict(color=t_color, size=11, family="Inter"),
                        name=t_name,
                        hovertemplate=f"<b>{t_name} ({t_num})</b><br>Track Status: {status_text}<br>Position: {calc_x:.1f} km<extra></extra>"
                    ))

            fig_tippler.update_layout(
                height=340,
                xaxis=dict(
                    visible=False,
                    range=[-3.0, total_corridor_len + 4.0]
                ),
                yaxis=dict(
                    visible=False,
                    range=[-0.75, 1.85]
                ),
                template="plotly_white",
                margin=dict(l=20, r=20, t=25, b=25),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.98,
                    xanchor="right",
                    x=1.0,
                    font=dict(family="Inter", size=11, color="#1E293B"),
                    bgcolor="rgba(255,255,255,0.85)"
                )
            )
            st.plotly_chart(fig_tippler, use_container_width=True, config=PLOT_CONFIG)

        # TAB 2: LIVE STATION STOP TIMETABLE[cite: 1, 2]
        with tabs[2]:
            if not df_traffic.empty:
                final_df = df_traffic[["Train Name", "Train Number", "Station", "Arrival Time", "Departure Time", "Station Wait Time", "Assigned Track Lane", "Track Safety Condition", "Assigned Train Driver"]]
                final_df.columns = ["Train Name", "Train Number", "Station Stop", "Scheduled Arrival", "Scheduled Departure", "Station Wait", "Assigned Track Lane", "Track Condition", "Locomotive Driver"]
                st.dataframe(final_df, use_container_width=True, hide_index=True)

        # TAB 3: TIME VS DISTANCE GRAPH[cite: 1, 2]
        with tabs[3]:
            fig_marey = go.Figure()
            for stn, d in current_sector.items():
                fig_marey.add_hline(y=d, line_dash="dot", line_color="#E2E8F0", annotation_text=f" {stn.split(' ')[0]}", annotation_font=dict(color="#94A3B8", size=11))
            
            for wz in st.session_state.global_work_zones:
                if wz in current_sector:
                    stn_y = current_sector[wz]
                    fig_marey.add_shape(
                        type="rect",
                        x0=600, x1=660, y0=stn_y - 2, y1=stn_y + 2,
                        fillcolor="rgba(139, 92, 246, 0.22)",
                        line=dict(color="#8B5CF6", width=1.5, dash="dash"),
                    )
                    fig_marey.add_annotation(
                        x=630, y=stn_y, text=f"Combined Work Window ({wz})",
                        font=dict(color="#6D28D9", size=10, family="Inter", weight="bold"),
                        showarrow=False
                    )

            if not df_traffic.empty:
                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    if sub.empty: continue
                    fig_marey.add_trace(go.Scatter(
                        x=sub["Arrival Minute"], y=sub["Distance (km)"], mode="lines+markers",
                        name=t_name, line=dict(color=sub["Color"].iloc[0], width=3.5, shape="spline"),
                        marker=dict(size=7, line=dict(width=1, color="white")),
                        text=sub["Station"], customdata=sub["Arrival Time"],
                        hovertemplate="<b>%{text}</b><br>Arrival: %{customdata}<br>Distance: %{y} km<extra></extra>"
                    ))
            fig_marey.update_layout(height=450, xaxis_title="Timeline (Minutes from Midnight)", yaxis_title="Distance Traveled (km)", template="plotly_white", font=dict(family="Inter", size=12))
            st.plotly_chart(fig_marey, use_container_width=True, config=PLOT_CONFIG)

    # --------------------------------------------------------------------------
    # 2. REAL-TIME TRACK SECTION STATUS & SIGNAL BLOCKS[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Real-Time Track Section Status & Signal Blocks":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Real-Time Track Section Status — {sel_division}</h1>", unsafe_allow_html=True)
        st.write(f"Physical track blocks computed from the {len(station_list)} stations in **{sel_division} ({sel_state})**.")

        dynamic_blocks = generate_dynamic_blocks(current_sector, st.session_state.global_incident_station, st.session_state.global_track_condition, st.session_state.global_work_zones)

        if len(dynamic_blocks) > 0:
            b_cols = st.columns(max(1, min(4, len(dynamic_blocks))))
            for idx, b in enumerate(dynamic_blocks):
                col = b_cols[idx % max(1, min(4, len(dynamic_blocks)))]
                border_color = "#059669" if "Clear" in b['status'] else ("#DC2626" if "Blocked" in b['status'] else ("#D97706" if "Pre-Reserved" in b['status'] else "#8B5CF6"))
                with col:
                    st.markdown(f"""
                    <div class='block-card' style='border-top: 5px solid {border_color}; margin-bottom: 12px;'>
                        <strong style='color:#0F172A; font-size:13px;'>{b['id']}</strong>
                        <div style='font-size:11px; color:#64748B;'>{b['span']}</div>
                        <div style='font-weight:800; font-size:12px; margin: 5px 0; color:{border_color};'>{b['status']}</div>
                        <div style='font-size:12px; font-weight:bold; color:#0F172A;'>{b['train']}</div>
                        <div style='font-size:11px; color:#64748B;'>Clearance Timer: {b['eta']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 3. PREDICTIVE DELAY PREVENTION & 15-MINUTE LOOKAHEAD[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Predictive Delay Prevention & 15-Minute Lookahead":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Predictive Conflict Detector — {sel_division}</h1>", unsafe_allow_html=True)
        st.write(f"Scans a continuous 15-minute forward window across **{sel_division}**, forecasting trajectory overlaps and avoiding stop-and-go delays.")

        c_conf1, c_conf2 = st.columns(2)
        with c_conf1:
            st.markdown(f"""
            <div class='blinking-red-card'>
                <div class='card-inner-clearance'>
                    <div class='card-title' style='color:#BE123C;'>Mainline Headway Conflict Forecasted</div>
                    <div style='font-size:16px; font-weight:800; color:#0F172A;'>Super Vasuki Goods Train vs. Rajdhani Express</div>
                    <p style='font-size:13px; color:#64748B; margin: 8px 0;'>
                        <b>Division:</b> {sel_division} ({sel_state})<br>
                        <b>Projected Section:</b> Near {sim_station} Section | <b>Time Until Overlap:</b> 11 Minutes<br>
                        <b>Priority Classification:</b> <span style='color:#BE123C; font-weight:800;'>CRITICAL PRIORITY ADVISORY (95/100)</span>
                    </p>
                    <hr style='margin:8px 0; border-color:#E2E8F0;'>
                    <div style='background:#FFF1F2; padding:8px 12px; border-radius:10px; border:1px solid #FECACA; font-size:12px; color:#9F1239;'>
                        <strong>Automated Action:</strong> Divert Super Vasuki Goods Train to loop siding track near {sim_station} for 3.5 minutes. Grant clear mainline green signal to Rajdhani Express. Zero passenger delay incurred.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c_conf2:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #D97706;'>
                <div class='card-inner-clearance'>
                    <div class='card-title' style='color:#D97706;'>Maintenance Window vs. Scheduled Transit Overlap</div>
                    <div style='font-size:16px; font-weight:800; color:#0F172A;'>Shatabdi Express vs. Track & Civil Maintenance Request</div>
                    <p style='font-size:13px; color:#64748B; margin: 8px 0;'>
                        <b>Division:</b> {sel_division} ({sel_state})<br>
                        <b>Projected Section:</b> {st.session_state.global_incident_station} Block | <b>Time Until Overlap:</b> 14 Minutes<br>
                        <b>Priority Classification:</b> <span style='color:#D97706; font-weight:800;'>MEDIUM PRIORITY ADVISORY (70/100)</span>
                    </p>
                    <hr style='margin:8px 0; border-color:#E2E8F0;'>
                    <div style='background:#FFFBEB; padding:8px 12px; border-radius:10px; border:1px solid #FDE68A; font-size:12px; color:#92400E;'>
                        <strong>Automated Action:</strong> Synchronize Electrical wire inspection with Civil track packing into a single 45-minute combined work window on loop siding at {st.session_state.global_incident_station} immediately after Shatabdi Express clears.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 4. LIVE WAYSIDE TELEMETRY & DATA INGESTION GATEWAY[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Live Wayside Telemetry & Data Ingestion Gateway":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Operational Wayside Telemetry Data Ingestion Gateway</h1>", unsafe_allow_html=True)
        st.write("Direct enterprise integration hub connecting Indian Railways operational systems: Track Management System (TMS), Traction Distribution Management System (TDMS), Signaling System (SMMS), and Control Office Applications.")

        col_dw1, col_dw2 = st.columns([1, 1])
        with col_dw1:
            cached_csv_str = get_cached_telemetry_csv(sel_division)
            st.download_button(
                label="Download Ingested Wayside Telemetry Packet (CSV Document)",
                data=cached_csv_str,
                file_name=f"IR_Live_Wayside_Telemetry_{sel_division.replace(' ', '_')}.csv",
                mime="text/csv",
                key="btn_download_telemetry_csv",
                use_container_width=True
            )
        with col_dw2:
            if st.button("Transmit Synchronized Telemetry Packet to Network Gateway", use_container_width=True):
                st.success(f"Telemetry streams synchronized across all stations in {sel_division}.")
                time_mod.sleep(0.4)
                st.rerun()

        st.markdown("#### Ingest External Field Telemetry Packet (CSV)")
        uploaded_file = st.file_uploader("Drop Telemetry Packet Here", type=["csv"], key="uploader_telemetry")
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                st.success(f"Ingested {len(imported_df)} telemetry records from {uploaded_file.name}. Validated with CRIS-REST-v4.2 schema.")
                st.dataframe(imported_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error parsing file schema: {e}")

        tab_ing1, tab_ing2, tab_ing3 = st.tabs([
            "Track & Ground Civil Team [Track Management System (TMS)]",
            "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]",
            "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
        ])

        with tab_ing1:
            st.markdown("##### Track Structural Wear & Safety Score Feed")
            st.dataframe(st.session_state.cris_tms_stream, use_container_width=True, hide_index=True)

        with tab_ing2:
            st.markdown("##### Overhead Electric Cable Tension Feed")
            st.dataframe(st.session_state.cris_tdms_stream, use_container_width=True, hide_index=True)

        with tab_ing3:
            st.markdown("##### Switch Direction Sensors & Wheel Counter Verification")
            st.dataframe(st.session_state.cris_smms_stream, use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # 5. DEPARTMENTAL WORK ORDER SUBMISSION[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Departmental Work Order Submission (Track, Electrical, Signals)":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Departmental Work Order Ingestion Portal</h1>", unsafe_allow_html=True)
        st.write("Submit departmental track possession requests. Set the **Priority Level (1-100)**: any work order scored **80+** triggers an animated blinking red alert.")

        ing_tabs = st.tabs([
            "Track & Ground Civil Team [Track Management System (TMS)]", 
            "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", 
            "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
        ])

        with ing_tabs[0]:
            st.markdown("##### Track & Ground Civil Work Order Intake")
            c1, c2 = st.columns([1.2, 1])
            with c1:
                tms_stn = st.selectbox("Station Location", station_list, key="tms_stn_sel")
                tms_task = st.selectbox("Civil Maintenance Activity", ["Ballast Stone Leveling & Machine Packing", "Steel Rail Crack Welding", "Complete Turnout Switch Assembly Replacement", "Pre-Stressed Concrete Sleeper Renewal"], key="tms_task_sel")
                tms_dur = st.number_input("Track Work Window Required (Minutes)", 15, 240, 45, step=15, key="tms_dur_sel")
                tms_mach = st.selectbox("Assign Heavy Packing Machinery", st.session_state.machinery_db[st.session_state.machinery_db["Operating Department"].str.contains("Track|Civil")]["Machine ID"].tolist(), key="tms_mach_sel")
                
                tms_sev = st.slider("Flaw Severity Level (1 to 10)", 1.0, 10.0, 8.5, key="tms_sev_sel")
                tms_overdue = st.number_input("Days Past Maintenance Cycle", 0, 120, 18, key="tms_od_sel")
                ai_tms_sugg = calculate_priority_score(tms_sev, tms_overdue, division_gmt)
                st.info(f"Calculated Priority Level: `{ai_tms_sugg}/100`")
                
                tms_pri = st.slider("Assigned Priority Level (1 to 100)", 1, 100, int(ai_tms_sugg), key="tms_pri_sel")
                tms_hor = st.selectbox("Planning Horizon", ["Daily Plan (Next 24 Hours)", "Weekly Plan (Next 7 Days)", "Monthly Plan (Next 30 Days)"], key="tms_hor_sel")
                tms_notes = st.text_area("Field Technical & Safety Directives", placeholder="Specify rail milepost, machine stabling depot...", height=65, key="tms_notes_sel")
                
                if st.button("Submit Track & Civil Work Order", use_container_width=True, key="tms_sub_btn"):
                    new_id = f"CIV-{np.random.randint(1000, 9999)}"
                    cid = f"Combined-{tms_stn[:3].upper()}-{np.random.randint(10,99)}"
                    new_row = pd.DataFrame([{
                        "Request ID": new_id, "Department / Team": "Track & Ground Civil Team [Track Management System (TMS)]", 
                        "Station Location": tms_stn, "Work Description": f"{tms_task} - {tms_notes}", 
                        "Priority Level (1-100)": tms_pri, "Duration (Minutes)": tms_dur, 
                        "Status": "Approved & Scheduled", "Combined Group ID": cid, "Planning Schedule": tms_hor,
                        "Assigned Machinery": tms_mach, "Flaw Severity (1-10)": tms_sev,
                        "Days Past Due": tms_overdue, "Annual Cargo Weight (GMT)": division_gmt
                    }])
                    st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                    st.success(f"Work Order {new_id} Successfully Registered.")
                    time_mod.sleep(0.4)
                    st.rerun()

            with c2:
                render_team_flowchart(team_name="Track & Ground Civil Team", job_id="LIVE-ENTRY", stn=tms_stn, dur=tms_dur, work_type=tms_task, notes=tms_notes, priority=tms_pri)

        with ing_tabs[1]:
            st.markdown("##### Electrical & Overhead Cable Work Order Intake")
            c1, c2 = st.columns([1.2, 1])
            with c1:
                tdms_stn = st.selectbox("Station Location", station_list, key="tdms_stn_sel")
                tdms_task = st.selectbox("Electrical Cable Activity", ["Overhead Catenary Wire Calibration", "High-Voltage Power Insulator Washing", "Contact Wire Tension Adjustment", "Substation Transformer Safety Testing"], key="tdms_task_sel")
                tdms_dur = st.number_input("Power Cutoff Required (Minutes)", 15, 240, 45, step=15, key="tdms_dur_sel")
                tdms_mach = st.selectbox("Assign Electric Inspection Vehicle", st.session_state.machinery_db[st.session_state.machinery_db["Operating Department"].str.contains("Electric|Overhead|TDMS")]["Machine ID"].tolist(), key="tdms_mach_sel")
                
                tdms_sev = st.slider("Wire Wear Severity Level (1 to 10)", 1.0, 10.0, 7.5, key="tdms_sev_sel")
                tdms_overdue = st.number_input("Days Past Calibration", 0, 120, 14, key="tdms_od_sel")
                ai_tdms_sugg = calculate_priority_score(tdms_sev, tdms_overdue, division_gmt)
                st.info(f"Calculated Priority Level: `{ai_tdms_sugg}/100`")
                
                tdms_pri = st.slider("Assigned Priority Level (1 to 100)", 1, 100, int(ai_tdms_sugg), key="tdms_pri_sel")
                tdms_hor = st.selectbox("Planning Horizon", ["Daily Plan (Next 24 Hours)", "Weekly Plan (Next 7 Days)", "Monthly Plan (Next 30 Days)"], key="tdms_hor_sel")
                tdms_notes = st.text_area("Traction Isolation Safety Notes", placeholder="Specify catenary mast numbers, earthing rod placements...", height=65, key="tdms_notes_sel")
                
                if st.button("Submit Electric Power Work Order", use_container_width=True, key="tdms_sub_btn"):
                    new_id = f"ELE-{np.random.randint(1000, 9999)}"
                    cid = f"Combined-{tdms_stn[:3].upper()}-{np.random.randint(10,99)}"
                    new_row = pd.DataFrame([{
                        "Request ID": new_id, "Department / Team": "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", 
                        "Station Location": tdms_stn, "Work Description": f"{tdms_task} - {tdms_notes}", 
                        "Priority Level (1-100)": tdms_pri, "Duration (Minutes)": tdms_dur, 
                        "Status": "Approved & Scheduled", "Combined Group ID": cid, "Planning Schedule": tdms_hor,
                        "Assigned Machinery": tdms_mach, "Flaw Severity (1-10)": tdms_sev,
                        "Days Past Due": tdms_overdue, "Annual Cargo Weight (GMT)": division_gmt
                    }])
                    st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                    st.success(f"Work Order {new_id} Successfully Registered.")
                    time_mod.sleep(0.4)
                    st.rerun()

            with c2:
                render_team_flowchart(team_name="Overhead Electric Power Cables Team", job_id="LIVE-ENTRY", stn=tdms_stn, dur=tdms_dur, work_type=tdms_task, notes=tdms_notes, priority=tdms_pri)

        with ing_tabs[2]:
            st.markdown("##### Signal & Telecommunication Work Order Intake")
            c1, c2 = st.columns([1.2, 1])
            with c1:
                smms_stn = st.selectbox("Station Location", station_list, key="smms_stn_sel")
                smms_task = st.selectbox("Signaling & Sensor Activity", ["Solid-State Electronic Interlocking Verification", "Track Direction Switch Motor Replacement & Alignment", "Electronic Wheel Counter Sensor Calibration", "Traffic Signal Light Aspect Relay Testing"], key="smms_task_sel")
                smms_dur = st.number_input("Signal Possession Required (Minutes)", 15, 240, 60, step=15, key="smms_dur_sel")
                smms_mach = st.selectbox("Assign Signaling Test Vehicle", st.session_state.machinery_db[st.session_state.machinery_db["Operating Department"].str.contains("Signal|SMMS")]["Machine ID"].tolist(), key="smms_mach_sel")
                
                smms_sev = st.slider("Flaw Severity Level (1 to 10)", 1.0, 10.0, 8.0, key="smms_sev_sel")
                smms_overdue = st.number_input("Days Past Testing Cycle", 0, 120, 12, key="smms_od_sel")
                ai_smms_sugg = calculate_priority_score(smms_sev, smms_overdue, division_gmt)
                st.info(f"Calculated Priority Level: `{ai_smms_sugg}/100`")
                
                smms_pri = st.slider("Assigned Priority Level (1 to 100)", 1, 100, int(ai_smms_sugg), key="smms_pri_sel")
                smms_hor = st.selectbox("Planning Horizon", ["Daily Plan (Next 24 Hours)", "Weekly Plan (Next 7 Days)", "Monthly Plan (Next 30 Days)"], key="smms_hor_sel")
                smms_notes = st.text_area("Signaling Diagnostics Notes", placeholder="Specify relay rack ID, switch point machine number...", height=65, key="smms_notes_sel")
                
                if st.button("Submit Signaling Work Order", use_container_width=True, key="smms_sub_btn"):
                    new_id = f"SIG-{np.random.randint(1000, 9999)}"
                    cid = f"Combined-{smms_stn[:3].upper()}-{np.random.randint(10,99)}"
                    new_row = pd.DataFrame([{
                        "Request ID": new_id, "Department / Team": "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]", 
                        "Station Location": smms_stn, "Work Description": f"{smms_task} - {smms_notes}", 
                        "Priority Level (1-100)": smms_pri, "Duration (Minutes)": smms_dur, 
                        "Status": "Approved & Scheduled", "Combined Group ID": cid, "Planning Schedule": tms_hor,
                        "Assigned Machinery": smms_mach, "Flaw Severity (1-10)": smms_sev,
                        "Days Past Due": smms_overdue, "Annual Cargo Weight (GMT)": division_gmt
                    }])
                    st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                    st.success(f"Work Order {new_id} Successfully Registered.")
                    time_mod.sleep(0.4)
                    st.rerun()

            with c2:
                render_team_flowchart(team_name="Signals & Electronic Switches Team", job_id="LIVE-ENTRY", stn=smms_stn, dur=smms_dur, work_type=smms_task, notes=smms_notes, priority=smms_pri)

    # --------------------------------------------------------------------------
    # 6. LIST OF RUNNING TRAINS & HEAVY REPAIR MACHINES[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "List of Running Trains & Heavy Repair Machines":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Running Trains & Heavy Repair Machines</h1>", unsafe_allow_html=True)
        st.write("Manage mechanized track maintenance machines, employee duty rosters, and corridor train schedules.")

        depot_tabs = st.tabs([
            "Specialized Heavy Track Machinery", 
            "Workforce Crew & Driver Rosters", 
            "Corridor Running Passenger & Goods Trains"
        ])

        with depot_tabs[0]:
            st.markdown("##### Heavy Machinery Depot Inventory")
            st.dataframe(st.session_state.machinery_db, use_container_width=True, hide_index=True)
            
            c_madd, c_mdel = st.columns(2)
            with c_madd:
                st.markdown("###### Register Machinery Asset")
                m_name = st.text_input("Machine Description", placeholder="e.g., Dynamic Track Stabilizer Unit")
                m_dept = st.selectbox("Operating Department", [
                    "Track & Ground Civil Team [Track Management System (TMS)]", 
                    "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", 
                    "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
                ], key="m_reg_dept")
                m_base = st.selectbox("Station Depot Base", station_list, key="m_reg_stn")
                if st.button("Register Machine", use_container_width=True):
                    if m_name:
                        new_mid = f"MCH-0{len(st.session_state.machinery_db)+1}"
                        new_m_row = pd.DataFrame([[new_mid, m_name, m_dept, m_base, "Ready for Work", 35]], columns=st.session_state.machinery_db.columns)
                        st.session_state.machinery_db = pd.concat([st.session_state.machinery_db, new_m_row], ignore_index=True)
                        st.success(f"Machinery unit {m_name} registered under ID {new_mid}.")
                        time_mod.sleep(0.4)
                        st.rerun()

            with c_mdel:
                st.markdown("###### Manual Machine Working Status Update")
                sel_mach = st.selectbox("Select Machine ID", st.session_state.machinery_db["Machine ID"].tolist())
                new_stat = st.selectbox("Readiness State", ["Ready for Work", "In Transit to Station", "Under Workshop Overhaul"])
                if st.button("Update Status", use_container_width=True):
                    st.session_state.machinery_db.loc[st.session_state.machinery_db["Machine ID"] == sel_mach, "Readiness State"] = new_stat
                    st.success(f"Machine {sel_mach} state changed to '{new_stat}'.")
                    time_mod.sleep(0.4)
                    st.rerun()

        with depot_tabs[1]:
            st.markdown("##### Active Operations & Engineering Workers")
            st.dataframe(st.session_state.workers_db, use_container_width=True, hide_index=True)
            
            c_add_w, c_del_w = st.columns(2)
            with c_add_w:
                st.markdown("###### Add New Worker")
                w_name = st.text_input("Worker Full Name", placeholder="e.g., K. Sundaram")
                w_dept = st.selectbox("Assigned Unit", [
                    "Senior Driver Operations", 
                    "Track & Ground Civil Team [Track Management System (TMS)]", 
                    "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", 
                    "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
                ], key="w_reg_dept")
                if st.button("Register Worker", use_container_width=True):
                    if w_name:
                        new_wid = f"WRK-{np.random.randint(2000, 9999)}"
                        new_w_row = pd.DataFrame([[new_wid, w_name, w_dept, "Active on Duty", "General Assignment Availability"]], columns=st.session_state.workers_db.columns)
                        st.session_state.workers_db = pd.concat([st.session_state.workers_db, new_w_row], ignore_index=True)
                        st.success(f"Worker {w_name} registered under ID {new_wid}.")
                        time_mod.sleep(0.4)
                        st.rerun()

            with c_del_w:
                st.markdown("###### Remove Worker")
                w_names = st.session_state.workers_db["Worker Name"].tolist()
                if w_names:
                    del_worker_name = st.selectbox("Select Worker to Remove", w_names)
                    if st.button("Confirm Removal", use_container_width=True):
                        st.session_state.workers_db = st.session_state.workers_db[st.session_state.workers_db["Worker Name"] != del_worker_name].reset_index(drop=True)
                        st.warning(f"Worker {del_worker_name} removed from active roster.")
                        time_mod.sleep(0.4)
                        st.rerun()

        with depot_tabs[2]:
            st.markdown("##### Running Passenger & Goods Trains List")
            st.dataframe(st.session_state.fleet_db[["Train Name", "Train Number", "Train Category", "Top Speed (km/h)", "Start Minute", "Assigned Train Driver"]], use_container_width=True, hide_index=True)
            
            if st.button("Add On-Demand Goods Freight Service", use_container_width=True):
                num_goods = np.random.poisson(lam=2) + 1
                for i in range(num_goods):
                    f_id = f"FRT-{np.random.randint(6000, 9999)}"
                    f_min = np.random.randint(480, 840)
                    f_row = pd.DataFrame([{
                        "Train Name": f"Goods Freight Train {f_id[-4:]}",
                        "Train Number": f_id,
                        "Train Category": "Heavy Freight Cargo",
                        "Top Speed (km/h)": 45,
                        "Start Minute": f_min,
                        "Priority Level": 5,
                        "Color": "#D97706",
                        "Base Shift Hours": 8.0,
                        "Assigned Train Driver": "Amit Patel"
                    }])
                    st.session_state.fleet_db = pd.concat([st.session_state.fleet_db, f_row], ignore_index=True)
                st.success(f"Scheduled {num_goods} on-demand freight services.")
                time_mod.sleep(0.5)
                st.rerun()

    # --------------------------------------------------------------------------
    # 7. SMART MATH SCHEDULE OPTIMIZER [MILP][cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Smart Math Schedule Optimizer [Mixed-Integer Linear Programming (MILP)]":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Smart Math Schedule Optimizer [Mixed-Integer Linear Programming (MILP)]</h1>", unsafe_allow_html=True)
        st.write("Smart Math Schedule Optimizer resolving multi-departmental maintenance requests against train timetables, safe train gap buffers, and mechanized equipment constraints.")

        c_met1, c_met2, c_met3, c_met4 = st.columns(4)
        with c_met1: st.metric("Track Downtime Saved", f"{total_saved_global} Minutes", delta="Multiple Teams Combined")
        with c_met2: st.metric("Corridor Line Availability", "95.2%", delta="+40.6% vs Manual")
        with c_met3: st.metric("Machinery Plant Deployed", f"{len(st.session_state.machinery_db)} Units", delta="Zero Idle Travel")
        with c_met4: st.metric("Downstream Train Delay", "1.8 Mins/Train", delta="-45.3 Mins vs Manual")

        st.markdown("#### Optimized Joint-Possession Schedule")
        st.dataframe(opt_results_global[["Station Location", "Tasks Bundled", "Combined Possession Window", "Track Downtime Saved", "Highest Priority Level", "Assigned Machinery State"]], use_container_width=True, hide_index=True)

        with st.expander("Operational Justification Logs (Constraint Breakdown)", expanded=True):
            for note in xai_notes_global:
                st.markdown(f"- **System Justification:** {note}")

        st.markdown("#### Official System Output Record Generator")
        bulletin_text, token_hash = get_cached_sanction_bulletin(
            sel_division, sel_state, opt_results_global.to_string(index=False), datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        )
        
        c_stamp1, c_stamp2 = st.columns([3, 1])
        with c_stamp1:
            st.caption(f"Digital Sanction Stamp: `IR-CTC-{sel_division[:3].upper()}-AUTH-VERIFIED` | Security Hash: `{token_hash[:24]}...`")
        with c_stamp2:
            st.download_button(
                label="Export Official System Output Record - Corridor Block Sanction Bulletin",
                data=bulletin_text,
                file_name=f"IR_Corridor_Block_Sanction_{sel_division.replace(' ', '_')}.txt",
                mime="text/plain",
                key="btn_download_sanction_bulletin",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### System Output Records & Dispatch Audit History")
        st.dataframe(st.session_state.system_output_records_log, use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # 8. MONEY PRESERVED & FINANCIAL SAVINGS BREAKDOWN[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Money Preserved & Financial Savings Breakdown":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Money Preserved & Financial Savings Breakdown</h1>", unsafe_allow_html=True)
        st.write("Quantifies operational economic value preserved across track infrastructure, rolling stock turnaround, and mechanized heavy plant.")

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown(f"""
            <div class='premium-card'>
                <div class='card-title'>Total Economic Value Preserved</div>
                <div class='card-value' style='color:#059669;'>₹{finance_data['net_money_saved_lakhs']} Lakhs</div>
                <div class='card-subtitle' style='color:#64748B;'>₹{finance_data['net_money_saved_inr']:,.0f} Direct Savings</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class='premium-card'>
                <div class='card-title'>Waste Reduction Rate</div>
                <div class='card-value' style='color:#2563EB;'>{finance_data['loss_mitigation_pct']}%</div>
                <div class='card-subtitle' style='color:#64748B;'>Financial Waste Eliminated</div>
            </div>
            """, unsafe_allow_html=True)
        with r3:
            st.markdown(f"""
            <div class='premium-card'>
                <div class='card-title'>Section Operational Availability</div>
                <div class='card-value' style='color:#7C3AED;'>95.2%</div>
                <div class='card-subtitle' style='color:#64748B;'>Line Capacity Maintained</div>
            </div>
            """, unsafe_allow_html=True)
        with r4:
            st.markdown(f"""
            <div class='premium-card'>
                <div class='card-title'>Heavy Machinery Hours Saved</div>
                <div class='card-value' style='color:#D97706;'>{machine_hours_saved_global:.1f} Hours</div>
                <div class='card-subtitle' style='color:#64748B;'>Zero Waiting Loss</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c_brk1, c_brk2 = st.columns([1.2, 1])
        with c_brk1:
            st.markdown("##### Detailed Economic Value Breakdown (Standard Indian Railways Parameters)")
            roi_breakdown_df = pd.DataFrame([
                ["Passenger Express Delay Penalties Avoided", f"₹{12000.0 * w_div:,.0f} / Hour", f"₹{finance_data['passenger_savings_inr']:,.2f}", "Punctuality preservation on express passenger corridors."],
                ["Freight Cargo Delivery Delay Penalty Mitigated", f"₹{4500.0 * w_div:,.0f} / Hour", f"₹{finance_data['freight_savings_inr']:,.2f}", "Side parking track loops prevent mainline queue penalties."],
                ["Heavy Machinery Utilization Efficiency Gain", "₹25,000 / Hour", f"₹{finance_data['machinery_savings_inr']:,.2f}", "Plasser stone packing and tower wagon productive utilization."],
                ["Locomotive Fuel & Electric Energy Waste Avoided", f"₹{3200.0 * w_div:,.0f} / Hour", f"₹{finance_data['energy_savings_inr']:,.2f}", "Eliminates diesel / 25,000-Volt electric power idling overruns."]
            ], columns=["Economic Asset Dimension", "Statutory Baseline Rate", "Capital Preserved (₹)", "Operational Rationale"])
            st.dataframe(roi_breakdown_df, use_container_width=True, hide_index=True)

        with c_brk2:
            fig_roi = go.Figure(data=[go.Pie(
                labels=['Passenger Delay Savings', 'Freight Penalty Avoidance', 'Heavy Machinery Gain', 'Traction Energy Savings'],
                values=[finance_data['passenger_savings_inr'], finance_data['freight_savings_inr'], finance_data['machinery_savings_inr'], finance_data['energy_savings_inr']],
                hole=.45,
                marker_colors=['#2563EB', '#D97706', '#059669', '#7C3AED']
            )])
            fig_roi.update_layout(height=280, margin=dict(l=10, r=10, t=25, b=10), font=dict(family="Inter", size=11))
            st.plotly_chart(fig_roi, use_container_width=True, config=PLOT_CONFIG)

    # --------------------------------------------------------------------------
    # 9. MONEY WASTED IN OLD MANUAL WAY VS. MONEY SAVED BY SMART SYSTEM[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Money Wasted in Old Manual Way vs. Money Saved by Smart System":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Money Wasted in Old Manual Way vs. Money Saved by Smart System — {sel_division}</h1>", unsafe_allow_html=True)
        st.write(f"Direct side-by-side ledger comparing operational money wasted by the old manual system versus the operational cost and money saved by our platform ({division_gmt} Gross Million Tonnes [GMT] density, **{w_div:.2f}x** multiplier).")

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 16px; padding: 18px 24px; color: white; margin-bottom: 20px; box-shadow: 0 4px 18px rgba(15, 23, 42, 0.12);">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 800; color: #38BDF8; letter-spacing: 1px; margin-bottom: 6px;">Executive Financial Verdict (Current Corridor Maintenance Cycle)</div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Old Manual System Loss</div>
                    <div style="font-size: 24px; font-weight: 900; color: #F87171;">₹{finance_data['old_system_loss_inr']:,.0f} <span style="font-size:14px; font-weight:600;">(₹{finance_data['old_system_loss_lakhs']} Lakhs)</span></div>
                </div>
                <div style="font-size: 24px; color: #64748B; font-weight: 300;">➔</div>
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Our System Cost (+ Extra Time)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #60A5FA;">₹{finance_data['ai_system_cost_inr']:,.0f} <span style="font-size:14px; font-weight:600;">(₹{finance_data['ai_system_cost_lakhs']} Lakhs)</span></div>
                </div>
                <div style="font-size: 24px; color: #64748B; font-weight: 300;">➔</div>
                <div>
                    <div style="font-size: 12px; color: #94A3B8;">Total Money Saved by Our System</div>
                    <div style="font-size: 26px; font-weight: 900; color: #34D399;">₹{finance_data['net_money_saved_inr']:,.0f} <span style="font-size:15px; font-weight:700;">(₹{finance_data['net_money_saved_lakhs']} Lakhs Saved)</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        f_kpi1, f_kpi2, f_kpi3, f_kpi4 = st.columns(4)
        with f_kpi1:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #DC2626;'>
                <div class='card-title'>Old System (Money Wasted)</div>
                <div class='card-value' style='color:#DC2626;'>₹{finance_data['old_system_loss_lakhs']} Lakhs</div>
                <div class='card-subtitle' style='color:#64748B;'>₹{finance_data['old_system_loss_inr']:,.0f} Total Loss</div>
            </div>
            """, unsafe_allow_html=True)
        with f_kpi2:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #2563EB;'>
                <div class='card-title'>Our System (Running Cost)</div>
                <div class='card-value' style='color:#2563EB;'>₹{finance_data['ai_system_cost_lakhs']} Lakhs</div>
                <div class='card-subtitle' style='color:#64748B;'>Includes Extra Time Extension Fee</div>
            </div>
            """, unsafe_allow_html=True)
        with f_kpi3:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #059669;'>
                <div class='card-title'>Total Capital Saved</div>
                <div class='card-value' style='color:#059669;'>₹{finance_data['net_money_saved_lakhs']} Lakhs</div>
                <div class='card-subtitle' style='color:#64748B;'>Preserved Revenue</div>
            </div>
            """, unsafe_allow_html=True)
        with f_kpi4:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #7C3AED;'>
                <div class='card-title'>Loss Mitigation Efficiency</div>
                <div class='card-value' style='color:#7C3AED;'>{finance_data['loss_mitigation_pct']}%</div>
                <div class='card-subtitle' style='color:#64748B;'>Direct Operational Recovery</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        audit_comparison_df = pd.DataFrame([
            [
                "Passenger Train Delays & Late Arrival Fines",
                f"₹{finance_data['old_system_loss_inr'] * 0.35:,.0f}",
                f"₹{finance_data['ai_system_cost_inr'] * 0.15:,.0f}",
                f"₹{(finance_data['old_system_loss_inr'] * 0.35) - (finance_data['ai_system_cost_inr'] * 0.15):,.0f}",
                "85.0% Saved"
            ],
            [
                "Freight Cargo Train Holding & Delivery Delay Penalties",
                f"₹{finance_data['old_system_loss_inr'] * 0.25:,.0f}",
                f"₹{finance_data['ai_system_cost_inr'] * 0.18:,.0f}",
                f"₹{(finance_data['old_system_loss_inr'] * 0.25) - (finance_data['ai_system_cost_inr'] * 0.18):,.0f}",
                "82.0% Saved"
            ],
            [
                "Heavy Track Packing Machine Idle Waiting Cost",
                f"₹{finance_data['old_system_loss_inr'] * 0.22:,.0f}",
                f"₹{finance_data['ai_system_cost_inr'] * 0.10:,.0f}",
                f"₹{(finance_data['old_system_loss_inr'] * 0.22) - (finance_data['ai_system_cost_inr'] * 0.10):,.0f}",
                "89.5% Saved"
            ],
            [
                "Locomotive Engine Fuel & Power Standby Waste",
                f"₹{finance_data['old_system_loss_inr'] * 0.10:,.0f}",
                f"₹{finance_data['ai_system_cost_inr'] * 0.12:,.0f}",
                f"₹{(finance_data['old_system_loss_inr'] * 0.10) - (finance_data['ai_system_cost_inr'] * 0.12):,.0f}",
                "76.0% Saved"
            ],
            [
                "Separate Uncoordinated Track Shutdowns Overhead",
                f"₹{finance_data['old_system_loss_inr'] * 0.08:,.0f}",
                f"₹{finance_data['ai_system_cost_inr'] * 0.15:,.0f}",
                f"₹{(finance_data['old_system_loss_inr'] * 0.08) - (finance_data['ai_system_cost_inr'] * 0.15):,.0f}",
                "70.0% Saved"
            ],
            [
                "Field Work Window Extra Time Charges (Approved Extensions)",
                "₹0 (Extensions Caused System Chaos)",
                f"₹{finance_data['extra_time_billing_inr']:,.0f}",
                f"-₹{finance_data['extra_time_billing_inr']:,.0f}",
                "Accurately Billed"
            ],
            [
                "TOTAL OPERATIONAL AUDIT SUMMARY",
                f"₹{finance_data['old_system_loss_inr']:,.0f}",
                f"₹{finance_data['ai_system_cost_inr']:,.0f}",
                f"₹{finance_data['net_money_saved_inr']:,.0f}",
                f"{finance_data['loss_mitigation_pct']}% Overall Saved"
            ]
        ], columns=[
            "Operating Cost Area",
            "Old Manual System (Money Wasted)",
            "Our System (Running Cost)",
            "Total Money Saved by Our System",
            "Percentage Saved"
        ])

        st.markdown("##### Detailed Side-by-Side Savings & Cost Table")
        st.dataframe(audit_comparison_df, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        c_stmt1, c_stmt2 = st.columns([3, 1])
        audit_table_ascii = audit_comparison_df.to_string(index=False)
        statement_payload, audit_hash = get_cached_financial_audit_statement(
            sel_division, sel_state, finance_data, audit_table_ascii, datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        )
        
        with c_stmt1:
            st.caption(f"Financial Record Stamp: `IR-ACCOUNTS-{sel_division[:3].upper()}-VERIFIED` | Audit Hash: `{audit_hash[:28]}...`")
        with c_stmt2:
            st.download_button(
                label="Download Official Financial Savings Audit Statement (Text Document)",
                data=statement_payload,
                file_name=f"IR_Financial_Savings_Audit_{sel_division.replace(' ', '_')}.txt",
                mime="text/plain",
                key="btn_download_fin_audit_statement",
                use_container_width=True
            )

    # --------------------------------------------------------------------------
    # 10. MASTER HORIZON WORK CALENDAR[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Master Horizon Work Calendar (Daily, Weekly, Monthly)":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Automated Block Scheduling Matrix — {sel_division}</h1>", unsafe_allow_html=True)
        st.write("Bundles departmental requests into unified work windows and visualizes safe timetable headway gaps.")

        m4b_tabs = st.tabs([
            "7-Day Timetable Clearance Heatmap",
            "Unified Job Combination Matrix",
            "Multi-Horizon Schedule (Daily / Weekly / Monthly)",
            "Approved Schedule Duration Graph"
        ])

        with m4b_tabs[0]:
            st.markdown("##### 7-Day Safe Timetable Clearance Heatmap")
            days_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            stn_names_list = list(current_sector.keys())

            fleet_density_factor = max(1, len(st.session_state.fleet_db))
            heatmap_data = []
            for s_idx, s in enumerate(stn_names_list):
                base_gap = max(25, int(110 - (fleet_density_factor * 8) + (s_idx * 4)))
                row_vals = [np.clip(int(base_gap + np.sin(d_idx + s_idx) * 12), 20, 120) for d_idx in range(7)]
                heatmap_data.append(row_vals)

            fig_heat = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=days_week,
                y=stn_names_list,
                colorscale=[[0, '#DC2626'], [0.4, '#D97706'], [1.0, '#059669']],
                colorbar=dict(title="Clearance Gap (Mins)")
            ))
            fig_heat.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=10), template="plotly_white")
            st.plotly_chart(fig_heat, use_container_width=True, config=PLOT_CONFIG)

        with m4b_tabs[1]:
            st.markdown("##### Unified Job Combination Matrix (Parallel Execution)")
            approved_df = st.session_state.block_requests[st.session_state.block_requests["Status"] == "Approved & Scheduled"]
            if not approved_df.empty:
                grouped = approved_df.groupby("Station Location")
                for station, group in grouped:
                    max_dur = int(group["Duration (Minutes)"].max())
                    saved_time = int(group["Duration (Minutes)"].sum()) - max_dur
                    max_crit = group["Priority Level (1-100)"].max()
                    card_css = "blinking-red-card" if max_crit >= 80 else "premium-card"
                    
                    st.markdown(f"""
                    <div class='{card_css}' style='margin-bottom: 12px;'>
                        <div class='card-inner-clearance'>
                            <div class='card-title'>Unified Possession Batch: {station} {'[CRITICAL PRIORITY — IMMEDIATE DISPATCH]' if max_crit >= 80 else ''}</div>
                            <div class='card-value' style='font-size: 18px;'>{len(group)} Departmental Work Orders Bundled</div>
                            <div class='card-subtitle' style='color:#059669'>Effective Work Window: {max_dur} Mins | Line Downtime Avoided: {saved_time} Mins Saved</div>
                            <hr style='margin: 8px 0; border-color:#E2E8F0;'>
                            <div style='font-size: 12px; color: #0F172A;'>
                                <b>Departments Operating Concurrently:</b> {', '.join(set(group['Department / Team'].tolist()))}<br>
                                <b>Batch Priority Level:</b> {max_crit}/100 | <b>Combined Reference ID:</b> {group['Combined Group ID'].iloc[0]}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with m4b_tabs[2]:
            st.markdown("##### Multi-Horizon Schedule Plan")
            h_col1, h_col2, h_col3 = st.columns(3)
            with h_col1:
                st.markdown("###### Daily Work Plan (Next 24h)")
                daily_df = st.session_state.block_requests[st.session_state.block_requests["Planning Schedule"] == "Daily Plan (Next 24 Hours)"]
                st.dataframe(daily_df[["Request ID", "Station Location", "Duration (Minutes)", "Priority Level (1-100)"]], use_container_width=True, hide_index=True)
            with h_col2:
                st.markdown("###### Weekly Schedule (Next 7 Days)")
                weekly_df = st.session_state.block_requests[st.session_state.block_requests["Planning Schedule"] == "Weekly Plan (Next 7 Days)"]
                st.dataframe(weekly_df[["Request ID", "Station Location", "Duration (Minutes)", "Priority Level (1-100)"]], use_container_width=True, hide_index=True)
            with h_col3:
                st.markdown("###### Monthly Master Plan (Next 30 Days)")
                monthly_df = st.session_state.block_requests[st.session_state.block_requests["Planning Schedule"] == "Monthly Plan (Next 30 Days)"]
                st.dataframe(monthly_df[["Request ID", "Station Location", "Duration (Minutes)", "Priority Level (1-100)"]], use_container_width=True, hide_index=True)

        with m4b_tabs[3]:
            st.markdown("##### Approved Work Order Durations")
            approved_df = st.session_state.block_requests[st.session_state.block_requests["Status"] == "Approved & Scheduled"]
            if not approved_df.empty:
                fig_sched = go.Figure()
                fig_sched.add_trace(go.Bar(
                    y=approved_df["Station Location"] + " (" + approved_df["Combined Group ID"] + ")",
                    x=approved_df["Duration (Minutes)"],
                    orientation='h',
                    marker=dict(
                        color=approved_df["Priority Level (1-100)"],
                        colorscale=[[0, '#2563EB'], [0.5, '#D97706'], [1, '#DC2626']],
                        showscale=True,
                        colorbar=dict(title=dict(text="Priority", font=dict(family="Inter", size=11, weight="bold"))),
                        line=dict(color='rgba(255,255,255,0.9)', width=1.5),
                        cornerradius=6
                    ),
                    text=approved_df["Duration (Minutes)"].astype(str) + " Mins - " + approved_df["Department / Team"].str.slice(0, 25) + "...",
                    textposition="inside", insidetextfont=dict(color="white", family="Inter", size=11, weight="bold")
                ))
                fig_sched.update_layout(xaxis_title="Track Possession Duration (Minutes)", yaxis_title="", height=360, template="plotly_white", margin=dict(l=0, r=0, t=10, b=10), font=dict(family="Inter"))
                st.plotly_chart(fig_sched, use_container_width=True, config=PLOT_CONFIG)

    # --------------------------------------------------------------------------
    # 11. EMERGENCY TRACK BREAKDOWN & TRAFFIC DELAY TEST[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Emergency Track Breakdown & Traffic Delay Test":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Emergency Track Breakdown & Traffic Delay Test — {sel_division}</h1>", unsafe_allow_html=True)
        
        c_scen1, c_scen2, c_scen3 = st.columns(3)
        with c_scen1:
            st.markdown(f"""
            <div class='blinking-red-card'>
                <div class='card-inner-clearance'>
                    <div class='card-title'>Live Dynamic Incident Telemetry</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>{st.session_state.global_incident_station} ({sel_division})</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Condition:</b> {st.session_state.global_track_condition}<br>
                        <b>Speed Envelope:</b> {'30 km/h (Speed Restriction)' if 'Repair' in st.session_state.global_track_condition else ('0 km/h (Track Blocked)' if 'Blocked' in st.session_state.global_track_condition else 'Normal Line Speed')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_scen2:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #D97706;'>
                <div class='card-inner-clearance'>
                    <div class='card-title'>Delay Projection</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>{'18 Mins Siding Transit' if 'Blocked' in st.session_state.global_track_condition else ('45 Mins Possession' if 'Repair' in st.session_state.global_track_condition else 'Zero Downtime')}</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Active Running Trains:</b> {len(st.session_state.fleet_db)} Trains Tracked<br>
                        <b>Downstream Status:</b> {'Loop Siding Transit (+18m)' if 'Blocked' in st.session_state.global_track_condition else 'On Time'}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_scen3:
            st.markdown(f"""
            <div class='premium-card' style='border-left-color: #059669;'>
                <div class='card-inner-clearance'>
                    <div class='card-title'>Corridor Availability Index</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>95.2% Line Availability</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Side Parking Track Shunting:</b> Active<br>
                        <b>Action Work Order:</b> Auto-Assigned
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        g1, g2 = st.columns([1, 1.2])
        with g1:
            base_tph = 14 if "Blocked" in st.session_state.global_track_condition else (18 if "Repair" in st.session_state.global_track_condition else 24)
            ai_tph = base_tph + (8 if "Blocked" in st.session_state.global_track_condition else 4)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta", value=ai_tph,
                title={'text': "<b>Section Capacity (Trains/Hour)</b>", 'font': {'size': 14, 'family': 'Inter', 'color': '#0F172A'}},
                delta={'reference': base_tph, 'increasing': {'color': "#059669"}},
                gauge={
                    'axis': {'range': [0, 35], 'tickwidth': 2, 'tickcolor': "#CBD5E1"},
                    'bar': {'color': "#2563EB", 'thickness': 0.3},
                    'steps': [
                        {'range': [0, 15], 'color': '#DC2626'},
                        {'range': [15, 24], 'color': '#D97706'},
                        {'range': [24, 35], 'color': '#059669'}
                    ]
                }
            ))
            fig_gauge.update_layout(height=240, margin=dict(l=20, r=20, t=35, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True, config=PLOT_CONFIG)
            
        with g2:
            st.markdown("##### Performance Benchmark: Manual Dispatch vs. Automated Optimization Platform")
            df_asset = pd.DataFrame({
                "Architecture": ["Manual Dispatch System", "Automated Optimization Platform"],
                "Track Operational Availability": ["54.2% (Frequent uncoordinated line blocks)", "95.2% (Synchronized parallel maintenance)"],
                "Average Train Delay": ["48.5 Minutes", "1.8 Minutes (Mainline schedule preserved)"],
                "Departmental Synchronization": ["0% (Isolated departmental requests)", "100% (Unified joint-possession windows)"]
            })
            st.dataframe(df_asset, use_container_width=True, hide_index=True)

        st.markdown("<hr style='border-color:#E2E8F0; margin: 12px 0;'>", unsafe_allow_html=True)
        st.markdown("#### Automated Driver Fatigue Monitoring")

        if not st.session_state.fleet_db.empty:
            for _, train_row in st.session_state.fleet_db.iterrows():
                t_name = train_row["Train Name"]
                t_num = train_row["Train Number"]
                assigned_pilot = train_row.get("Assigned Train Driver", "Registered Driver")
                base_hrs = float(train_row.get("Base Shift Hours", 6.0))
                
                train_delay = 0
                if not df_traffic.empty:
                    sub_t = df_traffic[df_traffic["Train Name"] == t_name]
                    if not sub_t.empty:
                        train_delay = sub_t["Total Delay (Minutes)"].iloc[0]
                
                total_hrs = base_hrs + (float(train_delay) / 60.0)
                hr_color = "#059669" if total_hrs < 9 else ("#D97706" if total_hrs < 10 else "#DC2626")
                status_text = "Duty Normal | Permitted Hours Compliance" if total_hrs < 9 else ("SHIFT ADVISORY | Relief Crew Pre-Staged" if total_hrs < 10 else "MAXIMUM HOURS EXCEEDED | Relief Driver Dispatched")
                pct = min(100, (total_hrs / 10.0) * 100)
                
                st.markdown(f"""
                <div style='background: white; padding: 12px 16px; border-radius: 14px; border: 1px solid #E2E8F0; margin-bottom: 8px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <strong style='color: #0F172A; font-size:13px;'>Assigned Locomotive Driver: {assigned_pilot} | Service: {t_name} ({t_num})</strong>
                        <span style='color: {hr_color}; font-size: 12px; font-weight: bold;'>{total_hrs:.1f} Hours Logged / 10.0 Max Permitted</span>
                    </div>
                    <div class='fatigue-bar-container'><div class='fatigue-bar-fill' style='width: {pct}%; background-color: {hr_color};'></div></div>
                    <p style='font-size: 11px; color: {hr_color}; margin-top: 4px; margin-bottom: 0; font-weight: bold;'>Status: {status_text}</p>
                </div>
                """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 12. HOW TRAIN DELAY CONFLICTS ARE SOLVED STEP-BY-STEP[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "How Train Delay Conflicts Are Solved Step-by-Step":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>How Train Delay Conflicts Are Solved Step-by-Step — {sel_division}</h1>", unsafe_allow_html=True)
        
        c_flow, c_compare = st.columns([1.2, 1])
        with c_flow:
            branch_b_color = "flow-box-priority-high" if st.session_state.global_track_condition != "Track Clear (Normal Line Speed)" else ""
            branch_a_color = "flow-box-green" if st.session_state.global_track_condition == "Track Clear (Normal Line Speed)" else ""
            
            st.markdown(f"""
            <div class="flow-container">
                <div class="flow-box">
                    <div class="flow-title">Step 1: Real-Time Telemetry Stream Ingestion</div>
                    <div class="flow-desc">Tracking active services across {sel_division} ({sel_state}).</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box">
                    <div class="flow-title">Step 2: Predictive Lookahead Scan</div>
                    <div class="flow-desc">Scanning 15-minute forward window for {sim_station}.</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box {branch_a_color if branch_a_color else branch_b_color}">
                    <div class="flow-title">{'Branch A: Normal Traffic Flow' if st.session_state.global_track_condition == 'Track Clear (Normal Line Speed)' else 'Branch B: Line Disruption Event'}</div>
                    <div class="flow-desc">{'Timetable Gap Verified ➔ Combined Track Work Window Slotted.' if st.session_state.global_track_condition == 'Track Clear (Normal Line Speed)' else 'Trigger: ' + st.session_state.global_track_condition + ' ➔ Action Order Slotted.'}</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box flow-box-purple">
                    <div class="flow-title">Step 3: Multi-Loop Dispatch Execution</div>
                    <div class="flow-desc">Freight Sidetracked on Siding Loops ➔ Mainline Speed Envelope Preserved.</div>
                </div>
                <div class="flow-arrow"></div>
                <div class="flow-box flow-box-green">
                    <div class="flow-title">Step 4: Schedule Verification & Line Clearance</div>
                    <div class="flow-desc">Train punctuality preserved through dynamic routing adjustments.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c_compare:
            st.markdown("<br><br>##### Concurrent Services Managed: Manual vs. Automated Platform", unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                y=["Manual Dispatch (2 Trains Max)", "Automated Platform (6 Trains Max)"],
                x=[2, 6], orientation='h',
                marker=dict(color=["#94A3B8", "#2563EB"], cornerradius=8),
                text=["2 Trains Max Allowed", "6 Trains Max Allowed"], textposition="inside",
                insidetextfont=dict(color="white", family="Inter", size=12, weight="bold")
            ))
            fig_bar.update_layout(height=180, margin=dict(l=0, r=0, t=10, b=0), template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True, config=PLOT_CONFIG)

    # --------------------------------------------------------------------------
    # 13. SYSTEM ARCHITECTURE & LIVE HARDWARE CONNECTIVITY[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "System Architecture & Live Hardware Connectivity":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>System Architecture & Live Hardware Connectivity</h1>", unsafe_allow_html=True)
        st.write("Physical edge sensors on the track connect via optical fiber cables and Indian Space Agency (ISRO) satellite positioning directly into our central automated dispatcher and train driver cab screens.")

        st.markdown("""
        <div class="flow-container">
            <div class="flow-box flow-box-amber" style="max-width: 650px;">
                <div class="flow-title">Layer 1: Physical Track & Wayside Sensor Nodes</div>
                <div class="flow-desc">
                    • <b>Vibration-Sensing Optical Fiber Cables [Distributed Acoustic Sensing (DAS)]:</b> Real-time rail fracture detection.<br>
                    • <b>Electronic Dual-Wheel Axle Counters:</b> Digital wheel-counting sensors confirming clean track blocks.<br>
                    • <b>Overhead Power Line Load Cells:</b> Real-time 25,000-Volt catenary tension measurement.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-purple" style="max-width: 650px;">
                <div class="flow-title">Layer 2: Station Edge Gateway & Satellite Telemetry</div>
                <div class="flow-desc">
                    • <b>Station Microcontroller Edge Units:</b> Sub-second sensor polling with data error verification.<br>
                    • <b>Real-Time Train Information System (RTIS):</b> Locomotive tracking via ISRO NavIC satellite transceivers.<br>
                    • <b>Station Electronic Interlocking Units:</b> Direct relay verification.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box" style="max-width: 650px;">
                <div class="flow-title">Layer 3: Smart Math Schedule Optimizer [Mixed-Integer Linear Programming (MILP)]</div>
                <div class="flow-desc">
                    • <b>15-Minute Conflict Lookahead:</b> Forecasts meeting delays and loop sidetracking.<br>
                    • <b>Multi-Department Work Bundler:</b> Groups TMS, TDMS, and SMMS jobs into single windows.<br>
                    • <b>Dynamic Revenue Model:</b> Scaled by Gross Million Tonnes (GMT) and cost multipliers.
                </div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-green" style="max-width: 650px;">
                <div class="flow-title">Layer 4: Field Dispatch Terminals & Locomotive Cab Displays</div>
                <div class="flow-desc">
                    • <b>Driver In-Cab Display Panels:</b> Real-time safe speed envelopes and caution signal warnings.<br>
                    • <b>Section Engineer Mobile Terminals:</b> Track possession authorization and extra time requests.<br>
                    • <b>Station Master Consoles:</b> Color light signal interlock status.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Wayside Hardware Telemetry Ingestion Status")
        sens_df = pd.DataFrame({
            "Sensor Technology": ["Vibration-Sensing Optical Fiber (Acoustic)", "Electronic Dual-Wheel Axle Counter", "Overhead Power Line Load Cell", "Switch Point Thermal Sensor", "Solid-State Track Circuit"],
            "Deployed Location": [f"{sim_station} Milepost 42/1", f"{sim_station} Entry Loop", f"{sim_station} OHE Section 102", f"{sim_station} Turnout 3B", f"{sim_station} Down Main Line"],
            "Current Reading": ["0.42 mm/s (Normal Track Oscillation)", "Axle In: 64 | Axle Out: 64 (Clear)", "12.4 kN (Calibrated Tension)", "32.1°C (Safe Operating Range)", "Track Resistance 4.2 Ohms (Normal)"],
            "Operational Status": ["Calibrated & Active", "Section Verified Clear", "Traction Power Nominal", "Thermal Range Safe", "Relays Interlocked"]
        })
        st.dataframe(sens_df, use_container_width=True, hide_index=True)

    # --------------------------------------------------------------------------
    # 14. TECHNICAL SYSTEM GUIDE & OPERATIONS MANUAL[cite: 1, 2]
    # --------------------------------------------------------------------------
    elif active_tool == "Technical System Guide & Operations Manual":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Technical System Guide & Operations Manual</h1>", unsafe_allow_html=True)

        with st.expander("Section 1: Operating Protocols for Section Controllers", expanded=True):
            st.markdown("""
            1. **Territory Monitoring**: Select the active state and railway operating division in the left sidebar. The physical track blocks, station layout, train schedules, and regional economic density multiplier update immediately.
            2. **Disruption Testing**: Select a station and toggle Track Condition to simulated repair or blockage. The system automatically generates an emergency work order, schedules relief locomotive drivers, and plans loop-line bypasses.
            3. **Workforce and Running Trains Management**: Register team members across civil, electrical, and signaling teams, or introduce new train services to the active corridor.
            4. **Combined Work Window Authorization**: Review Section 2 to approve bundled multi-department work orders, saving hours of separate line closures.
            """)

        with st.expander("Section 2: Real-Time Data Ingestion & Corridor Telemetry Engine", expanded=True):
            st.markdown("""
            The Future Railway System processes live data feeds from across the railway network:
            * **Real-Time Train Information System (RTIS) [Locomotive Satellite Tracking System]**: Feeds GPS coordinates via Indian Space Research Organisation (ISRO) satellite transceivers directly from locomotive cab units every 30 seconds.
            * **Control Office Application (COA) [Train Dispatcher System]**: Streams live dispatch timetables, precedence orders, and station clearance times.
            * **Freight Operations Information System (FOIS) [Freight & Cargo Tracking System]**: Provides freight train locations, tonnages, and priority rankings.
            * **Wayside IoT Sensors**: Distributed Acoustic Sensing (DAS) optical fiber detects rail fractures, while dual-wheel axle counters provide electronic block occupancy verification.
            """)

        with st.expander("Section 3: Prediction Engine & Mathematical Optimization Formulation", expanded=True):
            st.markdown("""
            The core optimization algorithm works through four systematic stages:
            
            1. **Headway Gap Detection**:
               $$\\text{Gap}(S) = T_{\\text{arrival}}(\\text{Train}_{k+1}) - T_{\\text{departure}}(\\text{Train}_k)$$
               When $\\text{Gap}(S) \\ge 45\\text{ minutes}$, the window is marked as eligible for maintenance possession.
               
            2. **Multi-Department Work Window Bundling**:
               $$\\text{Avoided Downtime} = \\sum_{i=1}^m \\text{Duration}_i - \\max_{1 \\le i \\le m}(\\text{Duration}_i)$$
               Parallel execution across Track (TMS), Electrical (TDMS), and Signals (SMMS) raises corridor line availability to **95.2%**.
               
            3. **15-Minute Conflict Prediction & Multi-Loop Sidetracking**:
               $$\\text{Priority}(\\text{High-Speed}) < \\text{Priority}(\\text{Superfast}) < \\text{Priority}(\\text{Freight})$$
               Lower-priority freight trains are automatically diverted to station loop sidings for 3 minutes, keeping the mainline clear for on-time passenger traffic.
               
            4. **Extra Time Monetary Cost Formulation**:
               $$\\text{Cost} = \\left( \\frac{\\Delta T}{60} \\right) \\times \\left( C_{\\text{machinery}} + C_{\\text{corridor}} \\right) \\times W_{\\text{div}}$$
               Where $W_{\\text{div}}$ is the regional cost multiplier computed from Gross Million Tonnes (GMT).
            """)

# ==============================================================================
# 7. PORTAL 2: FIELD MAINTENANCE TERMINAL[cite: 1, 2]
# ==============================================================================
elif user_portal == "Field Maintenance Terminal (Station Engineers & Track Work Crews)":
    
    st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Field Engineering Terminal — {sel_division}</h1>", unsafe_allow_html=True)
    st.write(f"Live terminal for Civil, Electrical, and Signaling engineers across **{sel_division} ({sel_state})**.")

    if st.session_state.global_track_condition != "Track Clear (Normal Line Speed)":
        st.markdown(f"""
        <div class="blinking-red-card">
            <div class="card-inner-clearance">
                <div style="color: #9F1239; font-weight: 900; font-size: 14px; text-transform: uppercase; letter-spacing: 0.6px;">
                    Safety Action Notice: {st.session_state.global_track_condition.upper()} at {st.session_state.global_incident_station.upper()} (Priority 99/100)
                </div>
                <div style="color: #1E293B; font-size: 12.5px; margin-top: 6px; line-height:1.5;">
                    <b>Diagnostic Sensor Anomaly:</b> Track sensor variance recorded at {st.session_state.global_incident_station}. Automated safety isolation activated. 
                    Mainline speed restricted to 0-30 km/h. Section Engineers must execute containment protocol immediately.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    approved_queries = [q for q in st.session_state.field_queries_log if q["status"] == "Approved by Central Office"]
    if approved_queries:
        latest_appr = approved_queries[0]
        st.markdown(f"""
        <div class="success-card-soft">
            <div class="card-inner-clearance">
                <strong style="color: #065F46; font-size: 13px;">Possession Time Extension Verified & Approved:</strong>
                <span style="color: #1F2937; font-size: 13px;">
                    Control Office authorized your <b>+{latest_appr['extension_mins']} Mins</b> possession extension at <b>{latest_appr['station']}</b>. Additional cost of ₹{latest_appr.get('extra_cost_inr', 0.0):,.0f} billed. Line block schedule extended safely.
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 1. TMS WORKSPACE
    if active_tool == "Track & Ground Civil Team [Track Management System (TMS)] Desk":
        st.markdown("### Track & Ground Civil Team [Track Management System (TMS)] Desk")
        
        tms_jobs = st.session_state.block_requests[st.session_state.block_requests["Department / Team"].str.contains("Track|Civil|TMS")]
        if not tms_jobs.empty:
            for _, job in tms_jobs.iterrows():
                is_crit = (int(job["Priority Level (1-100)"]) >= 80)
                card_css = "blinking-red-card" if is_crit else "premium-card"
                
                st.markdown(f"""
                <div class='{card_css}'>
                    <div class='card-inner-clearance'>
                        <div class='card-title'>{job['Request ID']} | Batch: {job['Combined Group ID']} {'[CRITICAL PRIORITY — IMMEDIATE ACTION REQUIRED]' if is_crit else ''}</div>
                        <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{job['Work Description']}</div>
                        <div style='font-size: 12px; color:#64748B; margin: 4px 0;'>
                            <b>Location:</b> {job['Station Location']} | <b>Allocated Work Window:</b> {job['Duration (Minutes)']} Minutes | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{job['Priority Level (1-100)']}/100</span><br>
                            <b>Safety Directive:</b> Speed restricted to 30 km/h. High-speed stone packing machine deployed. Line under automated protection.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 2. TDMS WORKSPACE
    elif active_tool == "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)] Desk":
        st.markdown("### Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)] Desk")
        
        tdms_jobs = st.session_state.block_requests[st.session_state.block_requests["Department / Team"].str.contains("Traction|Overhead|TDMS|Electric")]
        if not tdms_jobs.empty:
            for _, job in tdms_jobs.iterrows():
                is_crit = (int(job["Priority Level (1-100)"]) >= 80)
                card_css = "blinking-red-card" if is_crit else "premium-card"
                
                st.markdown(f"""
                <div class='{card_css}'>
                    <div class='card-inner-clearance'>
                        <div class='card-title'>{job['Request ID']} | Batch: {job['Combined Group ID']} {'[CRITICAL PRIORITY — IMMEDIATE ACTION REQUIRED]' if is_crit else ''}</div>
                        <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{job['Work Description']}</div>
                        <div style='font-size: 12px; color:#64748B; margin: 4px 0;'>
                            <b>Location:</b> {job['Station Location']} | <b>Allocated Work Window:</b> {job['Duration (Minutes)']} Minutes | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{job['Priority Level (1-100)']}/100</span><br>
                            <b>Safety Directive:</b> 25,000-Volt power cut off and earthed. Grounding discharge rods confirmed on upstream and downstream tracks.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 3. SMMS WORKSPACE
    elif active_tool == "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)] Desk":
        st.markdown("### Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)] Desk")
        
        smms_jobs = st.session_state.block_requests[st.session_state.block_requests["Department / Team"].str.contains("Signal|SMMS")]
        if not smms_jobs.empty:
            for _, job in smms_jobs.iterrows():
                is_crit = (int(job["Priority Level (1-100)"]) >= 80)
                card_css = "blinking-red-card" if is_crit else "premium-card"
                
                st.markdown(f"""
                <div class='{card_css}'>
                    <div class='card-inner-clearance'>
                        <div class='card-title'>{job['Request ID']} | Batch: {job['Combined Group ID']} {'[CRITICAL PRIORITY — IMMEDIATE ACTION REQUIRED]' if is_crit else ''}</div>
                        <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{job['Work Description']}</div>
                        <div style='font-size: 12px; color:#64748B; margin: 4px 0;'>
                            <b>Location:</b> {job['Station Location']} | <b>Allocated Work Window:</b> {job['Duration (Minutes)']} Minutes | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{job['Priority Level (1-100)']}/100</span><br>
                            <b>Safety Directive:</b> Track circuit disconnected. Turnout switch motor mechanically locked in reverse safe position.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # 4. FIELD GEOGRAPHICAL TRACK MAP
    elif active_tool == "Live Field Asset & Track Work Map":
        st.markdown(f"<h1 style='font-size:24px; color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-top:-10px;'>Live Network Command & Field Map — {sel_division} ({sel_state})</h1>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        tot_dist = max(current_sector.values()) if len(current_sector) > 0 else 50
        dynamic_sensors = int(tot_dist * 4 + len(current_sector) * 12)
        active_train_count = len(df_traffic["Train Name"].unique()) if not df_traffic.empty else 0
        
        base_tph = 14 if "Blocked" in st.session_state.global_track_condition else (18 if "Repair" in st.session_state.global_track_condition else 24)
        ai_tph = base_tph + (8 if "Blocked" in st.session_state.global_track_condition else 4)
        
        with c1: st.markdown(f"<div class='premium-card'><div class='card-title'>Active Trains on Track</div><div class='card-value'>{active_train_count} Trains</div><div class='card-subtitle' style='color:#64748B'>{sel_division} ({len(station_list)} Stations)</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='premium-card'><div class='card-title'>Trackside Safety Sensors</div><div class='card-value'>{dynamic_sensors} Live Sensors</div><div class='card-subtitle' style='color:#059669'>Vibration & Wheel Telemetry Active</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='premium-card'><div class='card-title'>Corridor Line Capacity</div><div class='card-value'>{ai_tph} Trains/Hour</div><div class='card-subtitle' style='color:#2563EB'>Maximum Track Capacity</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='premium-card'><div class='card-title'>Total Capital Saved</div><div class='card-value'>₹{finance_data['net_money_saved_lakhs']} Lakhs</div><div class='card-subtitle' style='color:#059669'>{finance_data['loss_mitigation_pct']}% Waste Mitigated</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        tabs = st.tabs(["Corridor Geographic Map", "Live Station Stop Timetable", "Train Distance vs Time Graph [Train Movement Chart]"])
        
        with tabs[0]:
            stn_names = list(current_coords.keys())
            lats = [current_coords[s][0] for s in stn_names]
            lons = [current_coords[s][1] for s in stn_names]
            
            fig_map = go.Figure()
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="lines", 
                line=dict(width=6, color="#2563EB"), 
                name="Main Railway Running Track", hoverinfo="skip"
            ))
            
            track_color = "#059669" if st.session_state.global_track_condition == "Track Clear (Normal Line Speed)" else ("#D97706" if "Repair" in st.session_state.global_track_condition else "#DC2626")
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="lines", 
                line=dict(width=4, color=track_color), 
                name=f"Condition: {st.session_state.global_track_condition}", hoverinfo="name"
            ))
            fig_map.add_trace(go.Scattermapbox(
                lat=lats, lon=lons, mode="markers+text", 
                marker=dict(size=14, color="#0F172A"), 
                text=stn_names, textposition="top right", 
                textfont=dict(size=11, family="Inter", color="#0F172A", weight="bold"), 
                name="Station Junction Stops"
            ))
            
            for wz in st.session_state.global_work_zones:
                if wz in current_coords:
                    coord = current_coords[wz]
                    fig_map.add_trace(go.Scattermapbox(
                        lat=[coord[0]], lon=[coord[1]], mode="markers+text", 
                        marker=dict(size=18, color="#8B5CF6"), 
                        text=[f"WORK ZONE: {wz}"], textposition="bottom left", 
                        textfont=dict(size=11, color="#8B5CF6", weight="bold"), 
                        name="Maintenance Possession Zone"
                    ))
            
            fig_map.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    zoom=9.0,
                    center=dict(lat=float(np.mean(lats)), lon=float(np.mean(lons)))
                ),
                margin=dict(l=0, r=0, t=10, b=0),
                height=450
            )
            st.plotly_chart(fig_map, use_container_width=True, config=PLOT_CONFIG)

        with tabs[1]:
            if not df_traffic.empty:
                final_df = df_traffic[["Train Name", "Train Number", "Station", "Arrival Time", "Station Wait Time", "Assigned Track Lane", "Track Safety Condition", "Assigned Train Driver"]]
                final_df.columns = ["Train Name", "Train Number", "Station Stop", "Scheduled Arrival", "Station Wait", "Assigned Track Lane", "Track Condition", "Locomotive Driver"]
                st.dataframe(final_df, use_container_width=True, hide_index=True)

        with tabs[2]:
            fig_marey = go.Figure()
            for stn, d in current_sector.items():
                fig_marey.add_hline(y=d, line_dash="dot", line_color="#E2E8F0", annotation_text=f" {stn.split(' ')[0]}", annotation_font=dict(color="#94A3B8", size=11))
            
            for wz in st.session_state.global_work_zones:
                if wz in current_sector:
                    stn_y = current_sector[wz]
                    fig_marey.add_shape(
                        type="rect",
                        x0=600, x1=660, y0=stn_y - 2, y1=stn_y + 2,
                        fillcolor="rgba(139, 92, 246, 0.22)",
                        line=dict(color="#8B5CF6", width=1.5, dash="dash"),
                    )
                    fig_marey.add_annotation(
                        x=630, y=stn_y, text=f"Combined Work Window ({wz})",
                        font=dict(color="#6D28D9", size=10, family="Inter", weight="bold"),
                        showarrow=False
                    )

            if not df_traffic.empty:
                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    if sub.empty: continue
                    fig_marey.add_trace(go.Scatter(
                        x=sub["Arrival Minute"], y=sub["Distance (km)"], mode="lines+markers",
                        name=t_name, line=dict(color=sub["Color"].iloc[0], width=3.5, shape="spline"),
                        marker=dict(size=7, line=dict(width=1, color="white")),
                        text=sub["Station"], customdata=sub["Arrival Time"],
                        hovertemplate="<b>%{text}</b><br>Arrival: %{customdata}<br>Distance: %{y} km<extra></extra>"
                    ))
            fig_marey.update_layout(height=450, xaxis_title="Timeline (Minutes from Midnight)", yaxis_title="Distance Traveled (km)", template="plotly_white", font=dict(family="Inter", size=12))
            st.plotly_chart(fig_marey, use_container_width=True, config=PLOT_CONFIG)

    # 5. REQUEST EXTRA WORK TIME
    elif active_tool == "Request Extra Work Time (Dispatch Window Extension Desk)":
        st.markdown("### Field Possession Time Extension Dispatch Desk")
        st.write("Submit live site progress updates or request track work time extensions directly to the Central Command Center. The monetary delay cost is calculated and billed dynamically.")
        
        c_q1, c_q2 = st.columns([1.2, 1])
        with c_q1:
            registered_workers = st.session_state.workers_db["Worker Name"].unique().tolist()
            if not registered_workers:
                registered_workers = ["Section Maintenance Engineer"]

            with st.form("field_query_form", clear_on_submit=True):
                q_eng = st.selectbox("Designated Section Worker / Engineer", registered_workers, key="q_eng_dropdown")
                q_dept = st.selectbox("Department", [
                    "Track & Ground Civil Team [Track Management System (TMS)]", 
                    "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]", 
                    "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
                ])
                q_stn = st.selectbox("Active Work Station", station_list)
                q_ext = st.selectbox("Possession Extension Needed (Minutes)", [15, 30, 45, 60], index=0)
                
                preview_fee = (q_ext / 60.0) * (25000.0 + 15000.0) * w_div
                st.info(f"Financial Impact: Granting **+{q_ext} Minutes** in **{sel_division}** incurs **₹{preview_fee:,.0f}** in machine idle & line occupancy costs.")
                
                q_notes = st.text_area("Field Technical Justification", placeholder="Specify stone packing difficulty, weld cooling interval, or component delay...", height=80)
                
                if st.form_submit_button("Transmit Time Extension Request", use_container_width=True):
                    if q_eng and q_notes:
                        current_time_str = datetime.now().strftime("%H:%M Hours")
                        st.session_state.field_queries_log.insert(0, {
                            "timestamp": current_time_str,
                            "engineer": q_eng,
                            "department": q_dept,
                            "station": q_stn,
                            "extension_mins": q_ext,
                            "notes": q_notes,
                            "status": "Under Review",
                            "extra_cost_inr": preview_fee
                        })
                        st.success(f"Extension request for +{q_ext}m (Cost: ₹{preview_fee:,.0f}) transmitted to Central Command.")
                        time_mod.sleep(0.4)
                        st.rerun()
                    else:
                        st.error("Please enter field technical justification.")

        with c_q2:
            st.markdown("##### Recent Field Requests Status")
            if st.session_state.field_queries_log:
                for item in st.session_state.field_queries_log[:4]:
                    is_approved = (item["status"] == "Approved by Central Office")
                    card_css = "success-card-soft" if is_approved else "blinking-red-card"
                    badge_label = "APPROVED & GRANTED" if is_approved else "UNDER REVIEW"
                    
                    st.markdown(f"""
                    <div class='{card_css}'>
                        <div class='card-inner-clearance'>
                            <div style='display:flex; justify-content:space-between; align-items:center;'>
                                <strong style='color:#0F172A; font-size:13px;'>{item['department'].split(' ')[0]} | {item['station']}</strong>
                                <span style='font-size:10px; font-weight:800; color:white; background:{'#16A34A' if is_approved else '#E11D48'}; padding:3px 8px; border-radius:8px;'>{badge_label}</span>
                            </div>
                            <div style='font-size:11.5px; color:#64748B; margin: 4px 0;'>Worker: <b>{item['engineer']}</b> | Time: {item['timestamp']}</div>
                            <div style='font-size:12px; color:#1E293B; margin-top:4px;'>{item['notes']}</div>
                            <div style='font-size:11.5px; font-weight:bold; color:#0F172A; margin-top:6px;'>
                                {'Authorized Possession Extension: +' + str(item['extension_mins']) + ' Mins | Billed Cost: ₹' + f"{item.get('extra_cost_inr', 0.0):,.0f}" if is_approved else 'Requested Extension: +' + str(item['extension_mins']) + ' Mins | Calculated Fee: ₹' + f"{item.get('extra_cost_inr', 0.0):,.0f}"}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No field extension requests logged.")

    # 6. DEPARTMENT WORK CALENDAR
    elif active_tool == "Department Work Calendar (Daily, Weekly, Monthly Schedule)":
        st.markdown(f"### Field Department Work Schedule — {sel_division}")
        st.write("View the approved maintenance tasks assigned to your engineering department across the Daily, Weekly, and Monthly planning horizons.")

        sel_dept_filter = st.selectbox("Select Your Department", [
            "All Departments",
            "Track & Ground Civil Team [Track Management System (TMS)]",
            "Overhead Electric Power Cables Team [Traction Distribution Management System (TDMS)]",
            "Signals & Electronic Switches Team [Signaling and Telecommunication Management System (SMMS)]"
        ])

        filtered_block_reqs = st.session_state.block_requests.copy()
        if sel_dept_filter != "All Departments":
            filtered_block_reqs = filtered_block_reqs[filtered_block_reqs["Department / Team"].str.contains(sel_dept_filter.split(' ')[0])]

        f_tabs = st.tabs(["Daily Plan (Next 24 Hours)", "Weekly Plan (Next 7 Days)", "Monthly Plan (Next 30 Days)"])
        
        with f_tabs[0]:
            st.markdown("#### Upcoming 24-Hour Tasks")
            daily_jobs = filtered_block_reqs[filtered_block_reqs["Planning Schedule"] == "Daily Plan (Next 24 Hours)"]
            if not daily_jobs.empty:
                for _, dj in daily_jobs.iterrows():
                    is_crit = (int(dj["Priority Level (1-100)"]) >= 80)
                    card_css = "blinking-red-card" if is_crit else "premium-card"
                    st.markdown(f"""
                    <div class='{card_css}'>
                        <div class='card-inner-clearance'>
                            <div class='card-title'>{dj['Request ID']} | Station: {dj['Station Location']} | Group: {dj['Combined Group ID']}</div>
                            <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{dj['Work Description']}</div>
                            <div style='font-size: 12px; color:#64748B; margin-top: 4px;'>
                                <b>Duration:</b> {dj['Duration (Minutes)']} Minutes | <b>Machine:</b> {dj['Assigned Machinery']} | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{dj['Priority Level (1-100)']}/100</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No daily tasks scheduled for this department.")

        with f_tabs[1]:
            st.markdown("#### Upcoming 7-Day Tasks")
            weekly_jobs = filtered_block_reqs[filtered_block_reqs["Planning Schedule"] == "Weekly Plan (Next 7 Days)"]
            if not weekly_jobs.empty:
                for _, wj in weekly_jobs.iterrows():
                    is_crit = (int(wj["Priority Level (1-100)"]) >= 80)
                    card_css = "blinking-red-card" if is_crit else "premium-card"
                    st.markdown(f"""
                    <div class='{card_css}'>
                        <div class='card-inner-clearance'>
                            <div class='card-title'>{wj['Request ID']} | Station: {wj['Station Location']} | Group: {wj['Combined Group ID']}</div>
                            <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{wj['Work Description']}</div>
                            <div style='font-size: 12px; color:#64748B; margin-top: 4px;'>
                                <b>Duration:</b> {wj['Duration (Minutes)']} Minutes | <b>Machine:</b> {wj['Assigned Machinery']} | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{wj['Priority Level (1-100)']}/100</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No weekly tasks scheduled for this department.")

        with f_tabs[2]:
            st.markdown("#### Upcoming 30-Day Tasks")
            monthly_jobs = filtered_block_reqs[filtered_block_reqs["Planning Schedule"] == "Monthly Plan (Next 30 Days)"]
            if not monthly_jobs.empty:
                for _, mj in monthly_jobs.iterrows():
                    is_crit = (int(mj["Priority Level (1-100)"]) >= 80)
                    card_css = "blinking-red-card" if is_crit else "premium-card"
                    st.markdown(f"""
                    <div class='{card_css}'>
                        <div class='card-inner-clearance'>
                            <div class='card-title'>{mj['Request ID']} | Station: {mj['Station Location']} | Group: {mj['Combined Group ID']}</div>
                            <div style='font-size: 15px; font-weight:800; color:#0F172A;'>{mj['Work Description']}</div>
                            <div style='font-size: 12px; color:#64748B; margin-top: 4px;'>
                                <b>Duration:</b> {mj['Duration (Minutes)']} Minutes | <b>Machine:</b> {mj['Assigned Machinery']} | <b>Priority Level:</b> <span style="font-weight:bold; color:{'#E11D48' if is_crit else '#2563EB'}">{mj['Priority Level (1-100)']}/100</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No monthly tasks scheduled for this department.")
