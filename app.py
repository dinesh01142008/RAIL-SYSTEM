import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, time, timedelta

# --- 1. NEXT-GEN 2026 ENTERPRISE CSS (VIBRANT & DYNAMIC) ---
st.set_page_config(page_title="Future Railway System | SIH 2026", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
    
    .stApp { background-color: #F4F7F9; font-family: 'Inter', sans-serif; }
    .css-18e3th9 { padding-top: 1rem; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F0F4F8 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    div[role="radiogroup"] { gap: 12px; }
    div[role="radiogroup"] > label {
        background: #FFFFFF;
        padding: 14px 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { 
        background: #FFFFFF; 
        transform: translateX(6px); 
        border-color: #3B82F6;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15); 
    }
    
    .premium-card {
        background: #FFFFFF;
        border-radius: 16px; padding: 22px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.04); 
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .premium-card::before {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        z-index: 1; pointer-events: none;
    }
    .premium-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.15); 
        border-left: 6px solid #10B981; 
    }
    
    .workflow-node {
        background: #FFFFFF;
        border-radius: 14px; padding: 20px; margin-bottom: 14px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        border-left: 5px solid #CBD5E1;
        transition: all 0.3s ease;
    }
    .workflow-node:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(15, 23, 42, 0.08);
    }
    .node-active { border-left-color: #10B981; }
    .node-alert { border-left-color: #EF4444; animation: pulse-red 2s infinite; }
    .node-caution { border-left-color: #F59E0B; }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    .w-title { font-size: 15px; font-weight: 800; color: #0F172A; display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;}
    .w-subtitle { font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 1.2px;}
    .w-status { font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase;}
    
    .card-title { color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 1.2px; margin-bottom: 6px; z-index: 2; position: relative;}
    .card-value { color: #0F172A; font-size: 32px; font-weight: 900; line-height: 1.1; z-index: 2; position: relative; background: -webkit-linear-gradient(45deg, #0F172A, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .card-subtitle { font-size: 12px; font-weight: 600; margin-top: 6px; z-index: 2; position: relative;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 25px; border-bottom: 2px solid #E2E8F0; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab"] { height: 45px; font-weight: 700; font-size: 15px; color: #94A3B8; background: transparent; border: none; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; font-weight: 800; }
    
    .modern-alert {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 5px solid #4F46E5; padding: 20px 24px; border-radius: 12px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.15); color: #1E293B;
        font-size: 14px; line-height: 1.6; margin-bottom: 25px; border: 1px solid #C7D2FE;
    }
    .modern-alert-red { 
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 5px solid #EF4444; border-color: #FECACA;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.15); 
    }
    .alert-title { font-weight: 900; font-size: 15px; color: #3730A3; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.8px;}
    .alert-title-red { color: #991B1B; }
    
    .stButton>button { border-radius: 10px; font-weight: 800; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; border: none; padding: 12px 28px; transition: all 0.3s; box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25); }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 12px 25px rgba(37, 99, 235, 0.4); color: white; }
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; }
    .login-container { max-width: 440px; margin: 80px auto; padding: 45px 35px; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.08); text-align: center; border: 1px solid #F1F5F9; border-top: 6px solid #2563EB;}
    
    /* Custom Progress Bars for Staff Optimization */
    .fatigue-bar-container { width: 100%; background-color: #E2E8F0; border-radius: 8px; margin-top: 8px; overflow: hidden; height: 10px;}
    .fatigue-bar-safe { height: 100%; background-color: #10B981; width: 45%; }
    .fatigue-bar-warn { height: 100%; background-color: #F59E0B; width: 75%; }
    .fatigue-bar-critical { height: 100%; background-color: #EF4444; width: 95%; animation: pulse-red 2s infinite; }
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {'displayModeBar': False, 'scrollZoom': True} 

# --- 2. AUTHENTICATION & NAVIGATION PROTOCOL ---
if "staff_authenticated" not in st.session_state: st.session_state.staff_authenticated = False
if "auth_error" not in st.session_state: st.session_state.auth_error = False
if "active_tab" not in st.session_state: st.session_state.active_tab = "Live Traffic Dashboard"

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
    st.session_state.active_tab = "Live Traffic Dashboard"

def format_24h(minutes):
    try:
        total_mins = int(minutes) % 1440
        hrs = total_mins // 60
        mins = total_mins % 60
        return f"{hrs:02d}:{mins:02d} Hrs"
    except Exception:
        return "00:00 Hrs"

# --- 3. MASSIVE ENTERPRISE GPS DATABASE (15 States, 30 Divisions) ---
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

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h2 style="color:#0F172A; font-weight:900; letter-spacing:-1px; margin-bottom: -5px; margin-top: 10px;">FUTURE RAILWAY SYSTEM</h2>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:10px; font-weight:800; color:#2563EB; margin-bottom:25px; line-height:1.4; letter-spacing: 0.5px;'>SIH 2026: CONFLICT DETECTION & RESOLUTION — MAXIMIZING SECTION THROUGHPUT USING AI-POWERED PRECISE TRAIN TRAFFIC CONTROL</p>", unsafe_allow_html=True)
    user_role = st.radio("Access Level", ["Passenger Application", "Central Command Center"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)

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
                <p style="color:#64748B; margin-bottom:25px; font-size:14px; font-weight:600;">Traffic Control Server</p>
            </div>
            """, unsafe_allow_html=True)
            st.text_input("Enter Passkey", type="password", key="pwd_input", label_visibility="collapsed")
            st.button("Authenticate", on_click=check_password, use_container_width=True)
            if st.session_state.auth_error: st.error("Access Denied: Invalid Credentials.")
                
    else:
        staff_module = st.sidebar.radio("Control Modules", ["Live Traffic Dashboard", "Conflict Resolution Logic", "Software Optimization"], key="active_tab")
        st.sidebar.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
        
        with st.sidebar:
            st.markdown("<h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>OPERATIONAL TERRITORY</h3>", unsafe_allow_html=True)
            try:
                sel_state = st.selectbox("State", list(RAILWAY_NETWORK.keys()), index=0, label_visibility="collapsed")
                city_options = list(RAILWAY_NETWORK[sel_state].keys())
                sel_city = st.selectbox("Division", city_options, index=0, label_visibility="collapsed")
                if sel_city not in city_options: sel_city = city_options[0]
                
                sector_data = RAILWAY_NETWORK[sel_state][sel_city]
                current_sector = sector_data["stations"]
                current_coords = sector_data["coords"]
                station_list = list(current_sector.keys())
                mid_station_idx = max(0, min(2, len(station_list)-1)) 
                
                st.markdown("<br><h3 style='font-size:11px; color:#64748B; font-weight:800; letter-spacing:1px;'>INCIDENT SIMULATOR</h3>", unsafe_allow_html=True)
                sel_station = st.selectbox("Target Station", station_list, index=0)
                if sel_station not in station_list: sel_station = station_list[0]
                    
                track_status = st.selectbox("Track Condition", ["Track Clear (Normal)", "Track Repair (Slow Speed)", "Track Blocked (Sensor Alert)"], on_change=trigger_ai_focus)
                
                st.markdown("<hr style='border-color:#E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
                ai_enabled = st.toggle("Enable AI Traffic Optimizer", value=True)
            except Exception as e:
                st.error(f"Data Sync Error: {e}")
                st.stop()

        def process_telemetry(damaged_stn, status, ai, sector_dict):
            try:
                vb_speed, exp_speed, fr_speed = 110, 85, 45
                trains = [
                    {"name": "Vande Bharat Express", "id": "VB-2026", "type": "High-Speed", "speed": vb_speed, "start_min": 540, "weight": 2, "color": "#10B981"}, 
                    {"name": "Super Vasuki Goods Train", "id": "FRT-8802", "type": "Freight", "speed": fr_speed, "start_min": 528, "weight": 3, "color": "#F59E0B"},    
                    {"name": "Rajdhani Express", "id": "RAJ-1260", "type": "Express", "speed": exp_speed, "start_min": 558, "weight": 2, "color": "#3B82F6"}   
                ]
                
                if ai: trains = sorted(trains, key=lambda x: x["weight"])
                    
                records = []
                for t in trains:
                    curr_time = t["start_min"]
                    prev_dist = 0
                    for stn, dist in sector_dict.items():
                        current_speed = t["speed"]
                        dwell = 2 
                        track = "Main Track"
                        node_condition = "Clear"

                        if stn == damaged_stn:
                            node_condition = status
                            if status == "Track Repair (Slow Speed)": 
                                current_speed = min(current_speed, 30)
                            elif status == "Track Blocked (Sensor Alert)":
                                if t["type"] == "Freight": dwell = 45 if not ai else 15
                                
                        mid_station = list(sector_dict.keys())[mid_station_idx] 
                        if ai and t["type"] == "Freight" and stn == mid_station:
                            dwell += 20
                            track = "Side Track (Waiting Line)"
                        
                        if not ai and t["type"] != "Freight" and status == "Track Blocked (Sensor Alert)" and dist >= sector_dict.get(damaged_stn, 999):
                            curr_time += 45
                            
                        dist_delta = dist - prev_dist if dist > prev_dist else 0
                        travel_time = (dist_delta / current_speed) * 60
                        
                        arrival = curr_time + travel_time
                        departure = arrival + dwell
                        curr_time = departure 
                        prev_dist = dist
                        
                        records.append({
                            "Train Name": t["name"], "Train ID": t["id"], "Station": stn, "Dist": dist, 
                            "Arrival_Mins": arrival, "Arrival 24H": format_24h(arrival),
                            "Wait Time at Station": f"{int(dwell)} mins", "Track Path Assigned": track, "Track Condition": node_condition, "Color": t["color"]
                        })
                return pd.DataFrame(records)
            except Exception:
                return pd.DataFrame(columns=["Train Name", "Train ID Number", "Current Station", "Dist", "Arrival_Mins", "Arrival Time", "Wait Time at Station", "Track Path Assigned", "Track Condition", "Color"])

        df_traffic = process_telemetry(sel_station, track_status, ai_enabled, current_sector)

        # ----------------------------------------------------------------------
        # VIEW 1: LIVE TRAFFIC DASHBOARD
        # ----------------------------------------------------------------------
        if st.session_state.active_tab == "Live Traffic Dashboard":
            st.markdown('<img src="https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=2000&q=80" style="width:100%; height:140px; object-fit:cover; border-radius:18px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1: st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Central Network Command</h1>", unsafe_allow_html=True)
            with col_t2: st.button("Logout Session", on_click=logout, type="secondary", use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            base_tph = 14 if "Blocked" in track_status else (18 if "Repair" in track_status else 24)
            ai_tph = base_tph + (8 if "Blocked" in track_status else 4) if ai_enabled else base_tph
            
            with c1: st.markdown(f"<div class='premium-card'><div class='card-title'>Active Trains</div><div class='card-value'>142</div><div class='card-subtitle' style='color:#64748B'>{sel_city} Region</div></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='premium-card'><div class='card-title'>Hardware Sensors</div><div class='card-value'>{'0' if ai_enabled else ('Alert' if track_status != 'Track Clear (Normal)' else '0')}</div><div class='card-subtitle' style='color:#10B981'>{'AI Auto-Resolved' if ai_enabled and track_status != 'Track Clear (Normal)' else 'Network Safe'}</div></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='premium-card'><div class='card-title'>Track Efficiency</div><div class='card-value'>{ai_tph}</div><div class='card-subtitle' style='color:#3B82F6'>Trains Per Hour</div></div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='premium-card'><div class='card-title'>AI Decision Engine</div><div class='card-value'>{'ONLINE' if ai_enabled else 'OFFLINE'}</div><div class='card-subtitle' style='color:{'#10B981' if ai_enabled else '#EF4444'}'>{'Smart Traffic Routing' if ai_enabled else 'Old Manual Routing'}</div></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if track_status != "Track Clear (Normal)":
                if ai_enabled:
                    st.markdown(f"""
                    <div class="modern-alert">
                        <div class="alert-title">AI Action Log: Traffic Conflict Automatically Resolved</div>
                        <strong>Sensor Alert:</strong> Anomaly detected as '{track_status}' at {sel_station}.<br>
                        <strong>AI Resolution:</strong> Software immediately recalculated safe braking distances for all active trains.<br>
                        <strong>Automated Routing:</strong> Super Vasuki Goods Train automatically diverted to a side track to allow Vande Bharat Express to pass without stopping.<br>
                        <strong>Final Outcome:</strong> Traffic jam prevented. Maximum track capacity maintained at {ai_tph} Trains/Hour.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="modern-alert modern-alert-red">
                        <div class="alert-title alert-title-red">Critical Alert: AI Routing Offline</div>
                        <strong>Sensor Alert:</strong> Track condition reported as '{track_status}' at {sel_station}.<br>
                        <strong>Fallback Mode:</strong> Reverting to old manual fixed-distance rules.<br>
                        <strong>Final Outcome:</strong> Severe traffic jam. Trains forced to stop completely. Efficiency drops to {base_tph} Trains/Hour.
                    </div>
                    """, unsafe_allow_html=True)

            try:
                tabs = st.tabs(["Live GPS Tracking Map", "Real-Time Schedule", "Interactive Traffic Simulation", "Time vs Distance Graph"])
                tab_openmap = tabs[0]; tab_schedule = tabs[1]; tab_radar = tabs[2]; tab_graph = tabs[3]
                
                with tab_openmap:
                    st.markdown(f"#### Geographic Tracking Map — {sel_city} Region ({sel_state})")
                    st.write("Live visualization of physical train routes, station stops, and dynamic hardware sensor conditions.")
                    
                    stn_names = list(current_coords.keys())
                    lats = [current_coords[s][0] for s in stn_names]
                    lons = [current_coords[s][1] for s in stn_names]
                    
                    fig_openmap = go.Figure()
                    
                    fig_openmap.add_trace(go.Scattermapbox(
                        lat=lats, lon=lons, mode="lines",
                        line=dict(width=8, color="#1E293B"),
                        name="Main Railway Track",
                        hoverinfo="skip"
                    ))
                    
                    track_color = "#10B981" if track_status == "Track Clear (Normal)" else ("#F59E0B" if "Repair" in track_status else "#EF4444")
                    fig_openmap.add_trace(go.Scattermapbox(
                        lat=lats, lon=lons, mode="lines",
                        line=dict(width=4, color=track_color),
                        name=f"Current Track Status: {track_status}",
                        hoverinfo="name"
                    ))
                    
                    fig_openmap.add_trace(go.Scattermapbox(
                        lat=lats, lon=lons, mode="markers+text",
                        marker=dict(size=15, color="#2563EB"),
                        text=stn_names,
                        textposition="top right",
                        textfont=dict(size=13, family="Inter", color="#0F172A", weight="bold"),
                        name="Station Stops",
                        hovertemplate="<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>"
                    ))
                    
                    if track_status != "Track Clear (Normal)":
                        dmg_coord = current_coords.get(sel_station, (lats[0], lons[0]))
                        fig_openmap.add_trace(go.Scattermapbox(
                            lat=[dmg_coord[0]], lon=[dmg_coord[1]], mode="markers+text",
                            marker=dict(size=26, color="#EF4444", opacity=0.8),
                            text=[f"ALERT: {sel_station}"],
                            textposition="bottom right",
                            textfont=dict(size=13, color="#EF4444", family="Inter", weight="bold"),
                            name="Incident Area",
                            hovertemplate="<b>Incident Area: %{text}</b><extra></extra>"
                        ))
                    
                    if len(lats) > 0 and len(lons) > 0:
                        center_lat = np.mean(lats)
                        center_lon = np.mean(lons)
                        
                        fig_openmap.update_layout(
                            mapbox=dict(style="carto-positron", zoom=9.5, center=dict(lat=center_lat, lon=center_lon)),
                            margin=dict(l=0, r=0, t=10, b=0),
                            height=480,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        st.plotly_chart(fig_openmap, use_container_width=True, config=PLOT_CONFIG)
                    st.markdown("<br>", unsafe_allow_html=True)

                with tab_schedule:
                    if not df_traffic.empty:
                        final_df = df_traffic[["Train Name", "Train ID", "Station", "Arrival 24H", "Wait Time at Station", "Track Path Assigned", "Track Condition"]]
                        final_df.columns = ["Train Name", "Train ID Number", "Current Station", "Arrival Time", "Wait Time at Station", "Track Path Assigned", "Track Condition"]
                        st.dataframe(final_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("System initializing traffic data. Waiting for valid tracking configurations.")
                    st.markdown("<br>", unsafe_allow_html=True)

                with tab_radar:
                    st.markdown("#### Interactive Temporal Traffic Simulation")
                    st.write("Adjust the timeline slider to strictly simulate where trains will be at any hour of the day. Notice how the AI mathematically avoids collisions.")
                    
                    selected_time = st.slider(
                        "Interactive Operations Timeline (HH:MM Format):",
                        min_value=time(8, 20),
                        max_value=time(12, 0),
                        value=time(9, 30),
                        step=timedelta(minutes=2),
                        format="HH:mm",
                        label_visibility="collapsed"
                    )
                    
                    sim_time_min = selected_time.hour * 60 + selected_time.minute
                    st.info(f"**Live Simulation Time:** {selected_time.strftime('%H:%M Hrs')} | **Focus Region:** {sel_city} Division")
                    
                    if not df_traffic.empty:
                        fig_radar = go.Figure()
                        max_dist = max(current_sector.values()) if len(current_sector) > 0 else 100
                        mid_dist = list(current_sector.values())[mid_station_idx]
                        
                        fig_radar.add_hline(y=1, line_dash="solid", line_color="#E2E8F0", line_width=6)
                        fig_radar.add_shape(type="line", x0=mid_dist-2, y0=1, x1=mid_dist, y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                        fig_radar.add_shape(type="line", x0=mid_dist, y0=1.5, x1=mid_dist+(max_dist*0.05), y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                        fig_radar.add_shape(type="line", x0=mid_dist+(max_dist*0.05), y0=1.5, x1=mid_dist+(max_dist*0.08), y1=1, line=dict(color="#E2E8F0", width=6)) 
                        
                        if track_status != "Track Clear (Normal)":
                            dmg_dist = current_sector.get(sel_station, 0)
                            dmg_color = "#EF4444" if "Blocked" in track_status else "#F59E0B"
                            fig_radar.add_shape(type="rect", x0=dmg_dist-1.5, y0=0.88, x1=dmg_dist+1.5, y1=1.12, fillcolor=dmg_color, opacity=0.9, line_width=0)
                            fig_radar.add_annotation(x=dmg_dist, y=0.72, text=f"<b>ALERT ZONE</b>", font=dict(color=dmg_color, size=12, family="Inter"), showarrow=False)

                        for t_name in df_traffic["Train Name"].unique():
                            sub = df_traffic[df_traffic["Train Name"] == t_name]
                            if sub.empty: continue
                            times, dists = sub["Arrival_Mins"].values, sub["Dist"].values
                            if len(times) == 0 or sim_time_min < times[0]: continue
                            current_dist = dists[-1] if sim_time_min > times[-1] else np.interp(sim_time_min, times, dists)
                            
                            y_pos = 1
                            if ai_enabled and t_name == "Super Vasuki Goods Train" and mid_dist <= current_dist <= mid_dist+(max_dist*0.05): y_pos = 1.5 
                            
                            color_val = sub["Color"].iloc[0]
                            tag_val = sub["Train ID"].iloc[0]
                            
                            fig_radar.add_trace(go.Scatter(
                                x=[current_dist], y=[y_pos], mode="markers+text",
                                marker=dict(size=24, color=color_val, line=dict(width=3, color="white")),
                                text=[tag_val], textposition="top center",
                                textfont=dict(size=12, color=color_val, family="Inter", weight="bold"),
                                name=t_name, hoverinfo="name"
                            ))

                        for stn, d in current_sector.items():
                            fig_radar.add_vline(x=d, line_dash="dot", line_color="#CBD5E1", annotation_text=f"  {stn.split(' ')[0]}", annotation_position="top left", annotation_font=dict(size=12, color="#64748B", family="Inter"))

                        fig_radar.update_layout(dragmode=False, yaxis=dict(showticklabels=False, range=[0.4, 2]), xaxis=dict(range=[-2, max_dist+(max_dist*0.1)], showgrid=False, zeroline=False), height=380, template="plotly_white", margin=dict(t=30, b=20), plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")
                        st.plotly_chart(fig_radar, use_container_width=True, config=PLOT_CONFIG)

                with tab_graph:
                    if not df_traffic.empty:
                        fig_marey = go.Figure()
                        for stn, d in current_sector.items():
                            fig_marey.add_hline(y=d, line_dash="dot", line_color="#E2E8F0", annotation_text=f" {stn.split(' ')[0]}", annotation_font=dict(color="#94A3B8", size=12))
                            
                        for t_name in df_traffic["Train Name"].unique():
                            sub = df_traffic[df_traffic["Train Name"] == t_name]
                            if sub.empty: continue
                            color_val = sub["Color"].iloc[0]
                            
                            fig_marey.add_trace(go.Scatter(
                                x=sub["Arrival_Mins"], y=sub["Dist"], mode="lines+markers",
                                name=t_name, line=dict(color=color_val, width=5, shape="spline"),
                                marker=dict(size=10, line=dict(width=2, color="white")),
                                hovertemplate="<b>%{text}</b><br>Time: %{customdata}<br>Distance: %{y} km<extra></extra>",
                                text=sub["Station"],
                                customdata=sub["Arrival 24H"]
                            ))
                        
                        fig_marey.update_layout(
                            dragmode=False, height=480,
                            xaxis_title="Simulation Timeline (Minutes elapsed from midnight)",
                            yaxis_title="Total Distance Traversed (km)",
                            template="plotly_white", plot_bgcolor="#FFFFFF",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            font=dict(family="Inter", size=13)
                        )
                        st.plotly_chart(fig_marey, use_container_width=True, config=PLOT_CONFIG)
            except Exception as e:
                st.error(f"Render System Error: {e}")
                
        # ----------------------------------------------------------------------
        # VIEW 2: AI LOGIC & CONFLICT RESOLUTION (SIH FOCUS)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Conflict Resolution Logic":
            st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Conflict Resolution Logic & Proof</h1>", unsafe_allow_html=True)
            st.write("This directly addresses the Smart India Hackathon problem statement: Maximizing section throughput using precise, AI-powered traffic control.")
            
            flow_state = "node-active"
            status_text = "SYSTEM NORMAL (NO CONFLICTS)"
            sm_action = "Automated routes verified. Traffic signals are GREEN."
            lp_action = "Trains proceeding at maximum permitted speed."
            status_color = "#10B981"
            
            if track_status == "Track Repair (Slow Speed)":
                flow_state = "node-caution"
                status_text = "PREDICTIVE SPEED REDUCTION"
                sm_action = "Software automatically switches signals to Caution (Yellow)."
                lp_action = "Train slowing down to mandatory 30 km/h safety limit."
                status_color = "#F59E0B"
            elif track_status == "Track Blocked (Sensor Alert)":
                flow_state = "node-alert"
                status_text = "CRITICAL TRAFFIC REROUTE"
                sm_action = "Main track blocked. AI unlocks side track for Goods Train to wait."
                lp_action = "Auto-braking engaged. Train safely moving to wait on the side track."
                status_color = "#EF4444"

            c_flow, c_dash = st.columns([1, 1.2])
            
            with c_flow:
                st.markdown("### 📡 Live Software Execution Flow")
                
                st.markdown(f"""
                <div style="padding: 5px;">
                    <div class="workflow-node node-active">
                        <div class="w-subtitle">Step 1 • AI Brain Server</div>
                        <div class="w-title">Central Traffic Algorithms <span class="w-status" style="background:#D1FAE5; color:#065F46;">Online</span></div>
                        <span style="font-size: 13px; color: #64748B;">Processing live GPS feeds to prevent train collisions.</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -8px 0; font-size: 20px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Step 2 • Track Assessment</div>
                        <div class="w-title">Routing Network Node <span class="w-status" style="background:{status_color}20; color:{status_color};">{status_text}</span></div>
                        <span style="font-size: 13px; color: #64748B;">Target area: <strong style="color:#0F172A;">{sel_station}</strong>. Transmitting movement permissions.</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -8px 0; font-size: 20px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Step 3 • Automated Station Hardware</div>
                        <div class="w-title">Station Server Control <span class="w-status" style="background:#F1F5F9; color:#334155;">Executing</span></div>
                        <span style="font-size: 13px; color: #64748B;">{sm_action}</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -8px 0; font-size: 20px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Step 4 • Train Execution</div>
                        <div class="w-title">Train Operator Dashboard <span class="w-status" style="background:#F1F5F9; color:#334155;">Responding</span></div>
                        <span style="font-size: 13px; color: #64748B;">{lp_action}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_dash:
                st.markdown("### ⚡ Maximized Section Throughput (Proof)")
                st.write("This visually demonstrates how our AI algorithm safely packs more trains onto the same physical track without hardware changes.")
                
                try:
                    base_tph = 14 if "Blocked" in track_status else (18 if "Repair" in track_status else 24)
                    ai_tph = base_tph + (8 if "Blocked" in track_status else 4) if ai_enabled else base_tph
                    
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = ai_tph,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "<b>Total Efficiency (Trains/Hour)</b>", 'font': {'size': 18, 'color': '#0F172A', 'family': 'Inter'}},
                        delta = {'reference': base_tph, 'increasing': {'color': "#10B981"}},
                        gauge = {
                            'axis': {'range': [None, 35], 'tickwidth': 2, 'tickcolor': "#CBD5E1"},
                            'bar': {'color': "#2563EB", 'thickness': 0.25},
                            'bgcolor': "#FFFFFF",
                            'borderwidth': 0,
                            'steps': [
                                {'range': [0, 15], 'color': '#FEF2F2'},
                                {'range': [15, 24], 'color': '#FFFBEB'},
                                {'range': [24, 35], 'color': '#ECFDF5'}
                            ],
                        }
                    ))
                    fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10), font=dict(family="Inter"))
                    st.plotly_chart(fig_gauge, use_container_width=True, config=PLOT_CONFIG)
                    
                    st.markdown("#### 📊 Old System vs. New AI System")
                    df_compare = pd.DataFrame({
                        "Software Type": ["Old Static System (Fixed Distance)", "Our AI System (Dynamic Distance)"],
                        "Simultaneous Trains Safely Allowed": [2, 6]
                    })
                    
                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(
                        y=df_compare["Software Type"],
                        x=df_compare["Simultaneous Trains Safely Allowed"],
                        orientation='h',
                        marker=dict(color=["#94A3B8", "#2563EB"], cornerradius=6),
                        text=["<b>2 Trains Max</b>", "<b>6 Trains Max</b>"],
                        textposition='inside',
                        insidetextanchor="middle",
                        textfont=dict(size=14, color="white", family="Inter"),
                        width=0.5
                    ))
                    fig_bar.update_layout(
                        height=180, margin=dict(l=0, r=0, t=10, b=0), 
                        xaxis=dict(title="Number of Active Trains Allowed on the Same Track", showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=13, color="#64748B")),
                        yaxis=dict(title="", showgrid=False),
                        template="plotly_white", plot_bgcolor="#FFFFFF", 
                        font=dict(family="Inter", size=14, color="#0F172A")
                    )
                    st.plotly_chart(fig_bar, use_container_width=True, config=PLOT_CONFIG)
                    
                except Exception as e:
                    st.error(f"Data mapping error: {e}")

        # ----------------------------------------------------------------------
        # VIEW 3: SOFTWARE OPTIMIZATION (UPGRADED UI & METRICS)
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Software Optimization":
            st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Advanced Software Optimization</h1>", unsafe_allow_html=True)
            st.write("Tackling massive software bottlenecks that delay trains without touching physical hardware: Manual platform allocation and staff shift fatigue.")
            
            t1, t2 = st.tabs(["Smart Platform Assignment Engine", "Predictive Staff Scheduling Engine"])
            
            with t1:
                st.markdown("### 🚉 AI Platform Re-assignment Matrix")
                st.write("Normally, trains wait outside stations for their specific numbered platform to clear. Our AI detects when a train is running late and instantly re-assigns the waiting train to any empty platform, preventing massive delays.")
                
                plat_status = "AI Optimizing Platforms" if ai_enabled else "Platform Traffic Jam Warning"
                plat_color = "#10B981" if ai_enabled else "#EF4444"
                
                st.markdown(f"<p style='font-weight: 800; color: {plat_color}; font-size: 16px; margin-bottom: 20px;'>Live Network Health: {plat_status}</p>", unsafe_allow_html=True)
                
                col_p1, col_p2, col_p3 = st.columns(3)
                
                with col_p1:
                    st.markdown("""
                    <div class='premium-card' style='border-left-color: #10B981;'>
                        <div class='card-title'>Platform 2</div>
                        <div class='card-value' style='font-size: 22px;'>Rajdhani Express</div>
                        <div class='card-subtitle' style='color:#64748B'>Occupancy: 12% - Status: Clear</div>
                        <hr style='margin: 10px 0; border-color:#E2E8F0;'>
                        <p style='font-size: 13px; font-weight: bold; color: #10B981; margin:0;'>Action: Train Proceeding Normally</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_p2:
                    status_text = "Action: Instantly Rerouted to Platform 4" if ai_enabled else "Action: CRITICAL TRAFFIC JAM (Waiting)"
                    border_color = "#2563EB" if ai_enabled else "#EF4444"
                    action_color = "#2563EB" if ai_enabled else "#EF4444"
                    st.markdown(f"""
                    <div class='premium-card' style='border-left-color: {border_color};'>
                        <div class='card-title'>Platform 2 (Conflict)</div>
                        <div class='card-value' style='font-size: 22px;'>Vande Bharat Express</div>
                        <div class='card-subtitle' style='color:#64748B'>Occupancy: 89% - Status: FULL</div>
                        <hr style='margin: 10px 0; border-color:#E2E8F0;'>
                        <p style='font-size: 13px; font-weight: bold; color: {action_color}; margin:0;'>{status_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_p3:
                    action_text2 = "Action: Stop and Wait on Side Track" if ai_enabled else "Action: Pending Human Decision"
                    st.markdown(f"""
                    <div class='premium-card' style='border-left-color: #F59E0B;'>
                        <div class='card-title'>Cargo Track 1</div>
                        <div class='card-value' style='font-size: 22px;'>Super Vasuki Goods</div>
                        <div class='card-subtitle' style='color:#64748B'>Occupancy: 45% - Status: Waiting to Pass</div>
                        <hr style='margin: 10px 0; border-color:#E2E8F0;'>
                        <p style='font-size: 13px; font-weight: bold; color: #F59E0B; margin:0;'>{action_text2}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            with t2:
                st.markdown("### 🧑‍✈️ Predictive Staff Shift Management")
                st.write("Train operators have strict legal limits on working hours. When trains are delayed, operators exceed their hours. Our software predicts this fatigue before it happens and automatically schedules a backup driver.")
                
                crew_status = "Driver Shifts AI-Optimized" if ai_enabled else "Severe Driver Exhaustion Detected"
                crew_color = "#2563EB" if ai_enabled else "#EF4444"
                
                st.markdown(f"<p style='font-weight: 800; color: {crew_color}; font-size: 16px; margin-bottom: 20px;'>Live Network Health: {crew_status}</p>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                        <strong style='color: #0F172A;'>Driver-9942 (Vande Bharat Express)</strong>
                        <span style='color: #64748B; font-size: 13px; font-weight: bold;'>07:45 Hrs logged / 10 Hrs Max</span>
                    </div>
                    <div class='fatigue-bar-container'><div class='fatigue-bar-safe'></div></div>
                    <p style='font-size: 13px; color: #10B981; margin-top: 8px; margin-bottom: 0; font-weight: bold;'>Status: Normal | AI Action: Continue Driving</p>
                </div>
                """, unsafe_allow_html=True)
                
                ai_crew_action = "Relief Backup Driver Dispatched to Next Station" if ai_enabled else "Awaiting Immediate Human Fix"
                bar_class = "fatigue-bar-warn" if ai_enabled else "fatigue-bar-critical"
                status_color_css = "#2563EB" if ai_enabled else "#EF4444"
                
                st.markdown(f"""
                <div style='background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                        <strong style='color: #0F172A;'>Driver-1184 (Super Vasuki Goods Train)</strong>
                        <span style='color: #EF4444; font-size: 13px; font-weight: bold;'>09:50 Hrs logged / 10 Hrs Max (OVERTIME RISK)</span>
                    </div>
                    <div class='fatigue-bar-container'><div class='{bar_class}'></div></div>
                    <p style='font-size: 13px; color: {status_color_css}; margin-top: 8px; margin-bottom: 0; font-weight: bold;'>Status: CRITICALLY EXHAUSTED | AI Action: {ai_crew_action}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                        <strong style='color: #0F172A;'>Driver-7703 (Rajdhani Express)</strong>
                        <span style='color: #64748B; font-size: 13px; font-weight: bold;'>04:20 Hrs logged / 10 Hrs Max</span>
                    </div>
                    <div class='fatigue-bar-container'><div class='fatigue-bar-safe' style='width: 25%;'></div></div>
                    <p style='font-size: 13px; color: #10B981; margin-top: 8px; margin-bottom: 0; font-weight: bold;'>Status: Normal | AI Action: Continue Driving</p>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# PORTAL 2: PASSENGER APPLICATION
# ==============================================================================
elif user_role == "Passenger Application":
    
    st.markdown('<img src="https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=2000&q=80" style="width:100%; height:160px; object-fit:cover; border-radius:20px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Consumer Ticket & Tracking Portal</h1>", unsafe_allow_html=True)

    try:
        passenger_states = list(RAILWAY_NETWORK.keys())
        default_state_idx = passenger_states.index("Tamil Nadu") if "Tamil Nadu" in passenger_states else 0
        
        with st.expander("Configure Travel Itinerary", expanded=True):
            c_org, c_dest = st.columns(2)
            with c_org:
                org_st = st.selectbox("Origin State", passenger_states, index=default_state_idx)
                
                org_city_list = list(RAILWAY_NETWORK[org_st].keys())
                org_cy = st.selectbox("Origin City", org_city_list, index=0)
                if org_cy not in RAILWAY_NETWORK[org_st]: org_cy = org_city_list[0]
                    
                org_stn_list = list(RAILWAY_NETWORK[org_st][org_cy]["stations"].keys())
                org_sn = st.selectbox("Boarding Station", org_stn_list, index=0)
                if org_sn not in org_stn_list: org_sn = org_stn_list[0]
                    
            with c_dest:
                dst_st = st.selectbox("Destination State", passenger_states, index=3 if len(passenger_states) > 3 else 0) 
                
                dst_city_list = list(RAILWAY_NETWORK[dst_st].keys())
                dst_cy = st.selectbox("Destination City", dst_city_list, index=0)
                if dst_cy not in RAILWAY_NETWORK[dst_st]: dst_cy = dst_city_list[0]
                    
                dst_stn_list = list(RAILWAY_NETWORK[dst_st][dst_cy]["stations"].keys())
                dst_sn = st.selectbox("Destination Station", dst_stn_list, index=max(0, len(dst_stn_list)-1))
                if dst_sn not in dst_stn_list: dst_sn = dst_stn_list[-1]
                
        # 24-Hour Time Math
        sched_min = 855 # 14:15 Hrs
        delay_min = np.random.choice([0, 0, 15, 30])
        exp_min = sched_min + delay_min
        
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        if delay_min == 0:
            with m1: st.markdown(f"<div class='premium-card'><div class='card-title'>Train Status</div><div class='card-value' style='color:#10B981'>On Time</div><div class='card-subtitle' style='color:#64748B'>No Network Delays</div></div>", unsafe_allow_html=True)
        else:
            with m1: st.markdown(f"<div class='premium-card'><div class='card-title'>Train Status</div><div class='card-value' style='color:#EF4444'>Delayed</div><div class='card-subtitle' style='color:#64748B'>AI Adjusted Arrival</div></div>", unsafe_allow_html=True)
            
        with m2: st.markdown(f"<div class='premium-card'><div class='card-title'>Printed Ticket Time</div><div class='card-value'>{format_24h(sched_min)}</div><div class='card-subtitle' style='color:#64748B'>Original Booking</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='premium-card'><div class='card-title'>Live Expected Arrival</div><div class='card-value' style='color:#2563EB'>{format_24h(exp_min)}</div><div class='card-subtitle' style='color:#64748B'>Arriving at Platform 4</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='premium-card'><div class='card-title'>Passenger Crowding</div><div class='card-value' style='color:#F59E0B'>Moderate</div><div class='card-subtitle' style='color:#64748B'>68% Train Capacity</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        tabs_p = st.tabs(["Live Journey Map", "Station Tracker", "Seat & Bed Layout", "Train Services"])
        p_map = tabs_p[0]; p_track = tabs_p[1]; p_coach = tabs_p[2]; p_services = tabs_p[3]

        with p_map:
            try:
                p1 = RAILWAY_NETWORK[org_st][org_cy]["coords"][org_sn]
                p2 = RAILWAY_NETWORK[dst_st][dst_cy]["coords"][dst_sn]
                
                lats, lons = [], []
                for t in np.linspace(0, 1, 30):
                    lat = p1[0] * (1 - t) + p2[0] * t
                    lon = p1[1] * (1 - t) + p2[1] * t
                    offset = np.sin(t * np.pi) * 0.8
                    lats.append(lat + offset)
                    lons.append(lon + (offset * 0.3))
                    
                live_pos = int(len(lats) * 0.6) 
                
                fig_pmap = go.Figure()
                fig_pmap.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="lines", line=dict(width=6, color="#2563EB"), name="Your Travel Route"))
                fig_pmap.add_trace(go.Scattermapbox(lat=[p1[0], p2[0]], lon=[p1[1], p2[1]], mode="markers+text", marker=dict(size=16, color="#0F172A"), text=[f"<b>{org_sn}</b>", f"<b>{dst_sn}</b>"], textposition="bottom center", textfont=dict(size=12, family="Inter", color="#0F172A"), name="Stations"))
                
                fig_pmap.add_trace(go.Scattermapbox(lat=[lats[live_pos]], lon=[lons[live_pos]], mode="markers+text", marker=dict(size=24, color="#10B981"), text=["<b>YOUR TRAIN IS HERE</b>"], textposition="top right", textfont=dict(size=13, family="Inter", color="#10B981", weight="bold"), name="Live Train"))

                center_lat = (p1[0] + p2[0]) / 2
                center_lon = (p1[1] + p2[1]) / 2
                fig_pmap.update_layout(dragmode=False, mapbox=dict(style="carto-positron", zoom=5.5, center=dict(lat=center_lat, lon=center_lon)), margin=dict(l=0, r=0, t=0, b=0), height=450)
                st.plotly_chart(fig_pmap, use_container_width=True, config=PLOT_CONFIG)
            except Exception as e:
                st.error(f"Map Rendering Error: {e}")

        with p_track:
            st.progress(60)
            st.dataframe(pd.DataFrame({
                "Station Stop": [org_sn, "Midpoint Crossing", dst_sn],
                "Scheduled Time (24H)": ["10:00 Hrs", "12:00 Hrs", format_24h(sched_min)],
                "Live Expected Time (24H)": ["10:00 Hrs", "12:05 Hrs", format_24h(exp_min)],
                "Status": ["Already Passed", "Arriving Soon", "Waiting"]
            }), use_container_width=True, hide_index=True)

        with p_coach:
            c1, c2 = st.columns([1, 2])
            with c1:
                my_seat = st.number_input("Find Your Seat Number (1-24):", 1, 24, 12)
            with c2:
                for bay in range(1, 4):
                    s = (bay - 1) * 8
                    b1, b2, b3, sp, b4 = st.columns([1,1,1,0.5,1])
                    b1.button(f"Lower ({s+1})", key=f"s{s+1}", disabled=(s+1==my_seat))
                    b2.button(f"Middle ({s+2})", key=f"s{s+2}", disabled=(s+2==my_seat))
                    b3.button(f"Upper ({s+3})", key=f"s{s+3}", disabled=(s+3==my_seat))
                    sp.write("||")
                    b4.button(f"Side ({s+7})", key=f"s{s+7}", disabled=(s+7==my_seat))

        with p_services:
            f1, f2, f3, f4 = st.columns(4)
            with f1: st.markdown("<div class='premium-card'><h4>Food Services</h4><p style='color:#10B981; font-weight:800;'><span style='color:#10B981;'>●</span> Open Now</p></div>", unsafe_allow_html=True)
            with f2: st.markdown("<div class='premium-card'><h4>Train WiFi</h4><p style='color:#10B981; font-weight:800;'><span style='color:#10B981;'>●</span> 15 Mbps Fast</p></div>", unsafe_allow_html=True)
            with f3: st.markdown("<div class='premium-card'><h4>Air Conditioning</h4><p style='color:#10B981; font-weight:800;'><span style='color:#10B981;'>●</span> Perfect Temp</p></div>", unsafe_allow_html=True)
            with f4: st.markdown("<div class='premium-card'><h4>Emergency Help</h4><p style='color:#EF4444; font-weight:800;'><span style='color:#EF4444;'>●</span> Dial 139</p></div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Render Fault: {e}")
