import streamlit as st
import pandas as pd
import utils.helper
from datetime import datetime
import io
import networkx as nx

st.set_page_config(layout="wide")
st.title("Edit GGL/TTM Roster")

graph = nx.Graph()
timeslot_dict = {}

# Confirmed roster (already assigned)
# if "leader_df" not in st.session_state:
#     st.error("No confirmed roster loaded. Please return to the main page.")
#     st.stop()
# confirmed_df = st.session_state.leader_df.copy()

# Sign-up pool

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
    

signup_file = st.file_uploader("Upload Sign-Up CSV", type="csv")
if signup_file:
    signup_df = pd.read_csv(signup_file)
    signup_df = signup_df.iloc[:,2:9]
    signup_df.columns = ["Name", "Telegram Handle", "Gender", "Year", "School", "Role", "Timeslots"]
    signup_df['Timeslots'] = signup_df['Timeslots'].apply(lambda x: [item.strip() for item in x.split(',')])

    signup_df["Telegram Handle"] = signup_df["Telegram Handle"].str.lower()
    signup_df['Year'] = signup_df['Year'].apply(utils.helper.calculate_year)
    unique_timeslots = list(set(slot for sublist in signup_df['Timeslots'] for slot in sublist))
    weekday_order = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    unique_timeslots = sorted(unique_timeslots, key=lambda x: (
        weekday_order[x.split()[0]],
        datetime.strptime(x.split()[1], "%I.%M%p")
    ))
    num_timeslots = len(unique_timeslots)
    timeslot_dict = {slot:0 for slot in unique_timeslots}

    gender_count = signup_df['Gender'].value_counts()
    year_count = signup_df['Year'].value_counts()
    role_count = signup_df['Role'].value_counts()
    signup_df['Name'] = signup_df['Name'].str.strip()
    names = signup_df['Name']
    GGLs = signup_df[signup_df['Role'] == 'GGL']
    TTMs = signup_df[signup_df['Role'] == 'TT Member']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(gender_count)
    with col2:
        st.write(year_count)
    with col3:
        st.write(role_count)

    st.write(signup_df)

    st.markdown("## Timeslots")
    col_slots = st.columns(num_timeslots)
    for col_index, col in enumerate(col_slots):
        with col:
            st.markdown(f"### {unique_timeslots[col_index]}")
    
    for i in range(len(unique_timeslots)):
        st.session_state[f"GGL_timeslot_{i}"] = GGLs[GGLs['Timeslots'].apply(lambda ts: unique_timeslots[i] in ts)]['Name'].sort_values().tolist()
        st.session_state[f"TTM_timeslot_{i}"] = TTMs[TTMs['Timeslots'].apply(lambda ts: unique_timeslots[i] in ts)]['Name'].sort_values().tolist()

    if 'gg_teams' not in st.session_state:
        st.session_state.gg_teams = {}
    if 'selected_ggls' not in st.session_state:
        st.session_state.selected_ggls = set()
    if 'selected_ttms' not in st.session_state:
        st.session_state.selected_ttms = set()
    
    rows = [st.columns(3, vertical_alignment="top") for _ in range (4)]

    for row_index, row in enumerate(rows):
        for col_index, col in enumerate(row):
            key = f"{col_index}_{row_index}"
            slot_key = unique_timeslots[col_index]

            if key not in st.session_state.gg_teams:
                st.session_state.gg_teams[key]= {"ggls":[] , "ttm":[]}
            
            with col.container(height=300):
                with st.container(border=True):
                    top_row = st.columns([1,1], vertical_alignment="center")
                    with top_row[0]:
                        st.markdown(f"GGLs ({slot_key})")
                    with top_row[1]:
                        num_ggls = st.number_input("",0,3,key=f"num_ggls_{key}", label_visibility="collapsed")
                    current_ggls = st.session_state.gg_teams[key].get("ggls",[])
                    if len(current_ggls) < num_ggls:
                        current_ggls += [None] * (num_ggls - len(current_ggls))
                    else:
                        current_ggls = current_ggls[: num_ggls]
                    st.session_state.gg_teams[key]["ggls"] = current_ggls


                    for i in range(num_ggls):
                        ggl_key = f"gg_teams.{key}.ggls.{i}"
                        available_ggls = [
                            g for g in st.session_state[f"GGL_timeslot_{col_index}"]
                            if g not in st.session_state.selected_ggls or g == st.session_state.gg_teams[key]["ggls"][i]
                        ]
                        selected = st.selectbox(
                            "GGL",
                            available_ggls,
                            index = available_ggls.index(current_ggls[i]) if current_ggls[i] in available_ggls else None,
                            key = ggl_key,
                            label_visibility="collapsed",
                            placeholder="Choose a GGL"
                        )
                        st.session_state.gg_teams[key]["ggls"][i] = selected
                        st.session_state.selected_ggls.add(selected)
                with st.container(border=True):
                    top_row = st.columns([1,1], vertical_alignment="center")
                    with top_row[0]:
                        st.markdown(f"TTMs ({slot_key})")
                    with top_row[1]:
                        num_ttms = st.number_input(f"# TTMs ({slot_key})", 0, 3, key=f"num_ttms_{key}", label_visibility="collapsed")
                    current_ttms = st.session_state.gg_teams[key].get("ttms",[])
                    if len(current_ttms) < num_ttms:
                        current_ttms += [None] * (num_ttms - len(current_ttms))
                    else:
                        current_ttms = current_ttms[:num_ttms]
                    st.session_state.gg_teams[key]["ttms"] = current_ttms
                    for i in range(num_ttms):
                        ttms_key = f"gg_teams.{key}.ttms.{i}"
                        available_ttms = [
                            g for g in st.session_state[f"TTM_timeslot_{col_index}"]
                            if g not in st.session_state.selected_ttms or g == st.session_state.gg_teams[key]["ttms"][i]
                        ]
                        selected = st.selectbox(
                            "TTM",
                            available_ttms,
                            index=available_ttms.index(current_ttms[i]) if current_ttms[i] in available_ttms else None,
                            key=ttms_key,
                            label_visibility="collapsed",
                            placeholder="Choose a TTM"
                        )
                        st.session_state.gg_teams[key]["ttms"][i] = selected
                        st.session_state.selected_ttms.add(selected)
    
    layout = st.columns([2,4,2])
    with layout[1]:
        st.markdown("## Current Roster")
        timeslots = st.columns(num_timeslots)
        for col_index, col in enumerate(timeslots):
            with col:
                st.markdown(f"### {unique_timeslots[col_index]}")
        selected = [st.columns(3, vertical_alignment="center") for _ in range(4)]
        for row_index, row in enumerate(selected):
            for col_index, col in enumerate(row):
                key = f"{col_index}_{row_index}"
                if key in st.session_state.gg_teams:
                    with col.container(height=200):
                            for ggl in st.session_state.gg_teams[key]["ggls"]:
                                st.write(f"**{ggl}**")
                            for ttm in st.session_state.gg_teams[key]["ttms"]:
                                st.write(ttm)

    #     # --- Export Roster ---
    # confirmed_roster = []

    # for key, members in st.session_state.gg_teams.items():
    #     col_index, row_index = map(int, key.split("_"))
    #     timeslot = unique_timeslots[col_index]
    #     group_index = row_index + 1  # 1-based index

    #     for role_type, names_list in [("ggls", members["ggls"]), ("ttms", members["ttms"])]:
    #         for name in names_list:
    #             if name:  # skip empty slots
    #                 # Lookup details in signup_df
    #                 details = signup_df[signup_df["Name"] == name].iloc[0]
    #                 confirmed_roster.append({
    #                     "Name": details["Name"],
    #                     "Telegram Handle": details["Telegram Handle"],
    #                     "Gender": details["Gender"],
    #                     "Year": details["Year"],
    #                     "School": details["School"],
    #                     "Role": details["Role"],
    #                     "Timeslot": timeslot,
    #                     "Group Index": group_index
    #                 })

    # if confirmed_roster:
    #     confirmed_df = pd.DataFrame(confirmed_roster)
    #     csv_buffer = io.StringIO()
    #     confirmed_df.to_csv(csv_buffer, index=False)
    #     csv_data = csv_buffer.getvalue()
    #     st.download_button(
    #         label="📥 Download Confirmed Roster CSV",
    #         data=csv_data,
    #         file_name="confirmed_roster.csv",
    #         mime="text/csv"
    #     )
    button_layout = st.columns([2,4,2])
    with button_layout[1]:
        if st.button("💾 Save Roster", type="primary"):
            confirmed_roster = []

            for key, members in st.session_state.gg_teams.items():
                col_index, row_index = map(int, key.split("_"))
                timeslot = unique_timeslots[col_index]
                group_index = row_index + 1  # 1-based index

                for role_type, names_list in [("ggls", members["ggls"]), ("ttms", members["ttms"])]:
                    for name in names_list:
                        if name:  # skip empty slots
                            details = signup_df[signup_df["Name"] == name].iloc[0]
                            confirmed_roster.append({
                                "Name": details["Name"],
                                "Telegram Handle": details["Telegram Handle"],
                                "Gender": details["Gender"],
                                "Year": details["Year"],
                                "School": details["School"],
                                "Role": details["Role"],
                                "Timeslot": timeslot,
                                "Group Index": group_index
                            })
                            timeslot_dict[timeslot] = group_index

            if confirmed_roster:
                confirmed_df = pd.DataFrame(confirmed_roster)
                st.session_state.leader_df = confirmed_df
                st.session_state.timeslot_dict = timeslot_dict
                output_path = "data/confirmed_roster_test.csv"  # save in /data folder
                confirmed_df.to_csv(output_path, index=False)
                st.success(f"Roster saved to {output_path}")
                # st.write(timeslot_dict)

            else:
                st.warning("No roster data to save.")
        
        if st.button("Confirm Roster", type="primary"):
                    confirmed = confirm_leaders()
                    if confirmed:
                        st.success("Leaders confirmed!")
                    else:
                        st.warning("Unable to confirm leaders, no dataframe found.")
        
  
                    






else:
    st.warning("Upload a sign-up file to begin.")
    st.stop()


