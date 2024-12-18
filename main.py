from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.streamlit.v1.spreadsheet import _get_mito_backend
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel('data/CLAARITY_with_alo_AF_.xlsx')
    return df

# Load and display the dataset
data = load_data()

# Display basic info about the data
st.write("### Dataset Overview")
st.write(data.head())

# Arrange visualizations in a 3-column layout
col1, col2= st.columns(2)

with col1:
    if 'alo' in data.columns:
        st.write("### Pie Chart of Allocation")
        fig, ax = plt.subplots()
        data['alo'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
    else:
        st.write("Column 'alo' not found in the dataset.")

# Visualization 2
with col2:
    if 'agegrp' in data.columns:
        st.write("### Age Distribution")
        fig, ax = plt.subplots()
        sns.histplot(data['agegrp'], kde=True, bins=20, ax=ax)
        ax.set_xlabel('Age Group')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    else:
        st.write("Column 'agegrp' not found in the dataset.")

col3, col4 = st.columns(2)

# Visualization 3: Boxplot
with col3:
    if 'alo' in data.columns and 'bmi2' in data.columns:
        st.write("### Boxplot of BMI by Allocation Category")
        fig, ax = plt.subplots()
        sns.boxplot(x='alo', y='bmi2', data=data, ax=ax)
        ax.set_xlabel('Allocation Category')
        ax.set_ylabel('BMI')
        st.pyplot(fig)
    else:
        st.write("Required columns ('alo' and 'bmi2') not found in the dataset.")

# Visualization 4: Scatter Plot
with col4:
    if 'height' in data.columns and 'weight' in data.columns:
        st.write("### Scatter Plot of Height and Weight")
        fig, ax = plt.subplots()
        sns.scatterplot(x='height', y='weight', data=data, ax=ax)
        ax.set_xlabel('Height')
        ax.set_ylabel('Weight')
        st.pyplot(fig)
    else:
        st.write("Columns 'height' and 'weight' not found in the dataset.")

# Visualization 5: Distribution of 'alo' Categories (Bar Plot)
col5, col6 = st.columns(2)
with col5:
    if 'alo' in data.columns:
        st.write("### Distribution of Allocation Categories")
        alo_counts = data['alo'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=alo_counts.index, y=alo_counts.values, ax=ax)
        ax.set_xlabel('Allocation Categories')
        ax.set_ylabel('Count')
        st.pyplot(fig)
    else:
        st.write("Column 'alo' not found in the dataset.")

# Add code display and cache-clearing function
def clear_mito_backend_cache():
    _get_mito_backend.clear()

@st.cache_resource
def get_cached_time():
    return {"last_executed_time": None}

def try_clear_cache():
    CLEAR_DELTA = timedelta(hours=12)
    current_time = datetime.now()
    cached_time = get_cached_time()
    if cached_time["last_executed_time"] is None or cached_time["last_executed_time"] + CLEAR_DELTA < current_time:
        clear_mito_backend_cache()
        cached_time["last_executed_time"] = current_time

try_clear_cache()

