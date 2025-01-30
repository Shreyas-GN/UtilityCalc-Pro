import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json
import os

def load_sleep_data():
    if os.path.exists('sleep_data.json'):
        with open('sleep_data.json', 'r') as f:
            return json.load(f)
    return []

def save_sleep_data(data):
    with open('sleep_data.json', 'w') as f:
        json.dump(data, f)

def calculate_sleep_debt(sleep_hours, recommended_hours=8):
    return max(0, recommended_hours - sleep_hours)

def calculate_recovery_plan(total_debt, max_extra_sleep=2):
    days_needed = total_debt / max_extra_sleep
    return round(days_needed)

def main():
    st.set_page_config(page_title="Sleep Debt Calculator", page_icon="😴", layout="wide")
    
    st.title("😴 Sleep Debt & Recovery Calculator")
    st.write("Track your sleep patterns and get personalized recovery plans")
    
    # Initialize session state
    if 'sleep_data' not in st.session_state:
        st.session_state.sleep_data = load_sleep_data()
    
    tab1, tab2, tab3 = st.tabs(["Track Sleep", "Sleep Analysis", "Recovery Plan"])
    
    # Track Sleep Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date")
            sleep_time = st.time_input("Sleep Time", value=datetime.strptime("22:00", "%H:%M"))
            wake_time = st.time_input("Wake Time", value=datetime.strptime("06:00", "%H:%M"))
            sleep_quality = st.select_slider(
                "Sleep Quality",
                options=["Poor", "Fair", "Good", "Excellent"],
                value="Good"
            )
            
            if st.button("Add Sleep Record"):
                # Calculate sleep duration
                sleep_datetime = datetime.combine(date, sleep_time)
                wake_datetime = datetime.combine(date + timedelta(days=1), wake_time)
                if wake_datetime < sleep_datetime:
                    wake_datetime += timedelta(days=1)
                
                duration = (wake_datetime - sleep_datetime).total_seconds() / 3600
                
                sleep_record = {
                    "date": date.strftime("%Y-%m-%d"),
                    "sleep_time": sleep_time.strftime("%H:%M"),
                    "wake_time": wake_time.strftime("%H:%M"),
                    "duration": duration,
                    "quality": sleep_quality
                }
                
                st.session_state.sleep_data.append(sleep_record)
                save_sleep_data(st.session_state.sleep_data)
                st.success("Sleep record added!")
    
    # Sleep Analysis Tab
    with tab2:
        if st.session_state.sleep_data:
            df = pd.DataFrame(st.session_state.sleep_data)
            df['date'] = pd.to_datetime(df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Sleep duration trend
                fig1 = px.line(df, x='date', y='duration',
                             title='Sleep Duration Trend')
                fig1.add_hline(y=8, line_dash="dash", 
                             annotation_text="Recommended")
                st.plotly_chart(fig1)
                
                # Calculate statistics
                avg_duration = df['duration'].mean()
                total_debt = sum([calculate_sleep_debt(hrs) for hrs in df['duration']])
                quality_counts = df['quality'].value_counts()
                
                st.markdown("### 📊 Sleep Statistics")
                st.info(f"Average Sleep Duration: {avg_duration:.1f} hours")
                st.warning(f"Total Sleep Debt: {total_debt:.1f} hours")
                
                # Quality distribution
                fig2 = go.Figure(data=[go.Pie(
                    labels=quality_counts.index,
                    values=quality_counts.values,
                    hole=.3
                )])
                fig2.update_layout(title="Sleep Quality Distribution")
                st.plotly_chart(fig2)
            
            with col2:
                # Sleep timing pattern
                st.markdown("### ⏰ Sleep Timing Pattern")
                df['sleep_hour'] = pd.to_datetime(df['sleep_time']).dt.hour
                df['wake_hour'] = pd.to_datetime(df['wake_time']).dt.hour
                
                avg_sleep_hour = df['sleep_hour'].mean()
                avg_wake_hour = df['wake_hour'].mean()
                
                # Create 24-hour clock visualization
                hours = list(range(24))
                values = [1 if h >= avg_sleep_hour or h <= avg_wake_hour else 0 
                         for h in hours]
                
                fig3 = go.Figure(data=[go.Barpolar(
                    r=values,
                    theta=hours,
                    width=ones,
                    marker_color=["#1f77b4" if v else "#lightgray" for v in values]
                )])
                fig3.update_layout(
                    title="Average Sleep-Wake Pattern",
                    polar=dict(
                        radialaxis=dict(visible=False, range=[0, 1]),
                        angularaxis=dict(
                            ticktext=[f"{h:02d}:00" for h in hours],
                            tickvals=hours,
                            direction="clockwise"
                        )
                    )
                )
                st.plotly_chart(fig3)
                
                # Sleep consistency
                sleep_std = df['duration'].std()
                st.info(f"Sleep Consistency (lower is better): {sleep_std:.1f} hours")
        else:
            st.write("Add some sleep records to see the analysis!")
    
    # Recovery Plan Tab
    with tab3:
        st.markdown("### 🎯 Sleep Recovery Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_sleep = st.number_input("Target Sleep Hours", min_value=6.0, max_value=10.0, value=8.0)
            max_extra_sleep = st.number_input("Maximum Extra Sleep per Day", min_value=0.5, max_value=4.0, value=2.0)
            
            if st.session_state.sleep_data:
                df = pd.DataFrame(st.session_state.sleep_data)
                recent_avg = df['duration'].tail(7).mean()
                total_debt = sum([calculate_sleep_debt(hrs, target_sleep) 
                                for hrs in df['duration'].tail(7)])
                
                days_needed = calculate_recovery_plan(total_debt, max_extra_sleep)
                
                with col2:
                    st.markdown("### 📋 Recovery Summary")
                    st.info(f"Recent Average Sleep: {recent_avg:.1f} hours")
                    st.warning(f"Current Sleep Debt: {total_debt:.1f} hours")
                    
                    if total_debt > 0:
                        st.error(f"Days needed for recovery: {days_needed} days")
                        
                        # Create recovery schedule
                        schedule = []
                        remaining_debt = total_debt
                        for day in range(days_needed):
                            extra_sleep = min(max_extra_sleep, remaining_debt)
                            schedule.append({
                                'Day': day + 1,
                                'Extra Sleep Needed': extra_sleep,
                                'Total Sleep Target': target_sleep + extra_sleep
                            })
                            remaining_debt -= extra_sleep
                        
                        schedule_df = pd.DataFrame(schedule)
                        st.dataframe(schedule_df.style.format({
                            'Extra Sleep Needed': '{:.1f} hrs',
                            'Total Sleep Target': '{:.1f} hrs'
                        }))
                    else:
                        st.success("No sleep debt to recover from!")
                
                # Tips based on sleep patterns
                st.markdown("### 💡 Personalized Sleep Tips")
                tips = [
                    "- Maintain a consistent sleep schedule, even on weekends",
                    f"- Aim to sleep by {df['sleep_time'].mode()[0]} and wake up by {df['wake_time'].mode()[0]}",
                    "- Create a relaxing bedtime routine"
                ]
                
                if recent_avg < 7:
                    tips.append("- Prioritize sleep by going to bed earlier")
                if df['quality'].value_counts().index[0] != "Excellent":
                    tips.append("- Improve sleep environment (temperature, darkness, noise)")
                
                st.write("\n".join(tips))
            else:
                st.write("Add some sleep records to get a personalized recovery plan!")

if __name__ == "__main__":
    main()
