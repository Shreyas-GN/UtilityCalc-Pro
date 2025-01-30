import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime, timedelta

def load_tasks():
    if os.path.exists('tasks_history.json'):
        with open('tasks_history.json', 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open('tasks_history.json', 'w') as f:
        json.dump(tasks, f)

def estimate_time(complexity, task_type, experience_level):
    # Base time in hours for different complexity levels
    base_times = {
        "Low": 1,
        "Medium": 3,
        "High": 8,
        "Very High": 16
    }
    
    # Multipliers for different task types
    type_multipliers = {
        "Development": 1.0,
        "Design": 0.8,
        "Documentation": 0.6,
        "Testing": 0.7,
        "Research": 1.2,
        "Planning": 0.5
    }
    
    # Experience level adjustments
    experience_multipliers = {
        "Beginner": 1.5,
        "Intermediate": 1.0,
        "Expert": 0.7
    }
    
    base_time = base_times[complexity]
    type_mult = type_multipliers[task_type]
    exp_mult = experience_multipliers[experience_level]
    
    estimated_time = base_time * type_mult * exp_mult
    
    # Add some variance (±20%)
    min_time = estimated_time * 0.8
    max_time = estimated_time * 1.2
    
    return min_time, estimated_time, max_time

def main():
    st.set_page_config(page_title="Task Time Estimator", page_icon="⏱️", layout="wide")
    
    st.title("⏱️ AI-Based Task Time Estimator")
    st.write("Estimate task completion time based on complexity and other factors")
    
    # Initialize session state
    if 'tasks' not in st.session_state:
        st.session_state.tasks = load_tasks()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Estimate Task", "Task History", "Analysis"])
    
    # Estimate Task Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name")
            task_description = st.text_area("Task Description")
            complexity = st.select_slider(
                "Task Complexity",
                options=["Low", "Medium", "High", "Very High"],
                value="Medium"
            )
            task_type = st.selectbox(
                "Task Type",
                ["Development", "Design", "Documentation", "Testing", "Research", "Planning"]
            )
            experience_level = st.select_slider(
                "Experience Level",
                options=["Beginner", "Intermediate", "Expert"],
                value="Intermediate"
            )
            
            if st.button("Estimate Time"):
                min_time, estimated_time, max_time = estimate_time(
                    complexity, task_type, experience_level
                )
                
                with col2:
                    st.markdown("### 📊 Time Estimate")
                    st.info(f"Estimated Time: {estimated_time:.1f} hours")
                    st.success(f"Optimistic Estimate: {min_time:.1f} hours")
                    st.warning(f"Conservative Estimate: {max_time:.1f} hours")
                    
                    # Create timeline visualization
                    fig = go.Figure()
                    
                    # Add range bar
                    fig.add_trace(go.Bar(
                        x=[estimated_time],
                        y=['Estimated'],
                        orientation='h',
                        name='Estimated Time',
                        error_x=dict(
                            type='data',
                            symmetric=False,
                            array=[max_time - estimated_time],
                            arrayminus=[estimated_time - min_time]
                        )
                    ))
                    
                    fig.update_layout(
                        title="Time Estimate Range",
                        xaxis_title="Hours",
                        showlegend=False
                    )
                    st.plotly_chart(fig)
                    
                    # Save task
                    if st.button("Save Estimate"):
                        task = {
                            "name": task_name,
                            "description": task_description,
                            "complexity": complexity,
                            "type": task_type,
                            "experience_level": experience_level,
                            "estimated_time": estimated_time,
                            "min_time": min_time,
                            "max_time": max_time,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.tasks.append(task)
                        save_tasks(st.session_state.tasks)
                        st.success("Task estimate saved!")
    
    # Task History Tab
    with tab2:
        if st.session_state.tasks:
            df = pd.DataFrame(st.session_state.tasks)
            st.dataframe(
                df.style.format({
                    'estimated_time': '{:.1f} hrs',
                    'min_time': '{:.1f} hrs',
                    'max_time': '{:.1f} hrs'
                })
            )
        else:
            st.write("No task history available.")
    
    # Analysis Tab
    with tab3:
        if st.session_state.tasks:
            df = pd.DataFrame(st.session_state.tasks)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Average time by complexity
                avg_by_complexity = df.groupby('complexity')['estimated_time'].mean()
                fig1 = go.Figure(data=[go.Bar(
                    x=avg_by_complexity.index,
                    y=avg_by_complexity.values,
                    text=avg_by_complexity.values.round(1),
                    textposition='auto'
                )])
                fig1.update_layout(
                    title="Average Time by Complexity",
                    yaxis_title="Hours"
                )
                st.plotly_chart(fig1)
            
            with col2:
                # Average time by task type
                avg_by_type = df.groupby('type')['estimated_time'].mean()
                fig2 = go.Figure(data=[go.Bar(
                    x=avg_by_type.index,
                    y=avg_by_type.values,
                    text=avg_by_type.values.round(1),
                    textposition='auto'
                )])
                fig2.update_layout(
                    title="Average Time by Task Type",
                    yaxis_title="Hours"
                )
                st.plotly_chart(fig2)
            
            # Insights
            st.markdown("### 💡 Task Insights")
            total_tasks = len(df)
            total_hours = df['estimated_time'].sum()
            avg_task_time = df['estimated_time'].mean()
            
            st.info(f"Total Tasks: {total_tasks}")
            st.success(f"Total Estimated Hours: {total_hours:.1f}")
            st.warning(f"Average Task Time: {avg_task_time:.1f} hours")
            
            # Most common task type
            most_common_type = df['type'].mode()[0]
            st.write(f"Most common task type: {most_common_type}")
            
            # Time distribution
            st.markdown("### ⏰ Time Distribution")
            fig3 = go.Figure(data=[go.Pie(
                labels=df['type'],
                values=df['estimated_time'],
                hole=.3
            )])
            fig3.update_layout(title="Time Distribution by Task Type")
            st.plotly_chart(fig3)
        else:
            st.write("Add some tasks to see the analysis!")

if __name__ == "__main__":
    main()
