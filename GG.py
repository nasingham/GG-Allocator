import streamlit as st
import pandas as pd

# Main page content
st.markdown("# GG Members")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    dataframe = dataframe.iloc[:, 1:8]
    dataframe.columns = ["Names", "Telehandle", "Gender", "Year of Matriculation", "School", "Email", "Timeslots", "Preferred Partners"]
    dataframe['Timeslots'] = dataframe['Timeslots'].apply(lambda x: [item.strip() for item in x.split(',')])
    gender_count = dataframe['Gender'].value_counts()
    year_count = dataframe['Year of Matriculation'].value_counts()
    role_count = dataframe['Role'].value_counts()
    names = dataframe['Names']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(gender_count)
    with col2:
        st.write(year_count)
    with col3:
        st.write(role_count)

    st.write(dataframe)