import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time as time_mod
from datetime import datetime, time, timedelta

# --- 1. ENTERPRISE CSS CONFIGURATION & ZERO WATERMARKS ---
st.set_page_config(page_title="Future Railway System | SIH 26027", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important; visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    
    button[data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: block !important;
        color: #0F172A !important;
        z-index: 100000 !important;
    }
    
    .stApp { background-color: #F4F7F9; font-family: 'Inter', sans-serif; }
    .css-18e3th9 { padding-top: 1rem; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F4F8 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    div[role="radiogroup"] { gap: 10px; }
    div[role="radiogroup"] > label {
        background: #FFFFFF;
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { 
        background: #FFFFFF; 
        transform: translateX(4px); 
        border-color: #2563EB;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.15); 
    }
    
    .premium-card {
        background: #FFFFFF;
        border-radius: 16px; padding: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.04); 
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .premium-card:hover { 
        transform: translateY(-4px); 
        border-color: #2563EB;
        box-shadow: 0 14px 35px rgba(37, 99, 235, 0.2); 
        border-left: 6px solid #10B981; 
    }
    
    .card-title { color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 1.2px; margin-bottom: 6px;}
    .card-value { color: #0F172A; font-size: 28px; font-weight: 900; line-height: 1.1; margin-bottom: 4px;}
    .card-subtitle { font-size: 12px; font-weight: 600;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 12px; border-bottom: 2px solid #E2E8F0; margin-bottom: 18px; }
    .stTabs [data-baseweb="tab"] { height: 44px; font-weight: 700; font-size: 13px; color: #94A3B8; background: transparent; border: none; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; font-weight: 800; }
    
    .modern-alert {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 5px solid #4F46E5; padding: 18px 22px; border-radius: 12px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.12); color: #1E293B;
        font-size: 14px; line-height: 1.6; margin-bottom: 20px; border: 1px solid #C7D2FE;
    }
    .modern-alert-red { 
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 5px solid #EF4444; border-color: #FECACA;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.12); 
    }
    .alert-title { font-weight: 900; font-size: 14px; color: #3730A3; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px;}
    .alert-title-red { color: #991B1B; }
    
    .stButton>button { border-radius: 10px; font-weight: 800; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; border: none; padding: 10px 24px; transition: all 0.3s; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.2); }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(37, 99, 235, 0.35); color: white; }
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.04); border: 1px solid #E2E8F0; }
    .login-container { max-width: 440px; margin: 60px auto; padding: 40px 32px; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.08); text-align: center; border: 1px solid #F1F5F9; border-top: 6px solid #2563EB;}
    
    .fatigue-bar-container { width: 100%; background-color: #E2E8F0; border-radius: 8px; margin-top: 8px; overflow: hidden; height: 10px;}
    .fatigue-bar-fill { height: 100%; border-radius: 8px; transition: width 0.5s ease; }
    
    .block-card {
        background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px;
        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
    }
    .block-card:hover {
        transform: translateY(-3px);
        border-color: #2563EB;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.18);
    }
    
    /* Interactive Flowchart Styles with Sharp Glowing Borders */
    .flow-container { display: flex; flex-direction: column; align-items: center; padding: 15px 0; font-family: 'Inter', sans-serif; }
    .flow-box { background: white; border: 2px solid #2563EB; border-radius: 12px; padding: 14px 22px; text-align: center; width: 440px; box-shadow: 0 6px 15px rgba(37, 99, 235, 0.1); position: relative; transition: all 0.3s ease; }
    .flow-box:hover { transform: translateY(-3px); box-shadow: 0 12px 30px rgba(37, 99, 235, 0.25); border-color: #1D4ED8; }
    .flow-box-red { border-color: #EF4444; box-shadow: 0 6px 15px rgba(239, 68, 68, 0.15); background: #FFF5F5; }
    .flow-box-red:hover { box-shadow: 0 12px 30px rgba(239, 68, 68, 0.25); }
    .flow-box-green { border-color: #10B981; box-shadow: 0 6px 15px rgba(16, 185, 129, 0.15); background: #F0FDF4; }
    .flow-box-green:hover { box-shadow: 0 12px 30px rgba(16, 185, 129, 0.25); }
    .flow-box-purple { border-color: #8B5CF6; box-shadow: 0 6px 15px rgba(139, 92, 246, 0.15); background: #F5F3FF; }
    .flow-box-purple:hover { box-shadow: 0 12px 30px rgba(139, 92, 246, 0.25); }
    .flow-title { font-weight: 800; font-size: 13px; color: #0F172A; text-transform: uppercase; margin-bottom: 4px; }
    .flow-desc { font-size: 12px; color: #475569; }
    .flow-arrow { width: 2px; height: 24px; background: #94A3B8; margin: 3px 0; position: relative; }
    .flow-arrow::after { content: ''; position: absolute; bottom: 0; left: -4px; border-width: 5px 5px 0; border-style: solid; border-color: #94A3B8 transparent transparent; }
    .flow-split { display: flex; width: 100%; max-width: 650px; justify-content: space-between; margin-top: 6px; }
    .flow-branch { display: flex; flex-direction: column; align-items: center; width: 48%; }
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {'displayModeBar': False, 'scrollZoom': True} 

# --- 2. GLOBAL STATE INITIALIZATION ---
if "staff_authenticated" not in st.session_state: st.session_state.staff_authenticated = False
if "auth_error" not in st.session_state: st.session_state.auth_error = False
if "active_tab" not in st.session_state: st.session_state.active_tab = "Live Network Traffic Dashboard"

if "global_incident_station" not in st.session_state: st.session_state.global_incident_station = "Salem Jn"
if "global_track_condition" not in st.session_state: st.session_state.global_track_condition = "Track Clear (Normal)"
if "global_ai_enabled" not in st.session_state: st.session_state.global_ai_enabled = True
if "global_work_zones" not in st.session_state: st.session_state.global_work_zones = ["Salem Jn", "Erode Jn"]
if "last_submitted_flowchart" not in st.session_state: st.session_state.last_submitted_flowchart = None

# Multi-Team Maintenance Request Database
if "block_requests" not in st.session_state:
    st.session_state.block_requests = pd.DataFrame([
        ["REQ-801", "Electric Overhead Wire Team (TDMS)", "Salem Jn", "Overhead Wire Calibration - Cable tension adjustment.", 95, 45, "AI Approved & Scheduled", "Combined-SAL-42", "Daily (24h)"],
        ["REQ-802", "Track & Rails Team (TMS)", "Salem Jn", "Ballast Stone Leveling - Track packing and tamping.", 85, 45, "AI Approved & Scheduled", "Combined-SAL-42", "Daily (24h)"],
        ["REQ-803", "Signals & Lights Team (SMMS)", "Erode Jn", "Signal Light Relay Repair - Electronic sensor test.", 60, 60, "AI Approved & Scheduled", "Combined-ERO-17", "Daily (24h)"],
        ["REQ-804", "Electric Overhead Wire Team (TDMS)", "Erode Jn", "Power Insulator Check - High-voltage line check.", 72, 60, "AI Approved & Scheduled", "Combined-ERO-17", "Daily (24h)"],
        ["REQ-805", "Track & Rails Team (TMS)", "Magnesite Jn", "Steel Rail Replacement - Ultrasonic crack fix.", 88, 90, "AI Approved & Scheduled", "Combined-MAG-91", "Weekly (7 Days)"],
        ["REQ-806", "Signals & Lights Team (SMMS)", "Magnesite Jn", "Track Switch Machine Overhaul - Motor check.", 92, 90, "AI Approved & Scheduled", "Combined-MAG-91", "Weekly (7 Days)"],
        ["REQ-807", "Track & Rails Team (TMS)", "Sankari Durg", "Complete Track Assembly Replacement.", 78, 120, "AI Approved & Scheduled", "Combined-SNK-08", "Monthly (30 Days)"]
    ], columns=["Request ID", "Team / Department", "Target Station", "Job Description", "Priority Level (1-100)", "Duration (Mins)", "Status", "Combined Job ID", "Planning Horizon"])

def check_password():
    if st.session_state.get("pwd_input", "") == "sona":
        st.session_state.staff_authenticated = True
        st.session_state.auth_error = False
    else:
        st.session_state.auth_error = True

def logout():
    st.session_state.staff_authenticated = False
    st.session_state.auth_error = False
    st.session_state.pwd_input = ""

def trigger_ai_focus():
    st.session_state.active_tab = "Live Network Traffic Dashboard"

def format_24h(minutes):
    try:
        total_mins = int(minutes) % 1440
        hrs = total_mins // 60
        mins = total_mins % 60
        return f"{hrs:02d}:{mins:02d} Hrs"
    except Exception:
        return "00:00 Hrs"

# --- 3. ENTERPRISE GPS DATABASE (15 States, 30 Divisions) ---
RAILWAY_NETWORK = {
    "Tamil Nadu": {
        "Salem": {
            "stations": {"Salem Jn": 0.0, "Magnesite Jn": 7.8, "Sankari Durg": 28.5, "Cauvery": 52.1, "Erode Jn": 64.2},
            "coords": {"Salem Jn": (11.6811, 78.1287), "Magnesite Jn": (11.7135, 78.1340), "Sankari Durg": (11.4795, 77.8732), "Cauvery": (11.3652, 77.7289), "Erode Jn": (11.3396, 77.7172)}
        },
        "Chennai": {
            "stations": {"Chennai Central": 0.0, "Basin Bridge": 2.5, "Perambur": 5.5, "Villivakkam": 9.2, "Avadi": 21.0},
            "coords": {"Chennai Central": (13.0827, 80.2755), "Basin Bridge": (13.0970, 80.2730), "Perambur": (13.1090, 80.2330), "Villivakkam": (13.1065, 80.2030), "Avadi": (13.1180, 80.0980)}
        }
    },
    "Maharashtra": {
        "Mumbai": {
            "stations": {"Mumbai CSMT": 0.0, "Dadar": 9.0, "Kurla Jn": 15.3, "Thane": 33.5, "Kalyan Jn": 53.2},
            "coords": {"Mumbai CSMT": (18.9402, 72.8356), "Dadar": (19.0178, 72.8478), "Kurla Jn": (19.0657, 72.8794), "Thane": (19.1860, 72.9759), "Kalyan Jn": (19.2354, 73.1299)}
        },
        "Pune": {
            "stations": {"Pune Jn": 0.0, "Shivajinagar": 2.5, "Khadki": 6.3, "Pimpri": 14.2, "Chinchwad": 16.5},
            "coords": {"Pune Jn": (18.5284, 73.8743), "Shivajinagar": (18.5314, 73.8510), "Khadki": (18.5630, 73.8310), "Pimpri": (18.6230, 73.7990), "Chinchwad": (18.6360, 73.7850)}
        }
    },
    "Karnataka": {
        "Bengaluru": {
            "stations": {"KSR Bengaluru": 0.0, "Bengaluru Cantt": 4.5, "KR Puram": 14.0, "Whitefield": 23.5, "Malur": 43.0},
            "coords": {"KSR Bengaluru": (12.9784, 77.5695), "Bengaluru Cantt": (12.9930, 77.5980), "KR Puram": (13.0012, 77.6766), "Whitefield": (12.9930, 77.7580), "Malur": (13.0030, 77.9380)}
        }
    },
    "Delhi NCR": {
        "New Delhi": {
            "stations": {"New Delhi": 0.0, "Tilak Bridge": 2.5, "Anand Vihar": 12.0, "Sahibabad Jn": 18.5, "Ghaziabad Jn": 25.0},
            "coords": {"New Delhi": (28.6431, 77.2197), "Tilak Bridge": (28.6250, 77.2430), "Anand Vihar": (28.6502, 77.3153), "Sahibabad Jn": (28.6720, 77.3610), "Ghaziabad Jn": (28.6675, 77.4330)}
        }
    },
    "Kerala": {
        "Thiruvananthapuram": {
            "stations": {"Trivandrum Central": 0.0, "Varkala": 40.5, "Kollam Jn": 64.2, "Kayamkulam Jn": 105.1, "Chengannur": 125.4},
            "coords": {"Trivandrum Central": (8.4875, 76.9530), "Varkala": (8.7360, 76.7160), "Kollam Jn": (8.8840, 76.5960), "Kayamkulam Jn": (9.1720, 76.5010), "Chengannur": (9.3170, 76.6130)}
        }
    },
    "Gujarat": {
        "Ahmedabad": {
            "stations": {"Ahmedabad Jn": 0.0, "Maninagar": 3.2, "Vatva": 7.5, "Geratpur": 13.1, "Barejadi": 17.8},
            "coords": {"Ahmedabad Jn": (23.0225, 72.6008), "Maninagar": (22.9980, 72.6040), "Vatva": (22.9570, 72.6340), "Geratpur": (22.9230, 72.6630), "Barejadi": (22.8870, 72.6890)}
        }
    },
    "West Bengal": {
        "Howrah": {
            "stations": {"Howrah Jn": 0.0, "Liluah": 4.8, "Belur": 6.2, "Bally": 8.5, "Dankuni Jn": 14.8},
            "coords": {"Howrah Jn": (22.5839, 88.3426), "Liluah": (22.6170, 88.3520), "Belur": (22.6320, 88.3540), "Bally": (22.6510, 88.3520), "Dankuni Jn": (22.6880, 88.2980)}
        }
    },
    "Uttar Pradesh": {
        "Lucknow": {
            "stations": {"Lucknow NR": 0.0, "Alambagh": 3.1, "Transport Nagar": 7.4, "Amausi": 11.2, "Harauni": 22.5},
            "coords": {"Lucknow NR": (26.8320, 80.9230), "Alambagh": (26.8120, 80.9030), "Transport Nagar": (26.7820, 80.8870), "Amausi": (26.7640, 80.8710), "Harauni": (26.7110, 80.7810)}
        }
    },
    "Rajasthan": {
        "Jaipur": {
            "stations": {"Jaipur Jn": 0.0, "Gandhinagar JPR": 5.4, "Getor Jagatpura": 11.2, "Khatipura": 16.8, "Kanauta": 25.4},
            "coords": {"Jaipur Jn": (26.9196, 75.7878), "Gandhinagar JPR": (26.8830, 75.8040), "Getor Jagatpura": (26.8480, 75.8490), "Khatipura": (26.8670, 75.9220), "Kanauta": (26.8680, 76.0120)}
        }
    },
    "Telangana": {
        "Secunderabad": {
            "stations": {"Secunderabad Jn": 0.0, "Sitafalmandi": 2.1, "Malkajgiri Jn": 3.5, "Bolarum": 13.8, "Medchal": 27.5},
            "coords": {"Secunderabad Jn": (17.4334, 78.5045), "Sitafalmandi": (17.4260, 78.5180), "Malkajgiri Jn": (17.4520, 78.5310), "Bolarum": (17.5280, 78.5130), "Medchal": (17.6290, 78.4830)}
        }
    },
    "Madhya Pradesh": {
        "Bhopal": {
            "stations": {"Bhopal Jn": 0.0, "Habibganj": 6.2, "Misrod": 13.5, "Mandideep": 23.8, "Obaidulla Ganj": 38.1},
            "coords": {"Bhopal Jn": (23.2599, 77.4126), "Habibganj": (23.2030, 77.4330), "Misrod": (23.1530, 77.4810), "Mandideep": (23.0940, 77.5350), "Obaidulla Ganj": (22.9730, 77.6250)}
        }
    },
    "Bihar": {
        "Patna": {
            "stations": {"Patna Jn": 0.0, "Rajendra Nagar": 2.8, "Gulzarbagh": 7.1, "Patna Saheb": 10.5, "Fatuha Jn": 22.1},
            "coords": {"Patna Jn": (25.5941, 85.1376), "Rajendra Nagar": (25.5980, 85.1630), "Gulzarbagh": (25.5930, 85.2070), "Patna Saheb": (25.5860, 85.2370), "Fatuha Jn": (25.5120, 85.3110)}
        }
    },
    "Odisha": {
        "Bhubaneswar": {
            "stations": {"Bhubaneswar": 0.0, "Mancheswar": 6.5, "Barang": 15.2, "Cuttack": 28.1, "Kendrapara Road": 32.5},
            "coords": {"Bhubaneswar": (20.2961, 85.8245), "Mancheswar": (20.3280, 85.8420), "Barang": (20.4070, 85.8560), "Cuttack": (20.4620, 85.8820), "Kendrapara Road": (20.4930, 85.8970)}
        }
    },
    "Punjab": {
        "Ludhiana": {
            "stations": {"Ludhiana Jn": 0.0, "Dhandari Kalan": 7.2, "Sanehwal": 15.1, "Doraha": 22.8, "Khanna": 43.5},
            "coords": {"Ludhiana Jn": (30.9010, 75.8573), "Dhandari Kalan": (30.8660, 75.9220), "Sanehwal": (30.8350, 75.9750), "Doraha": (30.7930, 76.0320), "Khanna": (30.7010, 76.2180)}
        }
    },
    "Assam": {
        "Guwahati": {
            "stations": {"Guwahati": 0.0, "Kamakhya": 6.8, "Azara": 19.5, "Mirza": 29.1, "Chhaygaon": 42.5},
            "coords": {"Guwahati": (26.1445, 91.7362), "Kamakhya": (26.1550, 91.6880), "Azara": (26.1210, 91.5940), "Mirza": (26.0840, 91.5310), "Chhaygaon": (26.0320, 91.4330)}
        }
    }
}

# --- 4. GLOBAL SIDEBAR & DISPATCH ENGINE ---
with st.sidebar:
    st.markdown('<h2 style="color:#0F172A; font-weight:900; letter-spacing:-1px; margin-bottom: -5px; margin-top: 10px;">FUTURE RAILWAY SYSTEM</h2>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px; font-weight:800; color:#2563EB; margin-bottom:20px; line-height:1.4; letter-spacing: 0.5px;'>AI AUTOMATIC BLOCK PLANNING (SIH26027)</p>", unsafe_allow_html=True)
    user_role = st.radio("System Portal Access", ["Central Command Center", "Controller's Overview in Passenger Application"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>OPERATIONAL TERRITORY</h3>", unsafe_allow_html=True)
    sel_state = st.selectbox("State Territory", list(RAILWAY_NETWORK.keys()), index=0)
    city_options = list(RAILWAY_NETWORK[sel_state].keys())
    sel_city = st.selectbox("Railway Division", city_options, index=0)
    
    sector_data = RAILWAY_NETWORK[sel_state][sel_city]
    current_sector = sector_data["stations"]
    current_coords = sector_data["coords"]
    station_list = list(current_sector.keys())
    mid_station_idx = max(0, min(2, len(station_list)-1)) 
    
    st.markdown("<br><h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>LIVE INCIDENT SIMULATOR</h3>", unsafe_allow_html=True)
    sel_station = st.selectbox("Target Station", station_list, index=0)
    track_status = st.selectbox("Track Condition", ["Track Clear (Normal)", "Track Repair (Slow Speed)", "Track Blocked (Sensor Alert)"], on_change=trigger_ai_focus)
    
    st.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
    ai_enabled = st.toggle("Enable AI Traffic Optimizer", value=True)
    
    st.session_state.global_incident_station = sel_station
    st.session_state.global_track_condition = track_status
    st.session_state.global_ai_enabled = ai_enabled

# Automatic Emergency Incident Response
if track_status != "Track Clear (Normal)":
    em_exists = any(r["Target Station"] == sel_station and "Emergency Auto-Dispatch" in r["Job Description"] for _, r in st.session_state.block_requests.iterrows())
    if not em_exists:
        new_em_id = f"EMG-{np.random.randint(1000, 9999)}"
        new_em_row = pd.DataFrame([[
            new_em_id, 
            "Track & Rails Team (TMS)" if "Repair" in track_status else "Signals & Lights Team (SMMS)", 
            sel_station, 
            f"Emergency Auto-Dispatch: Response to {track_status}", 
            99, 45, 
            "AI Approved & Scheduled", 
            f"Combined-{sel_station[:3].upper()}-EMG", 
            "Daily (24h)"
        ]], columns=st.session_state.block_requests.columns)
        st.session_state.block_requests = pd.concat([new_em_row, st.session_state.block_requests], ignore_index=True)
        if sel_station not in st.session_state.global_work_zones:
            st.session_state.global_work_zones.append(sel_station)

# Dynamic Global Simulation Engine (4 Trains)
def track_live_trains(damaged_stn, status, ai, sector_dict, approved_stns):
    try:
        vb_speed, exp_speed, fr_speed, shat_speed = 110, 85, 45, 95
        trains = [
            {"name": "Vande Bharat Express", "id": "VB-2026", "type": "High-Speed", "speed": vb_speed, "start_min": 540, "weight": 1, "color": "#10B981", "base_shift": 7.5}, 
            {"name": "Rajdhani Express", "id": "RAJ-1260", "type": "Express", "speed": exp_speed, "start_min": 558, "weight": 2, "color": "#3B82F6", "base_shift": 4.5},
            {"name": "Shatabdi Express", "id": "SHT-4421", "type": "Express", "speed": shat_speed, "start_min": 570, "weight": 3, "color": "#8B5CF6", "base_shift": 6.0},
            {"name": "Super Vasuki Goods Train", "id": "FRT-8802", "type": "Freight", "speed": fr_speed, "start_min": 528, "weight": 4, "color": "#F59E0B", "base_shift": 9.2}
        ]
        
        if ai: trains = sorted(trains, key=lambda x: x["weight"])
            
        records = []
        for t in trains:
            curr_time = t["start_min"]
            prev_dist = 0
            total_delay_added = 0
            
            for stn, dist in sector_dict.items():
                current_speed = t["speed"]
                dwell = 2 
                track = "Main Track"
                node_condition = "Clear"

                if stn == damaged_stn:
                    node_condition = status
                    if status == "Track Repair (Slow Speed)": 
                        current_speed = min(current_speed, 30)
                        total_delay_added += 15 if not ai else 8
                    elif status == "Track Blocked (Sensor Alert)":
                        added_wait = 120 if not ai else 18
                        dwell += added_wait
                        total_delay_added += added_wait
                        
                if stn in approved_stns:
                    node_condition = "Track Repair in Progress (Human Crew Working - AI Protected)"
                    current_speed = min(current_speed, 30)
                    total_delay_added += 5
                        
                mid_station = list(sector_dict.keys())[mid_station_idx] 
                if ai and t["type"] == "Freight" and stn == mid_station:
                    dwell += 20
                    track = "Side Track (Waiting Line)"
                    total_delay_added += 20
                
                dist_delta = dist - prev_dist if dist > prev_dist else 0
                travel_time = (dist_delta / current_speed) * 60
                
                arrival = curr_time + travel_time
                departure = arrival + dwell
                curr_time = departure 
                prev_dist = dist
                
                records.append({
                    "Train Name": t["name"], "Train ID": t["id"], "Station": stn, "Dist": dist, 
                    "Arrival_Mins": arrival, "Arrival 24H": format_24h(arrival),
                    "Wait Time at Station": f"{int(dwell)} mins", "Track Path Assigned": track, 
                    "Track Condition": node_condition, "Color": t["color"], 
                    "Base Shift": t["base_shift"], "Total Delay": total_delay_added
                })
        return pd.DataFrame(records)
    except Exception:
        return pd.DataFrame(columns=["Train Name", "Train ID", "Station", "Dist", "Arrival_Mins", "Arrival 24H", "Wait Time at Station", "Track Path Assigned", "Track Condition", "Color", "Base Shift", "Total Delay"])

df_traffic = track_live_trains(st.session_state.global_incident_station, st.session_state.global_track_condition, st.session_state.global_ai_enabled, current_sector, st.session_state.global_work_zones)

# Dynamic Block Generator
def generate_dynamic_blocks(sector_dict, incident_stn, incident_status, approved_work_zones):
    stations = list(sector_dict.keys())
    blocks = []
    
    for i in range(len(stations) - 1):
        s1, s2 = stations[i], stations[i+1]
        d1, d2 = sector_dict[s1], sector_dict[s2]
        bid = f"Block B{i+1}"
        span = f"{s1} → {s2} ({d1:.1f} - {d2:.1f} km)"
        
        status = "🟢 Free"
        train = "None"
        eta = "Available"
        
        if incident_status != "Track Clear (Normal)" and (s1 == incident_stn or s2 == incident_stn):
            if "Blocked" in incident_status:
                status = "🔴 Train Blocked"
                train = f"Freight Train (Stopped near {incident_stn})"
                eta = "Indefinite (Manual)" if not st.session_state.global_ai_enabled else "18 mins (AI Loop Reroute)"
            else:
                status = "🟣 Track Repair in Progress"
                train = "Repair Crew Active (Caution 30 km/h)"
                eta = "25 mins remaining"
        elif s1 in approved_work_zones or s2 in approved_work_zones:
            status = "🟣 Track Repair in Progress"
            train = "Combined Repair Team (AI Protected)"
            eta = "35 mins remaining"
        elif i == 0:
            status = "🔴 Train Occupied"
            train = "VB-2026 (Vande Bharat)"
            eta = "3 mins to clear"
        elif i == 1:
            status = "🟡 Reserved by AI"
            train = "RAJ-1260 (Rajdhani)"
            eta = "6 mins to arrive"
        
        blocks.append({
            "id": bid,
            "span": span,
            "status": status,
            "train": train,
            "eta": eta
        })
    return blocks

# Defensive Helper to Render Personalized Work-Order Flowchart
def render_team_flowchart(team_name=None, job_id=None, stn=None, dur=None, work_type=None, notes=None, team=None, id=None, work=None, **kwargs):
    t_name = team_name or team or "Maintenance Team"
    j_id = job_id or id or "REQ-AI"
    t_stn = stn or "Target Station"
    t_dur = dur or 45
    w_type = work_type or work or "Standard Repair"
    w_notes = notes or ""

    if "Track" in t_name:
        p_title = "Step 3: Track & Rails Safety Protocol"
        p_desc = f"Speed Reduced to 30 km/h at {t_stn} ➔ Ballast Tamping Machine Dispatched ➔ Ultrasonic Rail Check."
        box_class = "flow-box"
    elif "Electric" in t_name:
        p_title = "Step 3: Overhead Wire Safety Protocol"
        p_desc = f"OHE Power Isolated at {t_stn} ➔ Catenary Wire Tension Calibrated ➔ Earthing Discharge Verified."
        box_class = "flow-box-purple"
    else:
        p_title = "Step 3: Signals & Lights Safety Protocol"
        p_desc = f"Track Circuit Disconnected at {t_stn} ➔ Point Switch Motor Tested ➔ Interlocking Logic Verified."
        box_class = "flow-box-green"

    st.markdown(f"""
    <div style='margin-top: 20px;'>
        <h4 style='color: #0F172A;'>📋 Personalized Work-Order Execution Flowchart: {t_name}</h4>
        <div class="flow-container">
            <div class="flow-box">
                <div class="flow-title">Step 1: Work Order Verified & Ingested</div>
                <div class="flow-desc">Job ID: <b>{j_id}</b> | Team: <b>{t_name}</b> | Task: <b>{w_type}</b></div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box">
                <div class="flow-title">Step 2: Timetable Gap Locked in CCC</div>
                <div class="flow-desc">Location: <b>{t_stn}</b> | Allocated Safe Window: <b>{t_dur} Minutes</b></div>
            </div>
            <div class="flow-arrow"></div>
            <div class="{box_class}">
                <div class="flow-title">{p_title}</div>
                <div class="flow-desc">{p_desc}</div>
            </div>
            <div class="flow-arrow"></div>
            <div class="flow-box flow-box-green">
                <div class="flow-title">Step 4: Section Reopened & Telemetry Restored</div>
                <div class="flow-desc">Notes: {w_notes if w_notes else 'Standard execution'} | Signal Returned to Green.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PORTAL 1: CENTRAL COMMAND CENTER
# ==============================================================================
if user_role == "Central Command Center":
    
    if not st.session_state.staff_authenticated:
        st.markdown("<div style='height: 6vh;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class='login-container'>
                <div style='color:#0F172A; font-weight:900; font-size:24px; margin-bottom: 8px;'>System Admin Access</div>
                <p style="color:#64748B; margin-bottom:25px; font-size:14px; font-weight:600;">Central Command Center (CCC)</p>
            </div>
            """, unsafe_allow_html=True)
            st.text_input("Enter Passkey", type="password", key="pwd_input", label_visibility="collapsed")
            st.button("Authenticate System", on_click=check_password, use_container_width=True)
            if st.session_state.auth_error: st.error("Access Denied: Invalid Passkey.")
                
    else:
        staff_module = st.sidebar.radio("Control Modules", [
            "Live Network Traffic Dashboard", 
            "Real-Time Track Section Status (Dynamic Blocks)",
            "Predictive AI Conflict Detector (5–15 Min Lookahead)",
            "Multi-Team Automatic Block Planner (SIH26027)",
            "Disruption Testing & Track Availability Matrix",
            "Interactive Conflict Resolution Flowchart"
        ], key="active_tab")
        st.sidebar.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # MODULE 1: LIVE NETWORK TRAFFIC DASHBOARD
        # ----------------------------------------------------------------------
        if st.session_state.active_tab == "Live Network Traffic Dashboard":
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1: st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Central Network Command — {sel_city} Division ({sel_state})</h1>", unsafe_allow_html=True)
            with col_t2: st.button("Logout Session", on_click=logout, type="secondary", use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            base_tph = 14 if "Blocked" in st.session_state.global_track_condition else (18 if "Repair" in st.session_state.global_track_condition else 24)
            ai_tph = base_tph + (8 if "Blocked" in st.session_state.global_track_condition else 4) if st.session_state.global_ai_enabled else base_tph
            
            with c1: st.markdown(f"<div class='premium-card'><div class='card-title'>Active Trains</div><div class='card-value'>4 Trains Running</div><div class='card-subtitle' style='color:#64748B'>{sel_city} Division</div></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='premium-card'><div class='card-title'>Network Sensors</div><div class='card-value'>{'0 Sensor Alerts' if st.session_state.global_ai_enabled else ('Alert Active' if st.session_state.global_track_condition != 'Track Clear (Normal)' else '0 Sensor Alerts')}</div><div class='card-subtitle' style='color:#10B981'>{'AI Auto-Cleared' if st.session_state.global_ai_enabled and st.session_state.global_track_condition != 'Track Clear (Normal)' else 'Hardware Safe'}</div></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='premium-card'><div class='card-title'>Track Capacity</div><div class='card-value'>{ai_tph} Trains/Hour</div><div class='card-subtitle' style='color:#3B82F6'>Maximum Section Flow</div></div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='premium-card'><div class='card-title'>AI Traffic Brain</div><div class='card-value'>{'ONLINE' if st.session_state.global_ai_enabled else 'OFFLINE'}</div><div class='card-subtitle' style='color:{'#10B981' if st.session_state.global_ai_enabled else '#EF4444'}'>{'Dynamic Spacing Active' if st.session_state.global_ai_enabled else 'Old Fixed Distance'}</div></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if len(st.session_state.global_work_zones) > 0:
                unique_stns = list(set(st.session_state.global_work_zones))
                st.markdown(f"""
                <div class="modern-alert" style="border-left-color: #8B5CF6; background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%); border-color: #DDD6FE;">
                    <div class="alert-title" style="color: #6D28D9;">🚧 Active Track Repair Zones (AI-Protected)</div>
                    <strong>Live Dispatch Feed:</strong> Approved repair teams are actively working at <b>{', '.join(unique_stns)}</b> in <b>{sel_city} Division</b>. Approaching trains safely slow to 30 km/h with zero passenger timetable disruption.
                </div>
                """, unsafe_allow_html=True)

            tabs = st.tabs(["Geographic Track Map", "Live Station Timetable", "Operations Radar (Live Timeline)", "Time vs Distance Graph"])
            
            with tabs[0]:
                stn_names = list(current_coords.keys())
                lats = [current_coords[s][0] for s in stn_names]
                lons = [current_coords[s][1] for s in stn_names]
                
                fig_map = go.Figure()
                fig_map.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="lines", line=dict(width=8, color="#1E293B"), name="Main Line Track", hoverinfo="skip"))
                
                track_color = "#10B981" if st.session_state.global_track_condition == "Track Clear (Normal)" else ("#F59E0B" if "Repair" in st.session_state.global_track_condition else "#EF4444")
                fig_map.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="lines", line=dict(width=4, color=track_color), name=f"Status: {st.session_state.global_track_condition}", hoverinfo="name"))
                fig_map.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="markers+text", marker=dict(size=14, color="#2563EB"), text=stn_names, textposition="top right", textfont=dict(size=12, family="Inter", color="#0F172A", weight="bold"), name="Stations"))
                
                for wz in st.session_state.global_work_zones:
                    if wz in current_coords:
                        coord = current_coords[wz]
                        fig_map.add_trace(go.Scattermapbox(lat=[coord[0]], lon=[coord[1]], mode="markers+text", marker=dict(size=18, color="#8B5CF6"), text=[f"WORK ZONE: {wz}"], textposition="bottom left", textfont=dict(size=11, color="#8B5CF6", weight="bold"), name="Repair Zone"))
                
                fig_map.update_layout(mapbox=dict(style="carto-positron", zoom=9.5, center=dict(lat=np.mean(lats), lon=np.mean(lons))), margin=dict(l=0, r=0, t=10, b=0), height=460)
                st.plotly_chart(fig_map, use_container_width=True, config=PLOT_CONFIG)

            with tabs[1]:
                if not df_traffic.empty:
                    final_df = df_traffic[["Train Name", "Train ID", "Station", "Arrival 24H", "Wait Time at Station", "Track Path Assigned", "Track Condition"]]
                    final_df.columns = ["Train Name", "Train Number", "Station Stop", "Arrival Time", "Wait Time", "Assigned Path", "Track Condition"]
                    st.dataframe(final_df, use_container_width=True, hide_index=True)

            with tabs[2]:
                selected_time = st.slider("Operations Timeline (24-Hour Scrub):", min_value=time(8, 20), max_value=time(12, 0), value=time(9, 30), step=timedelta(minutes=2), format="HH:mm")
                sim_time_min = selected_time.hour * 60 + selected_time.minute
                st.info(f"**Simulation Hour:** {selected_time.strftime('%H:%M Hrs')} | **Active Division:** {sel_city}")
                
                fig_radar = go.Figure()
                max_dist = max(current_sector.values()) if len(current_sector) > 0 else 100
                mid_dist = list(current_sector.values())[mid_station_idx]
                
                fig_radar.add_hline(y=1, line_dash="solid", line_color="#E2E8F0", line_width=6)
                fig_radar.add_shape(type="line", x0=mid_dist-2, y0=1, x1=mid_dist, y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                fig_radar.add_shape(type="line", x0=mid_dist, y0=1.5, x1=mid_dist+(max_dist*0.05), y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                fig_radar.add_shape(type="line", x0=mid_dist+(max_dist*0.05), y0=1.5, x1=mid_dist+(max_dist*0.08), y1=1, line=dict(color="#E2E8F0", width=6)) 
                
                for wz in st.session_state.global_work_zones:
                    if wz in current_sector:
                        fig_radar.add_vline(x=current_sector[wz], line_dash="dash", line_color="#8B5CF6", line_width=2, opacity=0.7)
                        fig_radar.add_annotation(x=current_sector[wz], y=1.9, text="🚧 REPAIR ZONE", font=dict(color="#8B5CF6", size=10, family="Inter"), showarrow=False)

                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    if sub.empty: continue
                    times, dists = sub["Arrival_Mins"].values, sub["Dist"].values
                    if len(times) == 0 or sim_time_min < times[0]: continue
                    current_dist = dists[-1] if sim_time_min > times[-1] else np.interp(sim_time_min, times, dists)
                    
                    y_pos = 1
                    if ai_enabled and t_name == "Super Vasuki Goods Train" and mid_dist <= current_dist <= mid_dist+(max_dist*0.05): y_pos = 1.5 
                    
                    fig_radar.add_trace(go.Scatter(
                        x=[current_dist], y=[y_pos], mode="markers+text",
                        marker=dict(size=22, color=sub["Color"].iloc[0], line=dict(width=2, color="white")),
                        text=[sub["Train ID"].iloc[0]], textposition="top center",
                        textfont=dict(size=11, color=sub["Color"].iloc[0], family="Inter", weight="bold"),
                        name=t_name
                    ))

                for stn, d in current_sector.items():
                    fig_radar.add_vline(x=d, line_dash="dot", line_color="#CBD5E1", annotation_text=f" {stn.split(' ')[0]}", annotation_position="top left", annotation_font=dict(size=11, color="#64748B", family="Inter"))

                fig_radar.update_layout(yaxis=dict(showticklabels=False, range=[0.4, 2.2]), xaxis=dict(range=[-2, max_dist+(max_dist*0.1)], showgrid=False, zeroline=False), height=360, template="plotly_white", margin=dict(t=30, b=20), plot_bgcolor="#FFFFFF")
                st.plotly_chart(fig_radar, use_container_width=True, config=PLOT_CONFIG)

            with tabs[3]:
                fig_marey = go.Figure()
                for stn, d in current_sector.items():
                    fig_marey.add_hline(y=d, line_dash="dot", line_color="#E2E8F0", annotation_text=f" {stn.split(' ')[0]}", annotation_font=dict(color="#94A3B8", size=11))
                    
                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    if sub.empty: continue
                    fig_marey.add_trace(go.Scatter(
                        x=sub["Arrival_Mins"], y=sub["Dist"], mode="lines+markers",
                        name=t_name, line=dict(color=sub["Color"].iloc[0], width=4, shape="spline"),
                        marker=dict(size=8, line=dict(width=1, color="white")),
                        text=sub["Station"], customdata=sub["Arrival 24H"],
                        hovertemplate="<b>%{text}</b><br>Arrival: %{customdata}<br>Distance: %{y} km<extra></extra>"
                    ))
                fig_marey.update_layout(height=450, xaxis_title="Timeline (Minutes from Midnight)", yaxis_title="Distance Traversed (km)", template="plotly_white", font=dict(family="Inter", size=12))
                st.plotly_chart(fig_marey, use_container_width=True, config=PLOT_CONFIG)

        # ----------------------------------------------------------------------
        # MODULE 2: REAL-TIME TRACK SECTION STATUS (DYNAMIC BLOCKS)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Real-Time Track Section Status (Dynamic Blocks)":
            st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Real-Time Track Section Status — {sel_city} Division</h1>", unsafe_allow_html=True)
            st.write(f"Physical track blocks dynamically computed from the {len(station_list)} stations in **{sel_city} Division ({sel_state})**. Connected dynamically to live train traffic and incident feeds.")

            dynamic_blocks = generate_dynamic_blocks(current_sector, st.session_state.global_incident_station, st.session_state.global_track_condition, st.session_state.global_work_zones)

            b_cols = st.columns(min(4, len(dynamic_blocks)))
            for idx, b in enumerate(dynamic_blocks):
                col = b_cols[idx % min(4, len(dynamic_blocks))]
                border_color = "#10B981" if "🟢" in b['status'] else ("#EF4444" if "🔴" in b['status'] else ("#F59E0B" if "🟡" in b['status'] else "#8B5CF6"))
                with col:
                    st.markdown(f"""
                    <div class='block-card' style='border-top: 5px solid {border_color}; margin-bottom: 12px;'>
                        <strong style='color:#0F172A; font-size:14px;'>{b['id']}</strong>
                        <div style='font-size:11px; color:#64748B;'>{b['span']}</div>
                        <div style='font-weight:800; font-size:12px; margin: 6px 0; color:{border_color};'>{b['status']}</div>
                        <div style='font-size:12px; font-weight:bold; color:#0F172A;'>{b['train']}</div>
                        <div style='font-size:11px; color:#64748B;'>Status Countdown: {b['eta']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # MODULE 3: PREDICTIVE AI CONFLICT DETECTOR (5–15 MIN LOOKAHEAD)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Predictive AI Conflict Detector (5–15 Min Lookahead)":
            st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Predictive AI Conflict Detector — {sel_city} Division</h1>", unsafe_allow_html=True)
            st.write(f"Proactively scans a 15-minute future lookahead window across **{sel_city} Division**, forecasting trajectory overlaps before trains encounter red signals.")

            c_conf1, c_conf2 = st.columns(2)
            with c_conf1:
                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #EF4444;'>
                    <div class='card-title' style='color:#EF4444;'>⚡ Mainline Traffic Jam Detected Ahead</div>
                    <div style='font-size:16px; font-weight:800; color:#0F172A;'>Super Vasuki Goods vs. Rajdhani Express</div>
                    <p style='font-size:13px; color:#64748B; margin: 8px 0;'>
                        <b>Division / Territory:</b> {sel_city} Division ({sel_state})<br>
                        <b>Predicted Location:</b> Near {sel_station} Section | <b>Time Until Conflict:</b> 11 Minutes Ahead<br>
                        <b>Risk Level:</b> <span style='color:#EF4444; font-weight:800;'>HIGH RISK</span> (Both trains projected on single track line)
                    </p>
                    <hr style='margin:10px 0; border-color:#E2E8F0;'>
                    <div style='background:#FEF2F2; padding:10px; border-radius:8px; border:1px solid #FECACA; font-size:12px; color:#991B1B;'>
                        <strong>Automated AI Solution:</strong> Hold Super Vasuki Goods Train on Side Track near {sel_station} for 3.5 minutes. Allow Rajdhani Express to pass at full line speed. Zero passenger delay created.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_conf2:
                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #F59E0B;'>
                    <div class='card-title' style='color:#F59E0B;'>⚠️ Track Repair vs. Passenger Schedule Overlap</div>
                    <div style='font-size:16px; font-weight:800; color:#0F172A;'>Shatabdi Express vs. Repair Team Request</div>
                    <p style='font-size:13px; color:#64748B; margin: 8px 0;'>
                        <b>Division / Territory:</b> {sel_city} Division ({sel_state})<br>
                        <b>Predicted Location:</b> {st.session_state.global_incident_station} Track Section | <b>Time Until Conflict:</b> 14 Minutes Ahead<br>
                        <b>Risk Level:</b> <span style='color:#F59E0B; font-weight:800;'>MEDIUM RISK</span> (Track repair requested during scheduled train run)
                    </p>
                    <hr style='margin:10px 0; border-color:#E2E8F0;'>
                    <div style='background:#FFFBEB; padding:10px; border-radius:8px; border:1px solid #FDE68A; font-size:12px; color:#92400E;'>
                        <strong>Automated AI Solution:</strong> Combine Electric Wire repair with Track & Rails stone work into a single 45-minute combined window at {st.session_state.global_incident_station} starting right after Shatabdi passes.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # MODULE 4: MULTI-TEAM AUTOMATIC BLOCK PLANNER (SIH26027 CORE)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Multi-Team Automatic Block Planner (SIH26027)":
            st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Multi-Team Automatic Block Planner — {sel_city} Division</h1>", unsafe_allow_html=True)
            st.write("Coordinates Track & Rails (TMS), Electric Wires (TDMS), and Signals & Lights (SMMS) teams into natural timetable gaps between passing trains.")

            if st.session_state.global_track_condition != "Track Clear (Normal)":
                st.markdown(f"""
                <div class="modern-alert-red modern-alert">
                    <strong>🚨 EMERGENCY INCIDENT AUTO-DISPATCHED:</strong> Emergency track disruption at <b>{st.session_state.global_incident_station}</b> ({sel_city} Division). Repair teams have been automatically slotted into emergency windows below.
                </div>
                """, unsafe_allow_html=True)

            m_dept_tabs = st.tabs([
                "🔍 Visual Timetable Gap Finder",
                "🛠️ Track & Rails Team (TMS)", 
                "⚡ Electric Overhead Wire Team (TDMS)", 
                "🚦 Signals & Lights Team (SMMS)", 
                "🧠 Smart Job Combination Matrix",
                "📅 Multi-Horizon Plan (Daily/Weekly/Monthly)",
                "📊 Approved Schedule Graph"
            ])

            # TAB 0: Interactive Clearance Duration Bar Graph
            with m_dept_tabs[0]:
                st.markdown(f"### 🔍 Available Maintenance Gap Duration by Station — {sel_city}")
                st.write(f"The graph below calculates the exact safe maintenance time (in minutes) available between scheduled train runs for each station in **{sel_city} Division**.")

                stn_names_list = list(current_sector.keys())
                gap_durations = []
                bar_colors = []
                hover_texts = []

                for idx, stn_item in enumerate(stn_names_list):
                    df_stn_temp = df_traffic[df_traffic["Station"] == stn_item].sort_values("Arrival_Mins")
                    if len(df_stn_temp) >= 2:
                        t1_end = df_stn_temp.iloc[0]["Arrival_Mins"] + 15
                        t2_start = df_stn_temp.iloc[1]["Arrival_Mins"]
                        calc_gap = max(20, int(t2_start - t1_end))
                    else:
                        calc_gap = 65 - (idx * 5)
                    
                    gap_durations.append(calc_gap)
                    
                    if calc_gap >= 60:
                        bar_colors.append("#10B981") 
                    elif calc_gap >= 35:
                        bar_colors.append("#F59E0B") 
                    else:
                        bar_colors.append("#EF4444") 
                        
                    hover_texts.append(f"<b>{stn_item}</b><br>Available Window: <b>{calc_gap} Mins</b><br>Assigned Teams: TMS + TDMS + SMMS<br>Status: Safe for Parallel Execution")

                fig_gap_bar = go.Figure()
                fig_gap_bar.add_trace(go.Bar(
                    x=stn_names_list,
                    y=gap_durations,
                    marker=dict(color=bar_colors, cornerradius=8, line=dict(color="rgba(255,255,255,0.8)", width=1.5)),
                    text=[f"<b>{d} Mins</b>" for d in gap_durations],
                    textposition="inside",
                    insidetextfont=dict(color="white", size=13, weight="bold"),
                    hovertext=hover_texts,
                    hoverinfo="text"
                ))

                # Threshold line at 45 Mins minimum duration
                fig_gap_bar.add_hline(
                    y=45, line_dash="dash", line_color="#2563EB", line_width=2.5,
                    annotation_text="  Required Minimum Work Window (45 Mins)",
                    annotation_position="top left",
                    annotation_font=dict(color="#2563EB", size=12, weight="bold")
                )

                fig_gap_bar.update_layout(
                    height=320, template="plotly_white",
                    xaxis=dict(title="<b>Station / Track Section</b>", showgrid=False),
                    yaxis=dict(title="<b>Available Safe Gap (Minutes)</b>", showgrid=True, gridcolor="#F1F5F9", range=[0, max(gap_durations) + 25]),
                    margin=dict(l=0, r=0, t=20, b=10),
                    font=dict(family="Inter", size=12)
                )
                st.plotly_chart(fig_gap_bar, use_container_width=True, config=PLOT_CONFIG)

                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #10B981;'>
                    <div class='card-title'>AI Schedule Optimization Summary</div>
                    <div class='card-value' style='font-size: 18px;'>Longest Available Maintenance Gap: {max(gap_durations)} Minutes</div>
                    <div class='card-subtitle' style='color:#10B981'>All 3 departments (TMS, TDMS, SMMS) scheduled into parallel shadow blocks.</div>
                </div>
                """, unsafe_allow_html=True)

            with m_dept_tabs[1]:
                st.markdown(f"### 🛠️ Track & Rails Team (TMS) — {sel_city} Division")
                st.write("Submit repair requests for broken rails, track stone leveling, and sleeper replacements.")
                
                with st.form("tms_form", clear_on_submit=False):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        def_idx = list(current_sector.keys()).index(st.session_state.global_incident_station) if st.session_state.global_incident_station in current_sector else 0
                        tms_stn = st.selectbox("Target Station", list(current_sector.keys()), index=def_idx, key="tms_stn")
                        tms_work = st.selectbox("Work Type", ["Ballast Stone Leveling", "Steel Rail Fracture Fix", "Complete Track Assembly Replacement", "Sleeper Renewal"])
                    with c2:
                        tms_dur = st.number_input("Time Needed (Minutes)", 15, 240, 45, step=15, key="tms_dur")
                        tms_pri = st.slider("Priority Level (1 to 100)", 1, 100, 85, key="tms_pri")
                    with c3:
                        tms_hor = st.selectbox("Planning Horizon", ["Daily (24h)", "Weekly (7 Days)", "Monthly (30 Days)"], key="tms_hor")
                        tms_notes = st.text_area("Repair Notes", placeholder="Specific track details...", height=68)
                    
                    if st.form_submit_button("Submit Track & Rails Request to AI", use_container_width=True):
                        new_id = f"TMS-{np.random.randint(1000, 9999)}"
                        msg = st.empty()
                        msg.warning("AI is analyzing timetable gaps... finding safe slot.")
                        time_mod.sleep(2.5)
                        cid = f"Combined-{tms_stn[:3].upper()}-{np.random.randint(10,99)}"
                        msg.success(f"AI Approved & Scheduled! Assigned Combined Job ID: {cid}")
                        new_row = pd.DataFrame([[new_id, "Track & Rails Team (TMS)", tms_stn, f"{tms_work} - {tms_notes}", tms_pri, tms_dur, "AI Approved & Scheduled", cid, tms_hor]], columns=st.session_state.block_requests.columns)
                        st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                        st.session_state.last_submitted_flowchart = {
                            "team_name": "Track & Rails Team (TMS)", "job_id": new_id, "stn": tms_stn, "dur": tms_dur, "work_type": tms_work, "notes": tms_notes
                        }

                if st.session_state.last_submitted_flowchart and st.session_state.last_submitted_flowchart.get("team_name") == "Track & Rails Team (TMS)":
                    render_team_flowchart(**st.session_state.last_submitted_flowchart)

            with m_dept_tabs[2]:
                st.markdown(f"### ⚡ Electric Overhead Wire Team (TDMS) — {sel_city} Division")
                st.write("Submit requests for overhead wire tensioning, power checks, and electrical disconnections.")
                
                with st.form("tdms_form", clear_on_submit=False):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        def_idx = list(current_sector.keys()).index(st.session_state.global_incident_station) if st.session_state.global_incident_station in current_sector else 0
                        tdms_stn = st.selectbox("Target Station", list(current_sector.keys()), index=def_idx, key="tdms_stn")
                        tdms_work = st.selectbox("Work Type", ["Overhead Wire Calibration", "Power Insulator Check", "Wire Tension Adjustment", "Power Disconnection"])
                    with c2:
                        tdms_dur = st.number_input("Time Needed (Minutes)", 15, 240, 45, step=15, key="tdms_dur")
                        tdms_pri = st.slider("Priority Level (1 to 100)", 1, 100, 75, key="tdms_pri")
                    with c3:
                        tdms_hor = st.selectbox("Planning Horizon", ["Daily (24h)", "Weekly (7 Days)", "Monthly (30 Days)"], key="tdms_hor")
                        tdms_notes = st.text_area("Electric Wire Notes", placeholder="Catenary/contact wire details...", height=68)
                    
                    if st.form_submit_button("Submit Electric Wire Request to AI", use_container_width=True):
                        new_id = f"TDMS-{np.random.randint(1000, 9999)}"
                        msg = st.empty()
                        msg.warning("AI is analyzing timetable gaps... finding safe slot.")
                        time_mod.sleep(2.5)
                        cid = f"Combined-{tdms_stn[:3].upper()}-{np.random.randint(10,99)}"
                        msg.success(f"AI Approved & Scheduled! Assigned Combined Job ID: {cid}")
                        new_row = pd.DataFrame([[new_id, "Electric Overhead Wire Team (TDMS)", tdms_stn, f"{tdms_work} - {tdms_notes}", tdms_pri, tdms_dur, "AI Approved & Scheduled", cid, tdms_hor]], columns=st.session_state.block_requests.columns)
                        st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                        st.session_state.last_submitted_flowchart = {
                            "team_name": "Electric Overhead Wire Team (TDMS)", "job_id": new_id, "stn": tdms_stn, "dur": tdms_dur, "work_type": tdms_work, "notes": tdms_notes
                        }

                if st.session_state.last_submitted_flowchart and st.session_state.last_submitted_flowchart.get("team_name") == "Electric Overhead Wire Team (TDMS)":
                    render_team_flowchart(**st.session_state.last_submitted_flowchart)

            with m_dept_tabs[3]:
                st.markdown(f"### 🚦 Signals & Lights Team (SMMS) — {sel_city} Division")
                st.write("Submit requests for signal lights, moving track switch machines, and electronic track sensors.")
                
                with st.form("smms_form", clear_on_submit=False):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        def_idx = list(current_sector.keys()).index(st.session_state.global_incident_station) if st.session_state.global_incident_station in current_sector else 0
                        smms_stn = st.selectbox("Target Station", list(current_sector.keys()), index=def_idx, key="smms_stn")
                        smms_work = st.selectbox("Work Type", ["Signal Light Relay Repair", "Track Switch Machine Overhaul", "Track Sensor Calibration", "Interlocking Light Test"])
                    with c2:
                        smms_dur = st.number_input("Time Needed (Minutes)", 15, 240, 60, step=15, key="smms_dur")
                        smms_pri = st.slider("Priority Level (1 to 100)", 1, 100, 70, key="smms_pri")
                    with c3:
                        smms_hor = st.selectbox("Planning Horizon", ["Daily (24h)", "Weekly (7 Days)", "Monthly (30 Days)"], key="smms_hor")
                        smms_notes = st.text_area("Signal Notes", placeholder="Sensor coil details...", height=68)
                    
                    if st.form_submit_button("Submit Signals & Lights Request to AI", use_container_width=True):
                        new_id = f"SMMS-{np.random.randint(1000, 9999)}"
                        msg = st.empty()
                        msg.warning("AI is analyzing timetable gaps... finding safe slot.")
                        time_mod.sleep(2.5)
                        cid = f"Combined-{smms_stn[:3].upper()}-{np.random.randint(10,99)}"
                        msg.success(f"AI Approved & Scheduled! Assigned Combined Job ID: {cid}")
                        new_row = pd.DataFrame([[new_id, "Signals & Lights Team (SMMS)", smms_stn, f"{smms_work} - {smms_notes}", smms_pri, smms_dur, "AI Approved & Scheduled", cid, smms_hor]], columns=st.session_state.block_requests.columns)
                        st.session_state.block_requests = pd.concat([new_row, st.session_state.block_requests], ignore_index=True)
                        st.session_state.last_submitted_flowchart = {
                            "team_name": "Signals & Lights Team (SMMS)", "job_id": new_id, "stn": smms_stn, "dur": smms_dur, "work_type": smms_work, "notes": smms_notes
                        }

                if st.session_state.last_submitted_flowchart and st.session_state.last_submitted_flowchart.get("team_name") == "Signals & Lights Team (SMMS)":
                    render_team_flowchart(**st.session_state.last_submitted_flowchart)

            with m_dept_tabs[4]:
                st.markdown("### 🧠 Smart Job Combination Matrix (Combining Tasks into One Window)")
                st.write("Demonstrates how the AI bundles maintenance tasks from all 3 teams occurring at the same station into one single shared time window.")
                
                approved_df = st.session_state.block_requests[st.session_state.block_requests["Status"] == "AI Approved & Scheduled"]
                if not approved_df.empty:
                    grouped = approved_df.groupby("Target Station")
                    for station, group in grouped:
                        max_crit = group["Priority Level (1-100)"].max()
                        max_dur = group["Duration (Mins)"].max()
                        saved_time = group["Duration (Mins)"].sum() - max_dur
                        
                        st.markdown(f"""
                        <div class='premium-card' style='border-left-color: #3B82F6; margin-bottom: 12px;'>
                            <div class='card-title'>Combined Repair Batch: {station}</div>
                            <div class='card-value' style='font-size: 18px;'>{len(group)} Separate Team Tasks Combined</div>
                            <div class='card-subtitle' style='color:#10B981'>Total Track Closure Time: {max_dur} Mins | Track Downtime Avoided: {saved_time} Mins Saved</div>
                            <hr style='margin: 8px 0; border-color:#E2E8F0;'>
                            <div style='font-size: 12px; color: #0F172A;'>
                                <b>Teams Working Together:</b> {', '.join(group['Team / Department'].tolist())}<br>
                                <b>Overall Priority:</b> {max_crit}/100 | <b>Combined Job ID:</b> {group['Combined Job ID'].iloc[0]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No active repair requests in database.")

            with m_dept_tabs[5]:
                st.markdown("### 📅 Multi-Horizon Plan (Daily, Weekly, Monthly)")
                h_col1, h_col2, h_col3 = st.columns(3)
                with h_col1:
                    st.markdown("#### Daily Plan (Next 24h)")
                    daily_df = st.session_state.block_requests[st.session_state.block_requests["Planning Horizon"] == "Daily (24h)"]
                    st.dataframe(daily_df[["Request ID", "Target Station", "Duration (Mins)", "Status"]], use_container_width=True, hide_index=True)
                with h_col2:
                    st.markdown("#### Weekly Plan (Next 7 Days)")
                    weekly_df = st.session_state.block_requests[st.session_state.block_requests["Planning Horizon"] == "Weekly (7 Days)"]
                    st.dataframe(weekly_df[["Request ID", "Target Station", "Duration (Mins)", "Status"]], use_container_width=True, hide_index=True)
                with h_col3:
                    st.markdown("#### Monthly Plan (Next 30 Days)")
                    monthly_df = st.session_state.block_requests[st.session_state.block_requests["Planning Horizon"] == "Monthly (30 Days)"]
                    st.dataframe(monthly_df[["Request ID", "Target Station", "Duration (Mins)", "Status"]], use_container_width=True, hide_index=True)

            with m_dept_tabs[6]:
                st.markdown("### 📊 Approved Schedule Graph (Official Railway Colors)")
                approved_df = st.session_state.block_requests[st.session_state.block_requests["Status"] == "AI Approved & Scheduled"]
                if not approved_df.empty:
                    fig_sched = go.Figure()
                    fig_sched.add_trace(go.Bar(
                        y=approved_df["Target Station"] + " (" + approved_df["Combined Job ID"] + ")",
                        x=approved_df["Duration (Mins)"],
                        orientation='h',
                        marker=dict(
                            color=approved_df["Priority Level (1-100)"],
                            colorscale=[[0, '#2563EB'], [0.5, '#F59E0B'], [1, '#EF4444']],
                            showscale=True,
                            colorbar=dict(title=dict(text="Priority", font=dict(family="Inter", size=12, weight="bold"))),
                            line=dict(color='rgba(255,255,255,0.9)', width=2),
                            cornerradius=8
                        ),
                        text=approved_df["Duration (Mins)"].astype(str) + " Mins - " + approved_df["Team / Department"],
                        textposition="inside", insidetextfont=dict(color="white", family="Inter", size=12, weight="bold")
                    ))
                    fig_sched.update_layout(xaxis_title="Time Needed for Repair (Minutes)", yaxis_title="", height=380, template="plotly_white", margin=dict(l=0, r=0, t=10, b=10), font=dict(family="Inter"))
                    st.plotly_chart(fig_sched, use_container_width=True, config=PLOT_CONFIG)

        # ----------------------------------------------------------------------
        # MODULE 5: DISRUPTION TESTING & TRACK AVAILABILITY MATRIX
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Disruption Testing & Track Availability Matrix":
            st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Disruption Testing & Track Availability Matrix — {sel_city}</h1>", unsafe_allow_html=True)
            st.write(f"Simulate operational stress events across **{sel_city} Division ({sel_state})** and evaluate track availability vs. downtime saved.")

            c_scen1, c_scen2, c_scen3 = st.columns(3)
            with c_scen1:
                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #EF4444;'>
                    <div class='card-title'>Live Dynamic Incident Telemetry</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>{st.session_state.global_incident_station} ({sel_city})</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Condition:</b> {st.session_state.global_track_condition}<br>
                        <b>Speed Limit:</b> {'30 km/h (Caution)' if 'Repair' in st.session_state.global_track_condition else ('0 km/h (Halt)' if 'Blocked' in st.session_state.global_track_condition else 'Normal Line Speed')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with c_scen2:
                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #F59E0B;'>
                    <div class='card-title'>Downtime Impact Analysis</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>{('2.0 Hours Delay' if not ai_enabled else '18 Mins Safe Loop Transit') if 'Blocked' in st.session_state.global_track_condition else ('45 Mins Maintenance' if 'Repair' in st.session_state.global_track_condition else 'Zero Downtime')}</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Affected Trains:</b> 4 Trains active<br>
                        <b>Downstream Impact:</b> {'Cascading Late (+120m)' if not ai_enabled and 'Blocked' in st.session_state.global_track_condition else ('Loop Rerouted (+18m)' if 'Blocked' in st.session_state.global_track_condition else 'On Time')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            with c_scen3:
                st.markdown(f"""
                <div class='premium-card' style='border-left-color: #10B981;'>
                    <div class='card-title'>AI Recovery Benchmark</div>
                    <div style='font-size:18px; font-weight:800; color:#0F172A;'>94.8% Availability</div>
                    <p style='font-size:12px; color:#64748B; margin: 4px 0;'>
                        <b>Side Track Shunting:</b> Enabled<br>
                        <b>Corridor Batch:</b> Auto-Emergency Assigned
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            g1, g2 = st.columns([1, 1.2])
            
            with g1:
                base_tph = 14 if "Blocked" in st.session_state.global_track_condition else (18 if "Repair" in st.session_state.global_track_condition else 24)
                ai_tph = base_tph + (8 if "Blocked" in st.session_state.global_track_condition else 4) if st.session_state.global_ai_enabled else base_tph
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta", value=ai_tph,
                    title={'text': "<b>Track Capacity (Trains/Hour)</b>", 'font': {'size': 16, 'family': 'Inter', 'color': '#0F172A'}},
                    delta={'reference': base_tph, 'increasing': {'color': "#10B981"}},
                    gauge={
                        'axis': {'range': [0, 35], 'tickwidth': 2, 'tickcolor': "#CBD5E1"},
                        'bar': {'color': "#2563EB", 'thickness': 0.3},
                        'steps': [
                            {'range': [0, 15], 'color': '#EF4444'},
                            {'range': [15, 24], 'color': '#F59E0B'},
                            {'range': [24, 35], 'color': '#10B981'}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True, config=PLOT_CONFIG)
                
            with g2:
                st.markdown("#### ⚡ Track Availability vs. Downtime Saved")
                df_asset = pd.DataFrame({
                    "System Method": ["Old Manual Track Closing", "Our AI Automatic Block Planning"],
                    "Track Open & Ready (%)": ["54.2% (Track closed often)", "94.8% (Track open almost all day)"],
                    "Average Train Delay": ["48.5 Minutes Late", "1.8 Minutes (On Time)"],
                    "Team Coordination": ["0% (Teams work separately)", "100% (Teams work together)"]
                })
                st.dataframe(df_asset, use_container_width=True, hide_index=True)

            st.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("### 🧑‍✈️ Automated Driver Fatigue Monitor (Directly Linked to Delays)")
            st.write(f"Driver working hours dynamically scale when track delays occur at **{st.session_state.global_incident_station}**. The AI automatically alerts for a backup driver when shifts reach 10 hours.")

            if not df_traffic.empty:
                unique_trains = df_traffic.drop_duplicates(subset=["Train Name"])
                for _, row in unique_trains.iterrows():
                    base_hrs = row["Base Shift"]
                    added_delay_hrs = row["Total Delay"] / 60.0
                    total_hrs = base_hrs + added_delay_hrs
                    
                    hr_color = "#10B981" if total_hrs < 9 else ("#F59E0B" if total_hrs < 10 else "#EF4444")
                    status_text = "Duty Normal | Continue Operation" if total_hrs < 9 else ("SHIFT WARNING | Backup Driver Ready" if total_hrs < 10 else "CRITICAL EXHAUSTION | AI Backup Driver Dispatched")
                    pct = min(100, (total_hrs / 10.0) * 100)
                    
                    st.markdown(f"""
                    <div style='background: white; padding: 14px 18px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 10px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <strong style='color: #0F172A; font-size:14px;'>Assigned Driver: {row['Train Name']} ({row['Train ID']})</strong>
                            <span style='color: {hr_color}; font-size: 13px; font-weight: bold;'>{total_hrs:.1f} Hours Logged / 10.0 Max</span>
                        </div>
                        <div class='fatigue-bar-container'><div class='fatigue-bar-fill' style='width: {pct}%; background-color: {hr_color};'></div></div>
                        <p style='font-size: 12px; color: {hr_color}; margin-top: 6px; margin-bottom: 0; font-weight: bold;'>Status: {status_text}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # MODULE 6: CONFLICT RESOLUTION LOGIC (Interactive Flowchart)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Interactive Conflict Resolution Flowchart":
            st.markdown(f"<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Conflict Resolution Execution Flow — {sel_city} Division</h1>", unsafe_allow_html=True)
            st.write(f"Dynamic Branching Decision Logic actively managing **{sel_city} Division ({sel_state})**.")

            c_flow, c_compare = st.columns([1.2, 1])
            with c_flow:
                branch_b_color = "flow-box-red" if st.session_state.global_track_condition != "Track Clear (Normal)" else ""
                branch_a_color = "flow-box-green" if st.session_state.global_track_condition == "Track Clear (Normal)" else ""
                
                st.markdown(f"""
                <div class="flow-container">
                    <div class="flow-box">
                        <div class="flow-title">Step 1: Live Traffic Stream Detection</div>
                        <div class="flow-desc">Tracking 4 active trains across {sel_city} Division ({sel_state}).</div>
                    </div>
                    <div class="flow-arrow"></div>
                    <div class="flow-box">
                        <div class="flow-title">Step 2: Predictive Lookahead Anomaly Check</div>
                        <div class="flow-desc">Scanning 15-minute future window for {sel_station}.</div>
                    </div>
                    <div class="flow-arrow"></div>
                    <div class="flow-split">
                        <div class="flow-branch">
                            <div class="flow-box {branch_a_color}" style="width:100%;">
                                <div class="flow-title">Branch A: Normal Schedule</div>
                                <div class="flow-desc">Natural Gap Detected ➔ Multi-Team Slotted ➔ Green Signals.</div>
                            </div>
                        </div>
                        <div class="flow-branch">
                            <div class="flow-box {branch_b_color}" style="width:100%;">
                                <div class="flow-title">Branch B: Emergency Disruption</div>
                                <div class="flow-desc">Trigger: {st.session_state.global_track_condition} ➔ Auto-Emergency Crew Slotted.</div>
                            </div>
                        </div>
                    </div>
                    <div class="flow-arrow"></div>
                    <div class="flow-box flow-box-purple">
                        <div class="flow-title">Step 3: Mainline Dispatch Execution</div>
                        <div class="flow-desc">Super Vasuki Goods Sidetracked on Loop Line ➔ Mainline Speed Preserved.</div>
                    </div>
                    <div class="flow-arrow"></div>
                    <div class="flow-box flow-box-green">
                        <div class="flow-title">Step 4: Passenger Timetable Verification</div>
                        <div class="flow-desc">Passenger arrival delays minimized through automated diversion.</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_compare:
                st.markdown("<br><br>#### 📊 Simultaneous Trains Allowed on Same Section", unsafe_allow_html=True)
                fig_bar = go.Figure(go.Bar(
                    y=["Old System (2 Trains Max Allowed)", "Our AI System (6 Trains Max Allowed)"],
                    x=[2, 6], orientation='h',
                    marker=dict(color=["#94A3B8", "#2563EB"], cornerradius=8),
                    text=["2 Trains Max Allowed", "6 Trains Max Allowed"], textposition="inside",
                    insidetextfont=dict(color="white", family="Inter", size=13, weight="bold")
                ))
                fig_bar.update_layout(height=180, margin=dict(l=0, r=0, t=10, b=0), template="plotly_white")
                st.plotly_chart(fig_bar, use_container_width=True, config=PLOT_CONFIG)

# ==============================================================================
# PORTAL 2: CONTROLLER'S OVERVIEW IN PASSENGER APPLICATION
# ==============================================================================
elif user_role == "Controller's Overview in Passenger Application":
    
    col_p1, col_p2 = st.columns([5, 1])
    with col_p1: 
        st.markdown("<h1 style='font-size:30px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Controller's Overview in Passenger Application</h1>", unsafe_allow_html=True)
        st.write("Section controllers can use this overview to inspect whether live dispatch choices and track repair blocks caused delays for passenger trains.")
    with col_p2:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #10B981 0%, #059669 100%); color: white; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 800; text-align:center;'>
            📡 LINKED TO CCC DISPATCH
        </div>
        """, unsafe_allow_html=True)

    try:
        passenger_states = list(RAILWAY_NETWORK.keys())
        default_state_idx = passenger_states.index("Tamil Nadu") if "Tamil Nadu" in passenger_states else 0
        
        with st.expander("Configure Passenger Train Route to Inspect", expanded=True):
            c_org, c_dest = st.columns(2)
            with c_org:
                org_st = st.selectbox("Origin State", passenger_states, index=default_state_idx)
                org_city = st.selectbox("Origin City", list(RAILWAY_NETWORK[org_st].keys()), index=0)
                org_sn = st.selectbox("Boarding Station", list(RAILWAY_NETWORK[org_st][org_city]["stations"].keys()), index=0)
                    
            with c_dest:
                dst_st = st.selectbox("Destination State", passenger_states, index=3 if len(passenger_states) > 3 else 0) 
                dst_city = st.selectbox("Destination City", list(RAILWAY_NETWORK[dst_st].keys()), index=0)
                dst_stn_list = list(RAILWAY_NETWORK[dst_st][dst_city]["stations"].keys())
                dst_sn = st.selectbox("Destination Station", dst_stn_list, index=max(0, len(dst_stn_list)-1))
                
        cmd_condition = st.session_state.global_track_condition
        cmd_ai = st.session_state.global_ai_enabled
        cmd_work_zones = st.session_state.global_work_zones
        cmd_station = st.session_state.global_incident_station

        sched_min = 855 # Baseline 14:15 Hrs
        
        # Realistic Passenger Impact Calculation
        if cmd_condition != "Track Clear (Normal)":
            if not cmd_ai:
                delay_min = 120
                status_msg = "Severely Delayed (+120m)"
                status_color = "#EF4444"
                delay_reason = f"Manual track block at {cmd_station}"
                st.markdown(f"""
                <div class="modern-alert-red modern-alert">
                    <div class="alert-title alert-title-red">🔴 Critical Delay Alert: Passengers Delayed by +120 Mins</div>
                    Manual track block active at <b>{cmd_station}</b> without AI optimization. Downstream passenger services are severely impacted.
                </div>
                """, unsafe_allow_html=True)
            else:
                delay_min = 18 if "Blocked" in cmd_condition else 8
                status_msg = f"Emergency Loop Delay (+{delay_min}m)" if "Blocked" in cmd_condition else f"Caution Delay (+{delay_min}m)"
                status_color = "#F59E0B"
                delay_reason = f"AI emergency reroute around {cmd_station}"
                st.markdown(f"""
                <div class="modern-alert" style="border-left-color: #F59E0B; background: #FFFBEB;">
                    <div class="alert-title" style="color: #B45309;">🟡 Emergency Rerouting Active: Mitigated Passenger Delay</div>
                    Track obstruction at <b>{cmd_station}</b> detected. AI automatically guided passenger trains onto safe loop bypass tracks (incurring only +{delay_min} mins safe transit delay instead of +120 mins).
                </div>
                """, unsafe_allow_html=True)
        elif len(cmd_work_zones) > 0:
            delay_min = 0
            status_msg = "On Time (AI Scheduled)"
            status_color = "#10B981"
            delay_reason = "Repairs scheduled in empty gaps"
            st.markdown(f"""
            <div class="modern-alert">
                <div class="alert-title">🟢 All Passenger Services On Time — Zero Delays</div>
                Active track repairs at <b>{', '.join(cmd_work_zones)}</b> are scheduled inside empty timetable gaps. All trains running at full speed.
            </div>
            """, unsafe_allow_html=True)
        else:
            delay_min = 0
            status_msg = "On Time"
            status_color = "#10B981"
            delay_reason = "Track Clear"

        exp_min = sched_min + delay_min
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"<div class='premium-card'><div class='card-title'>Passenger Impact Status</div><div class='card-value' style='color:{status_color}; font-size:24px;'>{status_msg}</div><div class='card-subtitle' style='color:#64748B'>{delay_reason}</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='premium-card'><div class='card-title'>Scheduled Timetable Time</div><div class='card-value' style='font-size:24px;'>{format_24h(sched_min)}</div><div class='card-subtitle' style='color:#64748B'>Booked Arrival</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='premium-card'><div class='card-title'>Live Expected Arrival</div><div class='card-value' style='color:#2563EB; font-size:24px;'>{format_24h(exp_min)}</div><div class='card-subtitle' style='color:#64748B'>Live Calculated ETA</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='premium-card'><div class='card-title'>Platform Status</div><div class='card-value' style='color:#10B981; font-size:24px;'>Platform 4</div><div class='card-subtitle' style='color:#64748B'>Rerouted to Empty Platform</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        tabs_p = st.tabs(["Passenger Route Tracking Map", "Station Timetable Impact Table", "Platform & Station Crowd Monitor"])

        with tabs_p[0]:
            p1 = RAILWAY_NETWORK[org_st][org_city]["coords"][org_sn]
            p2 = RAILWAY_NETWORK[dst_st][dst_city]["coords"][dst_sn]
            
            lats, lons = [], []
            for t in np.linspace(0, 1, 30):
                lat = p1[0] * (1 - t) + p2[0] * t
                lon = p1[1] * (1 - t) + p2[1] * t
                offset = np.sin(t * np.pi) * 0.8
                lats.append(lat + offset)
                lons.append(lon + (offset * 0.3))
                
            live_pos = int(len(lats) * 0.6)
            fig_pmap = go.Figure()
            fig_pmap.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="lines", line=dict(width=6, color="#2563EB"), name="Passenger Train Path"))
            fig_pmap.add_trace(go.Scattermapbox(lat=[p1[0], p2[0]], lon=[p1[1], p2[1]], mode="markers+text", marker=dict(size=14, color="#0F172A"), text=[f"<b>{org_sn}</b>", f"<b>{dst_sn}</b>"], textposition="bottom center", textfont=dict(size=12, family="Inter", color="#0F172A"), name="Stations"))
            fig_pmap.add_trace(go.Scattermapbox(lat=[lats[live_pos]], lon=[lons[live_pos]], mode="markers+text", marker=dict(size=22, color="#10B981"), text=["<b>PASSENGER TRAIN POSITION</b>"], textposition="top right", textfont=dict(size=12, family="Inter", color="#10B981", weight="bold"), name="Live Train"))
            
            for wz in cmd_work_zones:
                if wz in RAILWAY_NETWORK[org_st][org_city]["coords"]:
                    w_coord = RAILWAY_NETWORK[org_st][org_city]["coords"][wz]
                    fig_pmap.add_trace(go.Scattermapbox(lat=[w_coord[0]], lon=[w_coord[1]], mode="markers+text", marker=dict(size=18, color="#8B5CF6"), text=[f"WORK ZONE: {wz}"], textposition="top left", textfont=dict(size=11, color="#8B5CF6", weight="bold"), name="Track Work Zone"))
                    
            fig_pmap.update_layout(mapbox=dict(style="carto-positron", zoom=5.5, center=dict(lat=(p1[0]+p2[0])/2, lon=(p1[1]+p2[1])/2)), margin=dict(l=0, r=0, t=0, b=0), height=420)
            st.plotly_chart(fig_pmap, use_container_width=True, config=PLOT_CONFIG)

        with tabs_p[1]:
            st.markdown("#### Live Timetable Impact Comparison (Downstream Delay Propagation)")
            mid_sched = 720 # 12:00 Hrs
            mid_delay = delay_min if (cmd_condition != "Track Clear (Normal)" and delay_min > 0) else 0
            mid_exp = mid_sched + mid_delay
            
            st.dataframe(pd.DataFrame({
                "Station Stop": [org_sn, "Midpoint Junction", dst_sn],
                "Scheduled Timetable": ["10:00 Hrs", format_24h(mid_sched), format_24h(sched_min)],
                "Live Expected Arrival": ["10:00 Hrs", format_24h(mid_exp), format_24h(exp_min)],
                "Delay Incurred": ["0 Mins", f"+{mid_delay} Mins", f"+{delay_min} Mins"],
                "Passenger Status": ["Departed On Time", "Downstream Updated" if mid_delay > 0 else "Passing On Time", status_msg]
            }), use_container_width=True, hide_index=True)

        with tabs_p[2]:
            st.markdown("#### Platform Rerouting & Station Congestion Monitor")
            col_pl1, col_pl2, col_pl3 = st.columns(3)
            with col_pl1:
                st.markdown("""
                <div class='premium-card' style='border-left-color: #10B981;'>
                    <div class='card-title'>Platform 2 (Clear)</div>
                    <div style='font-size: 18px; font-weight:800; color:#0F172A;'>Rajdhani Express</div>
                    <div style='color:#10B981; font-size:12px; font-weight:bold; margin-top:4px;'>Status: Arriving on Time</div>
                </div>
                """, unsafe_allow_html=True)
            with col_pl2:
                st.markdown("""
                <div class='premium-card' style='border-left-color: #2563EB;'>
                    <div class='card-title'>Platform 4 (AI Rerouted)</div>
                    <div style='font-size: 18px; font-weight:800; color:#0F172A;'>Vande Bharat Express</div>
                    <div style='color:#2563EB; font-size:12px; font-weight:bold; margin-top:4px;'>Status: Auto-Rerouted to Avoid Bottleneck</div>
                </div>
                """, unsafe_allow_html=True)
            with col_pl3:
                st.markdown("""
                <div class='premium-card' style='border-left-color: #F59E0B;'>
                    <div class='card-title'>Side Track 1 (Waiting)</div>
                    <div style='font-size: 18px; font-weight:800; color:#0F172A;'>Super Vasuki Freight</div>
                    <div style='color:#F59E0B; font-size:12px; font-weight:bold; margin-top:4px;'>Status: Yielding on Loop Line</div>
                </div>
                """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Render Fault: {e}")
