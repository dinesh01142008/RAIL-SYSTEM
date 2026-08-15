import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CSS (BRIGHT, FAST, UNBRANDED, BLUR-FREE) ---
st.set_page_config(page_title="Future Rail System | SIH 2026", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    /* ERADICATE FRAMEWORK WATERMARKS */
    #MainMenu {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important;}
    
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    .css-18e3th9 { padding-top: 1rem; }
    
    /* BRIGHT, PROFESSIONAL SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    /* Sleek Sidebar Buttons */
    div[role="radiogroup"] { gap: 12px; }
    div[role="radiogroup"] > label {
        background: #FFFFFF;
        padding: 14px 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { 
        background: #FFFFFF; 
        transform: translateX(6px); 
        border-color: #3B82F6;
        box-shadow: 0 8px 15px rgba(59, 130, 246, 0.1); 
    }
    
    /* 3D Premium Cards (Hardware Accelerated to prevent blur) */
    .premium-card {
        background: #FFFFFF;
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
        transform: translateZ(0);
        -webkit-font-smoothing: antialiased;
        backface-visibility: hidden;
    }
    .premium-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.12); 
        border-left: 5px solid #10B981; 
    }
    
    /* Clean Workflow Nodes */
    .workflow-node {
        background: #FFFFFF;
        border-radius: 14px; padding: 22px; margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        border-left: 5px solid #CBD5E1;
        transition: all 0.3s ease;
        transform: translateZ(0);
        -webkit-font-smoothing: antialiased;
        backface-visibility: hidden;
    }
    .workflow-node:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 25px rgba(15, 23, 42, 0.06);
    }
    .node-active { border-left-color: #10B981; }
    .node-alert { border-left-color: #EF4444; animation: pulse-red 2s infinite; }
    .node-caution { border-left-color: #F59E0B; }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    
    /* Typography */
    .w-title { font-size: 16px; font-weight: 800; color: #0F172A; display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;}
    .w-subtitle { font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 1.5px;}
    .w-status { font-size: 11px; font-weight: 800; padding: 5px 12px; border-radius: 20px; text-transform: uppercase;}
    
    .card-title { color: #64748B; font-size: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 8px; }
    .card-value { color: #0F172A; font-size: 32px; font-weight: 900; line-height: 1.2; letter-spacing: -0.5px;}
    .card-subtitle { font-size: 13px; font-weight: 600; margin-top: 8px; }
    
    /* Clean Enterprise Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid #E2E8F0; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab"] { height: 45px; font-weight: 700; font-size: 15px; color: #94A3B8; background: transparent; border: none; letter-spacing: 0.5px;}
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; font-weight: 800; }
    
    /* Alert Cards */
    .modern-alert {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 5px solid #4F46E5; padding: 22px 28px; border-radius: 14px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.08); color: #1E293B;
        font-size: 14px; line-height: 1.6; margin-bottom: 25px; border: 1px solid #C7D2FE;
        transform: translateZ(0); -webkit-font-smoothing: antialiased; backface-visibility: hidden;
    }
    .modern-alert-red { 
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 5px solid #EF4444; border-color: #FECACA;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.08); 
    }
    .alert-title { font-weight: 900; font-size: 16px; color: #3730A3; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;}
    .alert-title-red { color: #991B1B; }
    
    /* Buttons */
    .stButton>button { border-radius: 10px; font-weight: 800; background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; border: none; padding: 12px 28px; transition: all 0.3s; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.2); }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 12px 25px rgba(37, 99, 235, 0.3); color: white; }
    
    /* Fast Loading DataFrames */
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #E2E8F0; }
    .login-container { max-width: 420px; margin: 80px auto; padding: 50px 40px; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.04); text-align: center; border: 1px solid #F1F5F9; border-top: 5px solid #2563EB;}
</style>
""", unsafe_allow_html=True)

PLOT_CONFIG = {'displayModeBar': False} 

# --- 2. SESSION STATE FOR DYNAMIC PAGE SWITCHING ---
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
    # Jumps to Dashboard automatically when a track failure is selected
    st.session_state.active_tab = "Live Traffic Dashboard"

# --- 3. NATIONAL DATABASE ---
RAILWAY_DATA = {
    "Tamil Nadu": {
        "Salem": {"Salem Jn": 0.0, "Magnesite Jn": 7.8, "Sankari Durg": 28.5, "Cauvery": 52.1, "Erode Jn": 64.2},
        "Chennai": {"Chennai Central": 0.0, "Basin Bridge": 2.5, "Perambur": 5.5, "Villivakkam": 9.2, "Avadi": 21.0},
        "Coimbatore": {"Coimbatore Jn": 0.0, "Podanur": 5.8, "Kinathukadavu": 19.5, "Pollachi": 40.2, "Palakkad": 55.0},
        "Madurai": {"Madurai Jn": 0.0, "Tiruparankundram": 7.1, "Tirumangalam": 17.4, "Virudhunagar": 43.5, "Satur": 70.2}
    },
    "Maharashtra": {
        "Mumbai": {"CSMT": 0.0, "Dadar": 9.0, "Kurla": 15.3, "Thane": 33.5, "Kalyan": 53.2},
        "Pune": {"Pune Jn": 0.0, "Shivajinagar": 2.5, "Khadki": 6.3, "Pimpri": 14.2, "Chinchwad": 16.5}
    },
    "Karnataka": {
        "Bengaluru": {"KSR Bengaluru": 0.0, "Bengaluru Cantt": 4.5, "KR Puram": 14.0, "Whitefield": 23.5, "Malur": 43.0},
        "Mysuru": {"Mysuru Jn": 0.0, "Shrirangapatna": 14.5, "Pandavapura": 19.2, "Mandya": 45.0, "Maddur": 64.1}
    },
    "Delhi NCR": {
        "New Delhi": {"New Delhi": 0.0, "Tilak Bridge": 2.5, "Anand Vihar": 12.0, "Sahibabad": 18.5, "Ghaziabad": 25.0}
    },
    "Kerala": {
        "Thiruvananthapuram": {"Trivandrum Central": 0.0, "Varkala": 40.5, "Kollam": 64.2, "Kayamkulam": 105.1, "Chengannur": 125.4},
        "Kochi": {"Ernakulam Jn": 0.0, "Aluva": 19.5, "Angamaly": 28.7, "Chalakudi": 44.1, "Thrissur": 74.0}
    },
    "Gujarat": {
        "Ahmedabad": {"Ahmedabad Jn": 0.0, "Maninagar": 3.2, "Vatva": 7.5, "Geratpur": 13.1, "Barejadi": 17.8},
        "Surat": {"Surat": 0.0, "Udhna": 4.1, "Bhestan": 9.5, "Sachin": 15.2, "Maroli": 21.8}
    }
}

CITY_GPS_BASE = {
    "Chennai": (13.08, 80.27), "Salem": (11.66, 78.14), "Coimbatore": (11.00, 76.96), "Madurai": (9.92, 78.11),
    "Mumbai": (18.94, 72.83), "Pune": (18.52, 73.85), "Bengaluru": (12.97, 77.59), "New Delhi": (28.61, 77.20),
    "Thiruvananthapuram": (8.52, 76.93), "Kochi": (9.93, 76.26), "Ahmedabad": (23.02, 72.57), "Surat": (21.17, 72.83)
}

def get_dynamic_gps(city_name, station_name):
    base_lat, base_lon = CITY_GPS_BASE.get(city_name, (21.0, 78.0))
    offset = (len(str(station_name)) * 0.015) - 0.05 
    return (base_lat + offset, base_lon + (offset * 1.2))

def get_curved_route(p1, p2, num_points=30):
    lats, lons = [], []
    for t in np.linspace(0, 1, num_points):
        lat = p1[0] * (1 - t) + p2[0] * t
        lon = p1[1] * (1 - t) + p2[1] * t
        offset = np.sin(t * np.pi) * 0.5 
        lats.append(lat + offset)
        lons.append(lon + (offset * 0.5))
    return lats, lons

def format_time(minutes):
    hours, mins = int(minutes // 60), int(minutes % 60)
    return f"{hours:02d}:{mins:02d} AM"

# --- 4. BRIGHT, INTERACTIVE SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 style="color:#0F172A; font-weight:900; letter-spacing:-0.5px; margin-bottom: -5px; margin-top: 10px;">FUTURE RAIL SYSTEM</h2>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; font-weight:800; color:#2563EB; margin-bottom:30px; letter-spacing: 0.5px;'>SIH 2026: SMART CONFLICT RESOLUTION</p>", unsafe_allow_html=True)
    user_role = st.radio("Access Portal", ["Passenger Application", "Central Command Center"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#E2E8F0;'>", unsafe_allow_html=True)

# ==============================================================================
# PORTAL 1: CENTRAL COMMAND CENTER (COA)
# ==============================================================================
if user_role == "Central Command Center":
    
    if not st.session_state.staff_authenticated:
        st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class='login-container'>
                <div style='color:#0F172A; font-weight:900; font-size:24px; margin-bottom: 8px;'>Authorized Access Only</div>
                <p style="color:#64748B; margin-bottom:30px; font-size:14px; font-weight:600;">Control Office Application (COA)</p>
            </div>
            """, unsafe_allow_html=True)
            st.text_input("Enter Clearance Password", type="password", key="pwd_input", label_visibility="collapsed")
            st.button("Authenticate Login", on_click=check_password, use_container_width=True)
            if st.session_state.auth_error: st.error("Access Denied. Incorrect Password.")
                
    else:
        staff_module = st.sidebar.radio("Control Modules", ["Live Traffic Dashboard", "Operational Hierarchy"], key="active_tab")
        st.sidebar.markdown("<hr style='border-color:#E2E8F0;'>", unsafe_allow_html=True)
        
        with st.sidebar:
            st.markdown("<h3 style='font-size:12px; color:#64748B; font-weight:800; letter-spacing:1px;'>NETWORK REGION</h3>", unsafe_allow_html=True)
            sel_state = st.selectbox("State", list(RAILWAY_DATA.keys()), index=0, label_visibility="collapsed")
            sel_city = st.selectbox("Division", list(RAILWAY_DATA[sel_state].keys()), index=0, label_visibility="collapsed")
            current_sector = RAILWAY_DATA[sel_state][sel_city]
            station_list = list(current_sector.keys())
            mid_station_idx = max(0, min(2, len(station_list)-1)) 
            
            st.markdown("<br><h3 style='font-size:12px; color:#64748B; font-weight:800; letter-spacing:1px;'>INCIDENT INJECTION</h3>", unsafe_allow_html=True)
            sel_station = st.selectbox("Select Station Limit", station_list, index=0)
            track_status = st.selectbox("Track Condition", ["Clear (Normal)", "Maintenance (Slow Speed)", "Blocked (Sensor Failure)"], on_change=trigger_ai_focus)
            
            st.markdown("<hr style='border-color:#E2E8F0;'>", unsafe_allow_html=True)
            ai_enabled = st.toggle("Enable AI Smart Resolution", value=True)

        def process_telemetry(damaged_stn, status, ai, sector_dict):
            try:
                vb_speed, exp_speed, fr_speed = 110, 85, 45
                trains = [
                    {"name": "Vande Bharat Express", "id": "VB-01", "type": "High-Speed", "speed": vb_speed, "start": 9.0, "weight": 2, "color": "#10B981"},
                    {"name": "Heavy Freight Train", "id": "FRT-09", "type": "Freight", "speed": fr_speed, "start": 8.8, "weight": 3, "color": "#F59E0B"},
                    {"name": "Superfast Express", "id": "SF-04", "type": "Express", "speed": exp_speed, "start": 9.3, "weight": 2, "color": "#3B82F6"}
                ]
                
                if ai: trains = sorted(trains, key=lambda x: x["weight"])
                    
                records = []
                for t in trains:
                    curr_time = t["start"] * 60
                    for stn, dist in sector_dict.items():
                        prev_dist = 0 if len(records) == 0 else records[-1]["Distance (km)"]
                        current_speed = t["speed"]
                        dwell = 2 
                        track = "Mainline"
                        node_condition = "Clear"

                        if stn == damaged_stn:
                            node_condition = status
                            if status == "Maintenance (Slow Speed)": 
                                current_speed = min(current_speed, 30)
                            elif status == "Blocked (Sensor Failure)":
                                if t["type"] == "Freight": dwell = 45 if not ai else 15
                                
                        mid_station = list(sector_dict.keys())[mid_station_idx] 
                        if ai and t["type"] == "Freight" and stn == mid_station:
                            dwell += 20
                            track = "Loop Line (Waiting)"
                        
                        if not ai and t["type"] != "Freight" and status == "Blocked (Sensor Failure)" and dist >= sector_dict.get(damaged_stn, 999):
                            curr_time += 45
                            
                        travel_time = ((dist - prev_dist) / current_speed) * 60 if dist > 0 else 0
                        arrival = curr_time + travel_time
                        departure = arrival + dwell
                        curr_time = departure 
                        
                        records.append({
                            "Train Name": t["name"], 
                            "Train ID": t["id"], 
                            "Station": stn, 
                            "Distance (km)": dist, 
                            "Expected Arrival": arrival, 
                            "Wait Time (Mins)": dwell, 
                            "Assigned Track": track, 
                            "Status": node_condition, 
                            "Color": t["color"]
                        })
                return pd.DataFrame(records)
            except Exception:
                return pd.DataFrame() 

        df_traffic = process_telemetry(sel_station, track_status, ai_enabled, current_sector)

        # ----------------------------------------------------------------------
        # TAB 1: LIVE TRAFFIC DASHBOARD
        # ----------------------------------------------------------------------
        if st.session_state.active_tab == "Live Traffic Dashboard":
            st.markdown('<img src="https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=2000&q=80" style="width:100%; height:140px; object-fit:cover; border-radius:20px; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
            col_t1, col_t2 = st.columns([5, 1])
            with col_t1: st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Live Traffic Dashboard (COA)</h1>", unsafe_allow_html=True)
            with col_t2: st.button("End Session", on_click=logout, type="secondary", use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            base_tph = 14 if "Block" in track_status else (18 if "Maintenance" in track_status else 24)
            ai_tph = base_tph + (8 if "Block" in track_status else 4) if ai_enabled else base_tph
            
            with c1: st.markdown(f"<div class='premium-card'><div class='card-title'>Active Trains</div><div class='card-value'>142</div><div class='card-subtitle' style='color:#64748B'>{sel_city} Region</div></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='premium-card'><div class='card-title'>Network Status</div><div class='card-value'>{'0' if ai_enabled else ('Alert' if track_status != 'Clear (Normal)' else '0')}</div><div class='card-subtitle' style='color:#10B981'>{'AI Auto-Resolved' if ai_enabled and track_status != 'Clear (Normal)' else 'Operations Safe'}</div></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='premium-card'><div class='card-title'>Section Capacity</div><div class='card-value'>{ai_tph}</div><div class='card-subtitle' style='color:#3B82F6'>Trains Per Hour</div></div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='premium-card'><div class='card-title'>Smart Resolution</div><div class='card-value'>{'ONLINE' if ai_enabled else 'OFFLINE'}</div><div class='card-subtitle' style='color:{'#10B981' if ai_enabled else '#EF4444'}'>{'Moving Block Active' if ai_enabled else 'Manual Block Rules'}</div></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if track_status != "Clear (Normal)":
                if ai_enabled:
                    st.markdown(f"""
                    <div class="modern-alert">
                        <div class="alert-title">SMART SYSTEM LOG: CONFLICT RESOLVED</div>
                        <strong>Anomaly Detected:</strong> Track status changed to '{track_status}' at {sel_station}.<br>
                        <strong>AI Resolution:</strong> The Central Engine dynamically updated safe following distances.<br>
                        <strong>Action Executed:</strong> Heavy Freight Train safely re-routed to wait on the Loop Line.<br>
                        <strong>Outcome:</strong> Collision avoided. Mainline secured for Vande Bharat Express.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="modern-alert modern-alert-red">
                        <div class="alert-title alert-title-red">SYSTEM WARNING: AI ENGINE OFFLINE</div>
                        <strong>Anomaly Detected:</strong> Track status changed to '{track_status}' at {sel_station}.<br>
                        <strong>Fallback Protocol:</strong> Reverting to manual block system procedures.<br>
                        <strong>Outcome:</strong> Heavy traffic bottleneck. Trains holding at red signals. Network capacity reduced.
                    </div>
                    """, unsafe_allow_html=True)

            tabs = st.tabs(["Live Train Schedule", "Network GPS Map", "Position Tracker", "Time & Distance Chart"])
            tab_schedule, tab_map, tab_radar, tab_graph = tabs[0], tabs[1], tabs[2], tabs[3]
            
            with tab_schedule:
                formatted_df = df_traffic.copy()
                formatted_df["Expected Arrival"] = formatted_df["Expected Arrival"].apply(format_time)
                formatted_df["Wait Time (Mins)"] = formatted_df["Wait Time (Mins)"].apply(lambda x: int(x))
                final_df = formatted_df[["Train Name", "Station", "Expected Arrival", "Wait Time (Mins)", "Assigned Track", "Status"]]
                st.dataframe(final_df, use_container_width=True, hide_index=True)
                st.markdown("<br>", unsafe_allow_html=True)

            with tab_map:
                st.markdown("#### Real-Time Network Geography")
                fig_net = go.Figure()
                track_lats, track_lons, stn_names = [], [], []
                
                for s_name in current_sector.keys():
                    lat, lon = get_dynamic_gps(sel_city, s_name)
                    track_lats.append(lat)
                    track_lons.append(lon)
                    stn_names.append(s_name)
                    
                fig_net.add_trace(go.Scattermapbox(
                    lat=track_lats, lon=track_lons, mode="lines+markers+text",
                    marker=dict(size=12, color="#0F172A"), line=dict(width=4, color="#94A3B8"),
                    text=stn_names, textposition="bottom center",
                    textfont=dict(size=12, color="#0F172A", family="Inter", weight="bold"), name="Stations"
                ))
                
                max_d = max(current_sector.values()) if current_sector else 100
                sim_time = st.session_state.get('sim_time_val', 580)
                
                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    times, dists = sub["Expected Arrival"].values, sub["Distance (km)"].values
                    if sim_time < times[0]: continue
                    curr_d = dists[-1] if sim_time > times[-1] else np.interp(sim_time, times, dists)
                    
                    pct = curr_d / max_d if max_d > 0 else 0
                    pct = max(0, min(1, pct))
                    t_lat = track_lats[0] + pct * (track_lats[-1] - track_lats[0])
                    t_lon = track_lons[0] + pct * (track_lons[-1] - track_lons[0])
                    c_val = sub["Color"].iloc[0]
                    
                    fig_net.add_trace(go.Scattermapbox(
                        lat=[t_lat], lon=[t_lon], mode="markers+text",
                        marker=dict(size=20, color=c_val), 
                        text=[f"<b>{t_name}</b>"], textposition="top right",
                        textfont=dict(size=13, color=c_val, family="Inter"), name=t_name
                    ))
                    
                if track_status != "Clear (Normal)":
                    dmg_lat, dmg_lon = get_dynamic_gps(sel_city, sel_station)
                    dmg_col = "#EF4444" if "Block" in track_status else "#F59E0B"
                    fig_net.add_trace(go.Scattermapbox(
                        lat=[dmg_lat], lon=[dmg_lon], mode="markers+text",
                        marker=dict(size=30, color=dmg_col, opacity=0.6),
                        text=[track_status.upper()], textposition="top left",
                        textfont=dict(size=12, color=dmg_col, family="Inter", weight="bold"), name="Incident"
                    ))

                fig_net.update_layout(
                    mapbox=dict(style="carto-positron", zoom=7.5, center=dict(lat=np.mean(track_lats), lon=np.mean(track_lons))),
                    margin=dict(l=0, r=0, t=0, b=0), height=450, showlegend=False
                )
                st.plotly_chart(fig_net, use_container_width=True, config=PLOT_CONFIG)

            with tab_radar:
                sim_time = st.slider("Time Scrub", min_value=500, max_value=720, value=580, step=2, label_visibility="collapsed", key="sim_time_val")
                fig_radar = go.Figure()
                max_dist = max(current_sector.values()) if len(current_sector) > 0 else 100
                mid_dist = list(current_sector.values())[mid_station_idx]
                
                fig_radar.add_hline(y=1, line_dash="solid", line_color="#E2E8F0", line_width=6)
                fig_radar.add_shape(type="line", x0=mid_dist-2, y0=1, x1=mid_dist, y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                fig_radar.add_shape(type="line", x0=mid_dist, y0=1.5, x1=mid_dist+(max_dist*0.05), y1=1.5, line=dict(color="#E2E8F0", width=6)) 
                fig_radar.add_shape(type="line", x0=mid_dist+(max_dist*0.05), y0=1.5, x1=mid_dist+(max_dist*0.08), y1=1, line=dict(color="#E2E8F0", width=6)) 
                
                if track_status != "Clear (Normal)":
                    dmg_dist = current_sector.get(sel_station, 0)
                    dmg_color = "#EF4444" if "Block" in track_status else "#F59E0B"
                    fig_radar.add_shape(type="rect", x0=dmg_dist-1.5, y0=0.88, x1=dmg_dist+1.5, y1=1.12, fillcolor=dmg_color, opacity=0.9, line_width=0)
                    fig_radar.add_annotation(x=dmg_dist, y=0.72, text=f"<b>ALERT</b>", font=dict(color=dmg_color, size=11, family="Inter"), showarrow=False)

                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    times, dists = sub["Expected Arrival"].values, sub["Distance (km)"].values
                    if sim_time < times[0]: continue
                    current_dist = dists[-1] if sim_time > times[-1] else np.interp(sim_time, times, dists)
                    
                    y_pos = 1
                    if ai_enabled and t_name == "Heavy Freight Train" and mid_dist <= current_dist <= mid_dist+(max_dist*0.05): y_pos = 1.5 
                    
                    color_val = sub["Color"].iloc[0]
                    tag_val = sub["Train ID"].iloc[0]
                    
                    fig_radar.add_trace(go.Scatter(x=[current_dist], y=[y_pos], mode="markers+text", marker=dict(size=22, color=color_val, line=dict(width=3, color="white")), text=[tag_val], textposition="top center", textfont=dict(size=12, color=color_val, family="Inter", weight="bold"), name=t_name, hoverinfo="name"))

                for stn, d in current_sector.items():
                    fig_radar.add_vline(x=d, line_dash="dot", line_color="#CBD5E1", annotation_text=f"  {stn.split(' ')[0]}", annotation_position="top left", annotation_font=dict(size=11, color="#64748B", family="Inter"))

                fig_radar.update_layout(dragmode=False, yaxis=dict(showticklabels=False, range=[0.4, 2]), xaxis=dict(range=[-2, max_dist+(max_dist*0.1)], showgrid=False, zeroline=False), height=350, template="plotly_white", margin=dict(t=30, b=20), plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC")
                st.plotly_chart(fig_radar, use_container_width=True, config=PLOT_CONFIG)

            with tab_graph:
                fig_marey = go.Figure()
                for stn, d in current_sector.items():
                    fig_marey.add_hline(y=d, line_dash="dot", line_color="#E2E8F0", annotation_text=f" {stn.split(' ')[0]}", annotation_font=dict(color="#94A3B8", size=11))
                    
                for t_name in df_traffic["Train Name"].unique():
                    sub = df_traffic[df_traffic["Train Name"] == t_name]
                    color_val = sub["Color"].iloc[0]
                    
                    fig_marey.add_trace(go.Scatter(x=sub["Expected Arrival"], y=sub["Distance (km)"], mode="lines+markers", name=t_name, line=dict(color=color_val, width=4, shape="spline"), marker=dict(size=8, line=dict(width=2, color="white")), hovertemplate="<b>%{text}</b><br>Time: %{x:.1f} mins<br>Dist: %{y} km<extra></extra>", text=sub["Station"]))
                
                fig_marey.update_layout(dragmode=False, height=450, xaxis_title="Time Line (Minutes)", yaxis_title="Distance (km)", template="plotly_white", plot_bgcolor="#FFFFFF", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), font=dict(family="Inter"))
                st.plotly_chart(fig_marey, use_container_width=True, config=PLOT_CONFIG)
                
        # ----------------------------------------------------------------------
        # TAB 2: OPERATIONAL HIERARCHY
        # ----------------------------------------------------------------------
        elif st.session_state.active_tab == "Operational Hierarchy":
            st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Operational Command Flow</h1>", unsafe_allow_html=True)
            st.write("Visualizing how the Central Command App issues orders to field staff dynamically.")
            
            flow_state = "node-active"
            status_text = "System Normal"
            sm_action = "Digital signals cleared to GREEN."
            lp_action = "Cruising at max safe speed."
            status_color = "#10B981"
            
            if track_status == "Maintenance (Slow Speed)":
                flow_state = "node-caution"
                status_text = "Speed Restriction Issued"
                sm_action = "Signals automatically set to DOUBLE YELLOW."
                lp_action = "Speed dynamically reduced to 30 km/h."
                status_color = "#F59E0B"
            elif track_status == "Blocked (Sensor Failure)":
                flow_state = "node-alert"
                status_text = "Critical Reroute Order"
                sm_action = "Mainline locked. Loop Line track points activated."
                lp_action = "Auto-Brakes engaged. Routing to side track."
                status_color = "#EF4444"

            c_flow, c_dash = st.columns([1, 1.2])
            
            with c_flow:
                st.markdown("### Live Communications Flow")
                
                st.markdown(f"""
                <div style="padding: 10px;">
                    <div class="workflow-node node-active">
                        <div class="w-subtitle">Level 1 & 2 • Strategic</div>
                        <div class="w-title">Railway Board & Zonal GMs <span class="w-status" style="background:#D1FAE5; color:#065F46;">Online</span></div>
                        <span style="font-size: 13px; color: #64748B;">National policy and AI systems tracking active.</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -10px 0; font-size: 24px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Level 3 & 4 • Command</div>
                        <div class="w-title">Central Command (COA) <span class="w-status" style="background:{status_color}20; color:{status_color};">{status_text}</span></div>
                        <span style="font-size: 13px; color: #64748B;">Target Area: <strong style="color:#0F172A;">{sel_station}</strong>. Issuing digital directives.</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -10px 0; font-size: 24px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Level 5 • Execution</div>
                        <div class="w-title">Station Master <span class="w-status" style="background:#F1F5F9; color:#334155;">Executing</span></div>
                        <span style="font-size: 13px; color: #64748B;">{sm_action}</span>
                    </div>
                    <div style="text-align: center; color: #CBD5E1; margin: -10px 0; font-size: 24px;">⬇</div>
                    <div class="workflow-node {flow_state}">
                        <div class="w-subtitle">Level 6 & 7 • Train Control</div>
                        <div class="w-title">Loco Pilots & Engineers <span class="w-status" style="background:#F1F5F9; color:#334155;">Responding</span></div>
                        <span style="font-size: 13px; color: #64748B;">{lp_action}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with c_dash:
                st.markdown("### AI Spacing Efficiency (Moving Block)")
                st.write("Mathematical validation proving how AI upgrades the network from slow, fixed limits to fast, dynamic spacing.")
                
                base_tph = 14 if "Block" in track_status else (18 if "Maintenance" in track_status else 24)
                ai_tph = base_tph + (8 if "Block" in track_status else 4) if ai_enabled else base_tph
                
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = ai_tph,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "<b>Trains Per Hour</b>", 'font': {'size': 16, 'color': '#64748B', 'family': 'Inter'}},
                    delta = {'reference': base_tph, 'increasing': {'color': "#10B981"}},
                    gauge = {
                        'axis': {'range': [None, 35], 'tickwidth': 2, 'tickcolor': "#E2E8F0"},
                        'bar': {'color': "#2563EB", 'thickness': 0.2},
                        'bgcolor': "#FFFFFF",
                        'borderwidth': 1,
                        'bordercolor': "#F1F5F9",
                        'steps': [
                            {'range': [0, 15], 'color': '#FEF2F2'},
                            {'range': [15, 24], 'color': '#FFFBEB'},
                            {'range': [24, 35], 'color': '#ECFDF5'}
                        ],
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=10), font=dict(family="Inter"))
                st.plotly_chart(fig_gauge, use_container_width=True, config=PLOT_CONFIG)
                
                st.markdown("#### System Capacity Comparison")
                df_compare = pd.DataFrame({
                    "System Architecture": ["Legacy Fixed System", "AI Dynamic System"],
                    "Trains Safely Allowed": [2, 6]
                })
                
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(
                    y=df_compare["System Architecture"],
                    x=df_compare["Trains Safely Allowed"],
                    orientation='h',
                    marker=dict(color=["#94A3B8", "#2563EB"]),  # FIXED: Removed borderradius to prevent error
                    text=["<b>2 Trains</b>", "<b>6 Trains</b>"],
                    textposition='inside',
                    insidetextanchor="middle",
                    textfont=dict(size=14, color="white", family="Inter"),
                    width=0.45
                ))
                fig_bar.update_layout(
                    height=180, margin=dict(l=0, r=0, t=10, b=0), 
                    xaxis=dict(title="Trains Safely Allowed in Sector", showgrid=True, gridcolor="#F1F5F9", title_font=dict(size=13, color="#94A3B8")),
                    yaxis=dict(title="", showgrid=False),
                    template="plotly_white", plot_bgcolor="#FFFFFF", 
                    font=dict(family="Inter", size=14, color="#0F172A", weight="bold")
                )
                st.plotly_chart(fig_bar, use_container_width=True, config=PLOT_CONFIG)

# ==============================================================================
# PORTAL 2: PASSENGER APPLICATION
# ==============================================================================
elif user_role == "Passenger Application":
    
    st.markdown('<img src="https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=2000&q=80" style="width:100%; height:180px; object-fit:cover; border-radius:20px; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:32px; color:#0F172A; font-weight:900; letter-spacing:-1px; margin-top:-10px;'>Journey Dashboard</h1>", unsafe_allow_html=True)

    passenger_states = list(RAILWAY_DATA.keys())
    default_state_idx = passenger_states.index("Tamil Nadu") if "Tamil Nadu" in passenger_states else 0
    
    with st.expander("Configure Travel Route", expanded=True):
        c_org, c_dest = st.columns(2)
        with c_org:
            org_st = st.selectbox("Origin State", passenger_states, index=default_state_idx)
            city_list = list(RAILWAY_DATA[org_st].keys())
            default_city_idx = city_list.index("Salem") if "Salem" in city_list else 0
            org_cy = st.selectbox("Origin City", city_list, index=default_city_idx)
            org_sn = st.selectbox("Boarding Station", list(RAILWAY_DATA[org_st][org_cy].keys()), index=0)
        with c_dest:
            dst_st = st.selectbox("Destination State", passenger_states, index=3 if len(passenger_states) > 3 else 0) 
            dst_cy = st.selectbox("Destination City", list(RAILWAY_DATA[dst_st].keys()), index=0)
            dst_sn = st.selectbox("Destination Station", list(RAILWAY_DATA[dst_st][dst_cy].keys()), index=max(0, len(list(RAILWAY_DATA[dst_st][dst_cy].keys()))-1))
            
    expected_delay = np.random.choice([0, 0, 15, 30])
    sched_arrival = datetime.strptime("02:15 PM", "%I:%M %p")
    expected_arrival = sched_arrival + timedelta(minutes=int(expected_delay))
    
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    if expected_delay == 0:
        with m1: st.markdown(f"<div class='premium-card'><div class='card-title'>Live Status</div><div class='card-value' style='color:#10B981'>On Time</div><div class='card-subtitle' style='color:#64748B'>Smooth Operations</div></div>", unsafe_allow_html=True)
    else:
        with m1: st.markdown(f"<div class='premium-card'><div class='card-title'>Live Status</div><div class='card-value' style='color:#EF4444'>Delayed</div><div class='card-subtitle' style='color:#64748B'>Recalibrated ETA</div></div>", unsafe_allow_html=True)
        
    with m2: st.markdown(f"<div class='premium-card'><div class='card-title'>Scheduled</div><div class='card-value'>{sched_arrival.strftime('%I:%M %p')}</div><div class='card-subtitle' style='color:#64748B'>Original Time</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='premium-card'><div class='card-title'>Expected</div><div class='card-value' style='color:#2563EB'>{expected_arrival.strftime('%I:%M %p')}</div><div class='card-subtitle' style='color:#64748B'>Platform 4</div></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='premium-card'><div class='card-title'>Platform Crowd</div><div class='card-value' style='color:#F59E0B'>High</div><div class='card-subtitle' style='color:#64748B'>85% Capacity</div></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tabs_p = st.tabs(["Route Map", "Live Train Tracker", "Seat Layout", "Onboard Amenities"])
    p_map = tabs_p[0]; p_track = tabs_p[1]; p_coach = tabs_p[2]; p_services = tabs_p[3]

    with p_map:
        p1 = get_dynamic_gps(org_cy, org_sn)
        p2 = get_dynamic_gps(dst_cy, dst_sn)
        route_lats, route_lons = get_curved_route(p1, p2)
        live_pos = int(len(route_lats) * 0.6) 
        
        fig_pmap = go.Figure()
        fig_pmap.add_trace(go.Scattermapbox(lat=route_lats, lon=route_lons, mode="lines", line=dict(width=5, color="#2563EB"), name="Trajectory"))
        fig_pmap.add_trace(go.Scattermapbox(lat=[p1[0], p2[0]], lon=[p1[1], p2[1]], mode="markers+text", marker=dict(size=14, color="#0F172A"), text=["<b>ORIGIN</b>", "<b>DEST</b>"], textposition="bottom center", textfont=dict(size=11, family="Inter", color="#0F172A"), name="Nodes"))
        
        # FIXED: Removed 'line' property inside marker dict here!
        fig_pmap.add_trace(go.Scattermapbox(
            lat=[route_lats[live_pos]], lon=[route_lons[live_pos]], mode="markers+text", 
            marker=dict(size=22, color="#10B981"), 
            text=["<b>YOUR TRAIN</b>"], textposition="top right", textfont=dict(size=13, family="Inter", color="#10B981"), name="Train"
        ))

        fig_pmap.update_layout(dragmode=False, mapbox=dict(style="carto-positron", zoom=4.5, center=dict(lat=(p1[0]+p2[0])/2, lon=(p1[1]+p2[1])/2)), margin=dict(l=0, r=0, t=0, b=0), height=400)
        st.plotly_chart(fig_pmap, use_container_width=True, config=PLOT_CONFIG)

    with p_track:
        st.progress(60)
        st.dataframe(pd.DataFrame({
            "Station": [org_sn, "Intermediate Station", dst_sn],
            "Scheduled Time": ["10:00 AM", "12:00 PM", sched_arrival.strftime("%I:%M %p")],
            "Expected Arrival": ["10:00 AM", "12:05 PM", expected_arrival.strftime("%I:%M %p")],
            "Status": ["Passed", "Approaching", "Pending"]
        }), use_container_width=True, hide_index=True)

    with p_coach:
        c1, c2 = st.columns([1, 2])
        with c1:
            my_seat = st.number_input("Enter Seat Number (1-24):", 1, 24, 12)
        with c2:
            for bay in range(1, 4):
                s = (bay - 1) * 8
                b1, b2, b3, sp, b4 = st.columns([1,1,1,0.5,1])
                b1.button(f"LWR ({s+1})", key=f"s{s+1}", disabled=(s+1==my_seat))
                b2.button(f"MID ({s+2})", key=f"s{s+2}", disabled=(s+2==my_seat))
                b3.button(f"UPR ({s+3})", key=f"s{s+3}", disabled=(s+3==my_seat))
                sp.write("||")
                b4.button(f"SL ({s+7})", key=f"s{s+7}", disabled=(s+7==my_seat))

    with p_services:
        f1, f2, f3, f4 = st.columns(4)
        with f1: st.markdown("<div class='premium-card'><h4>Catering</h4><p style='color:#10B981; font-weight:800;'>Available</p></div>", unsafe_allow_html=True)
        with f2: st.markdown("<div class='premium-card'><h4>RailWire WiFi</h4><p style='color:#10B981; font-weight:800;'>15 Mbps Stable</p></div>", unsafe_allow_html=True)
        with f3: st.markdown("<div class='premium-card'><h4>Charging Ports</h4><p style='color:#10B981; font-weight:800;'>Working</p></div>", unsafe_allow_html=True)
        with f4: st.markdown("<div class='premium-card'><h4>Emergency</h4><p style='color:#EF4444; font-weight:800;'>Dial 139</p></div>", unsafe_allow_html=True)
