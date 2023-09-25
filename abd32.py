# -*- coding: utf-8 -*-
"""Untitled57.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmDMMf4bG7TWp1h7aLIFDR6FTTd8F2bL
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Read the modified dataset into a DataFrame
df = pd.read_csv("diabetess.csv")

# Page title
st.title("Diabetes Data Visualization")

# Description
st.write("Diabetes is a chronic health condition characterized by elevated blood sugar levels. It can have serious health consequences if not managed properly. This interactive dashboard allows you to explore and visualize data related to diabetes, including risk factors and outcomes.")

# Display files and available disk space
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded file preview:")
    st.write(df.head())

# Interactive Widgets
st.sidebar.subheader("Interactive Options")

# Checkbox to toggle displaying the dataset
show_data = st.sidebar.checkbox("Show Data")
if show_data:
    st.write("Dataset:")
    st.write(df)

# Filter the data based on user inputs
st.sidebar.subheader("Filter Data")

# Age Range Slider
age_range = st.sidebar.slider("Select Age Range", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

# BMI Range Slider
bmi_range = st.sidebar.slider("Select BMI Range", float(df['BMI'].min()), float(df['BMI'].max()), (float(df['BMI'].min()), float(df['BMI'].max())))

# Glucose Level Range Slider
glucose_range = st.sidebar.slider("Select Glucose Level Range", float(df['Glucose'].min()), float(df['Glucose'].max()), (float(df['Glucose'].min()), float(df['Glucose'].max())))

# Checkbox to filter by Outcome
filter_outcome = st.sidebar.checkbox("Filter by Outcome (Diabetic/Non-Diabetic)")

# Gender Selectbox
selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + df['gender'].unique().tolist())

# Smoking Status Selectbox
selected_smoking_status = st.sidebar.selectbox("Select Smoking Status", ['All'] + df['smoking_status'].unique().tolist())

# Apply filters to the DataFrame
filtered_df = df[
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1]) &
    (df['BMI'] >= bmi_range[0]) & (df['BMI'] <= bmi_range[1]) &
    (df['Glucose'] >= glucose_range[0]) & (df['Glucose'] <= glucose_range[1])
]

if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

if selected_smoking_status != 'All':
    filtered_df = filtered_df[filtered_df['smoking_status'] == selected_smoking_status]

if filter_outcome:
    filtered_df = filtered_df[filtered_df['Outcome'] == 1]  # Filter for diabetic patients

# Display filtered data if desired
if show_data:
    st.subheader("Filtered Data")
    st.write(filtered_df)

# Visualizations
st.subheader("Age Distribution by Outcome (Histogram)")
fig_age_distribution = px.histogram(filtered_df, x='Age', color='Outcome', title='Age Distribution by Outcome')
st.plotly_chart(fig_age_distribution)

st.subheader("3D Scatter Plot showing relationship between Glucose, BMI, and Age")
fig_3d_scatter = px.scatter_3d(filtered_df, x='Glucose', y='BMI', z='Age', color='Outcome',
                                title='3D Scatter Plot showing relationship between Glucose, BMI, and Age')
st.plotly_chart(fig_3d_scatter)

st.subheader("BMI vs. Glucose Level with Age and Pregnancies Transformations vs Outcome")
fig_transformations = px.scatter(filtered_df, x='BMI', y='Glucose', color='Age', size='Pregnancies',
                 title='BMI vs. Glucose Level with Age and Pregnancies Transformations vs Outcome',
                 labels={'Glucose': 'Glucose Level', 'BMI': 'BMI'},
                 hover_name='Outcome')
st.plotly_chart(fig_transformations)

st.subheader("Animated Scatter Plot of Glucose Level vs. Diabetes Outcome with BMI in Animation")
# Sort the DataFrame by the "BMI" column in increasing order
df_sorted = filtered_df.sort_values(by="BMI")

# Create an animated scatter plot with Age, Outcome, and BMI
fig_animated = px.scatter(df_sorted, x="Glucose", y="Outcome", animation_frame="BMI", animation_group="Outcome",
                 size="Age", color="Age",
                 labels={"Glucose": "Glucose Level", "Outcome": "Diabetes Outcome", "BMI": "BMI"},
                 title="Animated Scatter Plot of Glucose Level vs. Diabetes Outcome with BMI in Animation")

# Customize the appearance of the plot (optional)
fig_animated.update_traces(marker=dict(size=10),
                  selector=dict(mode='markers+text'))

st.plotly_chart(fig_animated)

st.subheader("Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)")
fig_density_heatmap = px.density_heatmap(filtered_df[filtered_df['Outcome'] == 0], x='DiabetesPedigreeFunction', y='BMI',
                                   labels={'DiabetesPedigreeFunction': 'Diabetes Pedigree Function', 'BMI': 'BMI'},
                                   title='Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)')
st.plotly_chart(fig_density_heatmap)

# Contour Plot (Added per your request)
st.subheader("Contour Plot of Age vs. Average Glucose Level")
fig_contour = px.density_contour(filtered_df, x='Age', y='Glucose', color='Outcome',
                                 title='Contour Plot of Age vs. Glucose Level',
                                 labels={'Age': 'Age', 'Glucose': 'Glucose Level'},
                                 color_discrete_map={0: 'blue', 1: 'red'})
st.plotly_chart(fig_contour)

# Relationships between Smoking Status and Outcome
st.subheader("Relationship between Smoking Status and Outcome")
smoking_outcome_count = filtered_df.groupby(['smoking_status', 'Outcome']).size().reset_index(name='count')
fig_smoking_outcome = px.bar(smoking_outcome_count, x='smoking_status', y='count', color='Outcome', barmode='group', labels={'smoking_status': 'Smoking Status', 'count': 'Count'}, title='Smoking Status vs. Outcome')
st.plotly_chart(fig_smoking_outcome)
# Relationships between Gender and Outcome (Pie Chart)
st.subheader("Relationship between Gender and Outcome")
gender_outcome_count = filtered_df.groupby(['gender', 'Outcome']).size().reset_index(name='count')

# Pie Chart for Gender vs. Outcome
st.subheader(f"Pie Chart: Relationship between Gender and Outcome for {selected_gender if selected_gender != 'All' else 'All Genders'}")
gender_outcome_count = filtered_df.groupby(['gender', 'Outcome']).size().reset_index(name='count')

# Pie Chart for Gender vs. Outcome
st.subheader(f"Pie Chart: Relationship between Gender and Outcome for {selected_gender if selected_gender != 'All' else 'All Genders'}")
gender_outcome_count = filtered_df.groupby(['gender', 'Outcome']).size().reset_index(name='count')

# Pie Chart for Distribution of Diabetes for All Genders
st.subheader("Pie Chart: Distribution of Diabetes for All Genders")
diabetes_count = filtered_df['Outcome'].value_counts().reset_index(name='count')
labels = ['Non-Diabetic', 'Diabetic']

fig_diabetes_pie = px.pie(
    diabetes_count,
    names='index',
    values='count',
    labels={'index': 'Outcome'},
    title="Distribution of Diabetes for All Genders",
    color_discrete_sequence=['green', 'red']  # Green for non-diabetic, red for diabetic
)

st.plotly_chart(fig_diabetes_pie)




