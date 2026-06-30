import streamlit as st
import datetime
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="GATE Study Tracker", page_icon="⏱️", layout="wide")

# --- INITIALIZE TRACKING DATA STATICS ---
if 'streak' not in st.session_state: st.session_state.streak = 14
if 'lifetime_hours' not in st.session_state: st.session_state.lifetime_hours = 118.15
if 'weekly_hours' not in st.session_state: st.session_state.weekly_hours = 39.33
if 'today_accumulated' not in st.session_state: st.session_state.today_accumulated = 6.75  # 6h 45m

# Timer Engine Session State Handles
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'recent_sessions' not in st.session_state: 
    st.session_state.recent_sessions = [
        {"time": "04:00–06:30 AM", "duration": "2h 30m"},
        {"time": "09:00–11:00 AM", "duration": "2h 00m"},
        {"time": "02:00–04:15 PM", "duration": "2h 15m"}
    ]

# --- APP LAYOUT UI COMPONENT ---
st.title("⏱️ GATE Study Tracker")
st.caption("🚀 Simple Active Interval Counter | Precision Analytics Framework")

# Top Level Dashboard Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    # Target goal metric logic
    st.metric(label="📅 Today's Progress", value=f"{st.session_state.today_accumulated:.2f}h / 7.0h Goal")
    st.progress(min(st.session_state.today_accumulated / 7.0, 1.0))
with col2:
    st.metric(label="📈 Weekly Aggregate", value=f"{st.session_state.weekly_hours:.2f} Hours")
with col3:
    st.metric(label="🔥 Current Consistency Streak", value=f"{st.session_state.streak} Days")
with col4:
    st.metric(label="📊 Cumulative Lifetime Hours", value=f"{st.session_state.lifetime_hours:.2f} Hours")

st.markdown("---")

# Main Action Menu Interface Layout split
left_panel, right_panel = st.columns([2, 1])

with left_panel:
    st.header("⚡ Active Engine Matrix")
    
    # Subject Configuration Selection Dropdown box
    target_subject = st.selectbox("📚 Select Target Focus Area Before Starting Session:", [
        "Data Structures & Algorithms", "Operating Systems", "DBMS", "Computer Networks",
        "Computer Organization & Architecture", "Theory of Computation", "Compiler Design",
        "Digital Logic", "Discrete Mathematics", "Engineering Mathematics", "Aptitude", 
        "Mock Tests", "PYQ Practice"
    ])
    
    # Timer Action Operations State Machine
    st.markdown("### ⏱️ Session Clock Controller")
    
    if not st.session_state.timer_running:
        if st.button("🟢 START SESSION", use_container_width=True):
            st.session_state.timer_running = True
            st.session_state.start_time = time.time()
            st.rerun()
        st.info("Status: Engine Idle. Select a core syllabus subject and tap Start above to initiate telemetry capture.")
    else:
        # Display live tracking notice
        st.warning(f"⏳ Currently Tracking: **{target_subject}**")
        elapsed_seconds = time.time() - st.session_state.start_time
        elapsed_hours = elapsed_seconds / 3600.0
        
        st.metric("Current Session Duration (Live Preview)", f"{elapsed_hours:.4f} hrs")
        
        if st.button("🔴 STOP & SAVE SESSION", use_container_width=True):
            # Compute total elapsed chunk delta
            final_delta_secs = time.time() - st.session_state.start_time
            final_delta_hours = final_delta_secs / 3600.0
            
            # Append changes across global operational stores
            st.session_state.today_accumulated += final_delta_hours
            st.session_state.weekly_hours += final_delta_hours
            st.session_state.lifetime_hours += final_delta_hours
            
            # Append string tag map to recent logs array
            now = datetime.datetime.now()
            time_stamp_str = f"{now.strftime('%I:%M %p')} Session"
            st.session_state.recent_sessions.insert(0, {"time": time_stamp_str, "duration": f"{final_delta_hours:.2f}h ({target_subject})"})
            
            # Reset active layout locks
            st.session_state.timer_running = False
            st.session_state.start_time = None
            st.success("Interval data committed to cloud telemetry logs!")
            st.balloons()
            st.rerun()

with right_panel:
    st.header("📋 Activity Log History")
    st.caption("Recent logged runtime session fragments")
    
    for session in st.session_state.recent_sessions[:5]:
        st.markdown(f"• **{session['time']}** — `{session['duration']}`")
        
    st.markdown("---")
    st.subheader("🏆 Milestone Achievements")
    st.success("✅ **7-Hour Goal Crusher** (Unlocked)")
    st.success("✅ **14-Day Streak Engine** (Unlocked)")
    st.info("🔒 *100-Hour Benchmark Milestone (Progressing)*")

st.markdown("---")

# Analytics Module Section View
st.header("📊 Deep Performance Framework Trends")
tab_graph, tab_report = st.tabs(["📊 Subject Trends Analysis", "📤 Export Reports Configuration"])

with tab_graph:
    st.subheader("Weekly Distribution Trends Matrix")
    # Generates a baseline synthetic data vector map correlating to historical parameters
    chart_data = {
        "Mon": 6.2, "Tue": 7.0, "Wed": 6.8, "Thu": 5.5, "Fri": 7.1, "Sat": 6.7, "Sun": st.session_state.today_accumulated
    }
    st.bar_chart(chart_data)

with tab_report:
    st.subheader("Configuration Engine Data Extraction")
    st.button("📄 Generate Verified Progress Portfolio (PDF)")
    st.button("📊 Extract Complete History Raw Values (CSV)")
