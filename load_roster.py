import streamlit as st
import pandas as pd
from datetime import datetime
import networkx as nx
import os

# Main page content
st.title("GGL/TTM")

groups = {}
group_leaders = {}

graph = nx.Graph()

num_nodes = 0
leader_nodes = 0
visited = set()

timeslot_dict = {}


@st.dialog("Load another roster")
def load_file():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        if dataframe:
            st.success("New roster uploaded")
            st.session_state.leader_df = dataframe
            st.rerun()

def confirm_leaders():
    if "leader_df" not in st.session_state:
        return False
    else:
        df = st.session_state.get("leader_df",[])
        timeslot_dict = st.session_state.get("timeslot_dict",{})
        groups = {timeslot: [[] for _ in range(num_groups)] for timeslot, num_groups in timeslot_dict.items()}
        print(groups)
        num_nodes = 0
        for index,row in df.iterrows():
            leader_info = {
                'Names': row['Name'],
                'Telehandle': row['Telegram Handle'],
                'Gender': row['Gender'],
                'Year': row['Year'],
                'School': row['School'],
                'Role': row['Role'],
                'Available Timeslots': row['Timeslot'],
                'Group': row["Group Index"]
            }
            groups[row['Timeslot']][row["Group Index"]-1].append(leader_info)
            graph.add_node(row["Telegram Handle"],data=leader_info)
            num_nodes+=1
        st.session_state.groups = groups
        st.session_state.graph = graph
        print(num_nodes,"added")
        return True

        






file_path = "data/confirmed_roster_test.csv"

loaded = False


if "leader_df" not in st.session_state:
    if os.path.exists(file_path):
        saved_roster_row = st.columns([0.5,0.5])
        with saved_roster_row[0]:
            with st.container(border=True):
                st.success("Existing Leader's Roster found")
                st.write("Would you like to use this roster?")
                if st.button("Yes",type="primary"):
                    df = pd.read_csv(file_path)
                    st.session_state.leader_df = df
                    loaded=True
                    st.write("File loaded successfully.")
else:
    df = st.session_state.get("leader_df",[])
    loaded=True

if loaded:
    st.dataframe(df)
    layout = st.columns(3)
    timeslots = df['Timeslot'].unique()
    num_timeslots = len(timeslots)
    timeslot_dict = {slot:0 for slot in timeslots}
    with layout[1]:
        grid_col = st.columns(num_timeslots)

        for col_index, col in enumerate(grid_col):
            with col:
                st.markdown(f"## {timeslots[col_index]}")

                # Filter rows for this timeslot
                slot_rows = df[df['Timeslot'] == timeslots[col_index]]
                gg_indexes = slot_rows['Group Index'].unique()

                for gg in gg_indexes:
                    timeslot_dict[timeslots[col_index]] +=1
                    with st.container(border=True):
                        st.markdown(f"**Group {gg}**")
                        
                        # Filter rows for this Group Index
                        group_rows = slot_rows[slot_rows['Group Index'] == gg]

                        # Display the Names
                        for _, row in group_rows.iterrows():
                            if row["Role"] == "GGL":
                                st.markdown(f"**{row['Name']}**")
                            else:
                                st.write(row['Name'])  # or st.markdown(row['Name'])
        st.session_state.timeslot_dict = timeslot_dict
        print("timeslot_dict", timeslot_dict)
        button_col = st.columns(3)
        with button_col[0]:
            if st.button("Confirm Roster", type="primary", use_container_width=True):
                confirmed = confirm_leaders()
                if confirmed:
                    st.success("Leaders confirmed!")
                else:
                    st.warning("Unable to confirm leaders, no dataframe found.")

        with button_col[1]:
            if st.button("Load another file", type="secondary", use_container_width=True):
                load_file()
        with button_col[2]:
            st.page_link("create_roster.py", label="**Edit Roster**",use_container_width=True)



