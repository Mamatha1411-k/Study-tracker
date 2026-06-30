import streamlit as st
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="GATE Study Tracker", page_icon="⏱️", layout="wide")

# --- INITIALIZE TRACKING DATA (CLEARED FOR JULY 1ST KICKOFF) ---
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'lifetime_hours' not in st.session_state: st.session_state.lifetime_hours = 0.00
if 'weekly_hours' not in st.session_state: st.session_state.weekly_hours = 0.00
if 'today_accumulated' not in st.session_state: st.session_state.today_accumulated = 0.00

# Timer Engine Session State Handles
if 'timer_running' not in st.session_state: st.session_state.timer_running = False
if 'start_clock_time' not in st.session_state: st.session_state.start_clock_time = None
if 'recent_sessions' not in st.session_state: st.session_state.recent_sessions = []

# --- APP LAYOUT UI COMPONENT ---
st.title("⏱️ GATE Study Tracker")
# Hardcoded to July 1, 2026 at your current clock time 00:54
st.caption("📅 Date: 1 July 2026 | ⏰ Current Sync Time: 00:54 (12:54 AM)")

# Top Level Dashboard Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
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
    
    target_subject = st.selectbox("📚 Select Target Focus Area Before Starting Session:", [
        "Data Structures & Algorithms", "Operating Systems", "DBMS", "Computer Networks",
        "Computer Organization & Architecture", "Theory of Computation", "Compiler Design",
        "Digital Logic", "Discrete Mathematics", "Engineering Mathematics", "Aptitude", 
        "Mock Tests", "PYQ Practice"
    ])
    
    st.markdown("### ⏱️ Session Clock Controller")
    
    if not st.session_state.timer_running:
        if st.button("🟢 START SESSION", use_container_width=True):
            st.session_state.timer_running = True
            st.session_state.start_clock_time = datetime.datetime.now()
            st.rerun()
        st.info("Status: Engine Idle. Select a core syllabus subject and tap Start above to initiate telemetry capture.")
    else:
        st.warning(f"⏳ Currently Tracking: **{target_subject}**")
        
        # Calculate real-time elapsed duration using exact timestamps
        now = datetime.datetime.now()
        duration_delta = now - st.session_state.start_clock_time
        elapsed_hours = duration_delta.total_seconds() / 3600.0
        
        start_str = st.session_state.start_clock_time.strftime("%I:%M:%S %p")
        st.info(f"⏰ Session started at your clock time: **{start_str}**")
        st.metric("Current Session Duration", f"{elapsed_hours:.2f} hrs")
        
        if st.button("🔴 STOP & SAVE SESSION", use_container_width=True):
            stop_clock_time = datetime.datetime.now()
            final_delta = stop_clock_time - st.session_state.start_clock_time
            final_delta_hours = final_delta.total_seconds() / 3600.0
            
            # Append changes across global operational stores
            st.session_state.today_accumulated += final_delta_hours
            st.session_state.weekly_hours += final_delta_hours
            st.session_state.lifetime_hours += final_delta_hours
            
            if st.session_state.streak == 0 and final_delta_hours > 0.05:
                st.session_state.streak = 1
            
            # Format time logs window
            time_stamp_str = f"{st.session_state.start_clock_time.strftime('%I:%M %p')}–{stop_clock_time.strftime('%I:%M %p')}"
            st.session_state.recent_sessions.insert(0, {"time": time_stamp_str, "duration": f"{final_delta_hours:.2f}h ({target_subject})"})
            
            # Reset active layout locks
            st.session_state.timer_running = False
            st.session_state.start_clock_time = None
            st.success("Interval data committed to cloud telemetry logs!")
            st.balloons()
            st.rerun()

with right_panel:
    st.header("📋 Activity Log History")
    st.caption("Recent logged runtime session fragments")
    
    if len(st.session_state.recent_sessions) == 0:
        st.info("No sessions recorded yet for today. Hit START to log your first session fragment!")
    else:
        for session in st.session_state.recent_sessions[:5]:
            st.markdown(f"• **{session['time']}** — `{session['duration']}`")
        
    st.markdown("---")
    st.subheader("🏆 Milestone Achievements")
    if st.session_state.today_accumulated >= 7.0:
        st.success("✅ **7-Hour Goal Crusher** (Unlocked!)")
    else:
        st.info("🔒 *7-Hour Goal Crusher (Reach 7 hrs today to unlock)*")

st.markdown("---")
st.subheader("Weekly Distribution Trends Matrix")
chart_data = {
    "Mon": 0.0, "Tue": 0.0, "Wed": st.session_state.today_accumulated, "Thu": 0.0, "Fri": 0.0, "Sat": 0.0, "Sun": 0.0
}
st.bar_chart(chart_data)
                
