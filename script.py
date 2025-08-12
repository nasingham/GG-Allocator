import streamlit as st
import pandas as pd
from datetime import datetime
import networkx as nx
import io
import os


st.set_page_config(
    layout="wide",
    page_title="GG Allocator"
)
# # Define the pages
pages = {
    "GGL/TTM": [
        st.Page("load_roster.py", title="Load roster"),
        st.Page("create_roster.py", title="Create new roster"),
    ],
    "Growth Groups": [
        st.Page("load_GG.py", title="Load Growth Groups"),
        st.Page("generate_GG.py", title="Generate new Growth Groups"),
    ],
}

pg = st.navigation(pages, position="top")
pg.run()


# tab1, tab2 = st.tabs(["**TT**", "**GG**"])


# groups = {}
# group_leaders = {}

# graph = nx.Graph()

# num_nodes = 0
# leader_nodes = 0
# visited = set()



# with tab1:
#     st.markdown("# GGL/TTM")


#     file_path = "../Files/confirmed_roster.csv"

#     if os.path.exists(file_path):
#         saved_roster_row = st.columns([0.5,0.5])
#         with saved_roster_row[0]:
#             with st.container(border=True):
#                 st.success("Existing Leader's Roster found")
#                 st.write("Would you like to use this roster?")
#                 if st.button("Yes",type="primary"):
#                     df = pd.read_csv(file_path)
#                     st.write("File loaded successfully.")
#                     st.dataframe(df)
#     else:
#         st.warning("File not found.")

#     uploaded_file = st.file_uploader("Choose a file")
#     if uploaded_file is not None:
#         dataframe = pd.read_csv(uploaded_file)
#         dataframe = dataframe.iloc[:, 2:9]
#         dataframe.columns = ["Names", "Telehandle", "Gender", "Year of Matriculation", "School", "Role", "Timeslots"]
#         dataframe['Timeslots'] = dataframe['Timeslots'].apply(lambda x: [item.strip() for item in x.split(',')])
#         dataframe['Telehandle'] = dataframe['Telehandle'].str.lower() # Lowercase Telegram Handle
#         dataframe['Year'] = dataframe['Year of Matriculation'].apply(calculate_year)
#         unique_timeslots = list(set(slot for sublist in dataframe['Timeslots'] for slot in sublist))

#         weekday_order = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
#         unique_timeslots = sorted(unique_timeslots, key=lambda x: (
#             weekday_order[x.split()[0]],
#             datetime.strptime(x.split()[1], "%I.%M%p")
#         ))

#         num_timeslots = len(unique_timeslots)
#         gender_count = dataframe['Gender'].value_counts()
#         year_count = dataframe['Year'].value_counts()
#         role_count = dataframe['Role'].value_counts()
#         dataframe['Names'] = dataframe['Names'].str.strip()

#         names = dataframe['Names']
#         GGLs = dataframe[dataframe['Role'] == 'GGL']
#         TTMs = dataframe[dataframe['Role'] == 'TT Member']

#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.write(gender_count)
#         with col2:
#             st.write(year_count)
#         with col3:
#             st.write(role_count)

#         st.write(dataframe)

#         st.markdown("## Timeslots")
#         timeslots = st.columns(num_timeslots)
#         for col_index, col in enumerate(timeslots):
#             with col:
#                 st.markdown(f"### {unique_timeslots[col_index]}")

#         for i in range(len(unique_timeslots)):
#             st.session_state[f"GGL_timeslot_{i}"] = GGLs[GGLs['Timeslots'].apply(lambda ts: unique_timeslots[i] in ts)]['Names'].sort_values().tolist()
#             st.session_state[f"TTM_timeslot_{i}"] = TTMs[TTMs['Timeslots'].apply(lambda ts: unique_timeslots[i] in ts)]['Names'].sort_values().tolist()

#         if 'gg_teams' not in st.session_state:
#             st.session_state.gg_teams = {}
#         if 'selected_ggls' not in st.session_state:
#             st.session_state.selected_ggls = set()
#         if 'selected_ttms' not in st.session_state:
#             st.session_state.selected_ttms = set()

#         rows = [st.columns(3, vertical_alignment="top") for _ in range(4)]

#         for row_index, row in enumerate(rows):
#             for col_index, col in enumerate(row):
#                 key = f"{col_index}_{row_index}"
#                 slot_key = unique_timeslots[col_index]

#                 if key not in st.session_state.gg_teams:
#                     st.session_state.gg_teams[key] = {"ggls": [], "ttms": []}

#                 with col.container(height=300):
#                     with st.container(border=True):
#                         top_row = st.columns([1, 1], vertical_alignment="center")  # Adjust width ratio as needed
#                         with top_row[0]:
#                             st.markdown(f"GGLs ({slot_key})")
#                         with top_row[1]:
#                             num_ggls = st.number_input("", 0, 3, key=f"num_ggls_{key}", label_visibility="collapsed")
#                         current_ggls = st.session_state.gg_teams[key].get("ggls",[])
#                         if len(current_ggls) < num_ggls:
#                             current_ggls += [None] * (num_ggls - len(current_ggls))
#                         else:
#                             current_ggls = current_ggls[:num_ggls]
#                         st.session_state.gg_teams[key]["ggls"] = current_ggls
                            
#                         # new_ggls = []
#                         for i in range(num_ggls):
#                             ggl_key = f"gg_teams.{key}.ggls.{i}"
#                             available_ggls = [
#                                 g for g in st.session_state[f"GGL_timeslot_{col_index}"]
#                                 if g not in st.session_state.selected_ggls or g == st.session_state.gg_teams[key]["ggls"][i]
#                             ]
#                             selected = st.selectbox(
#                                 "GGL",
#                                 available_ggls,
#                                 index=available_ggls.index(current_ggls[i]) if current_ggls[i] in available_ggls else None,
#                                 key=ggl_key,
#                                 label_visibility="collapsed",
#                                 placeholder="Choose a GGL"
#                             )
#                             st.session_state.gg_teams[key]["ggls"][i] = selected
#                             st.session_state.selected_ggls.add(selected)

#                     with st.container(border=True):
#                         top_row = st.columns([1,1], vertical_alignment="center")
#                         with top_row[0]:
#                             st.markdown(f"TTMs ({slot_key})")
#                         with top_row[1]:
#                             num_ttms = st.number_input(f"# TTMs ({slot_key})", 0, 3, key=f"num_ttms_{key}", label_visibility="collapsed")
#                         current_ttms = st.session_state.gg_teams[key].get("ttms",[])
#                         if len(current_ttms) < num_ttms:
#                             current_ttms += [None] * (num_ttms - len(current_ttms))
#                         else:
#                             current_ttms = current_ttms[:num_ttms]
#                         st.session_state.gg_teams[key]["ttms"] = current_ttms
#                         for i in range(num_ttms):
#                             ttms_key = f"gg_teams.{key}.ttms.{i}"
#                             available_ttms = [
#                                 g for g in st.session_state[f"TTM_timeslot_{col_index}"]
#                                 if g not in st.session_state.selected_ttms or g == st.session_state.gg_teams[key]["ttms"][i]
#                             ]
#                             selected = st.selectbox(
#                                 "TTM",
#                                 available_ttms,
#                                 index=available_ttms.index(current_ttms[i]) if current_ttms[i] in available_ttms else None,
#                                 key=ttms_key,
#                                 label_visibility="collapsed",
#                                 placeholder="Choose a TTM"
#                             )
#                             st.session_state.gg_teams[key]["ttms"][i] = selected
#                             st.session_state.selected_ttms.add(selected)
#                     # st.write(st.session_state.gg_teams[key]["ggls"])

        
#         layout = st.columns([2,4,2])
#         with layout[1]:
#             st.markdown("## Current Roster")
#             timeslots = st.columns(num_timeslots)
#             for col_index, col in enumerate(timeslots):
#                 with col:
#                     st.markdown(f"### {unique_timeslots[col_index]}")
#             selected = [st.columns(3, vertical_alignment="center") for _ in range(4)]
#             for row_index, row in enumerate(selected):
#                 for col_index, col in enumerate(row):
#                     key = f"{col_index}_{row_index}"
#                     if key in st.session_state.gg_teams:
#                         with col.container(height=200):
#                                 for ggl in st.session_state.gg_teams[key]["ggls"]:
#                                     st.write(f"**{ggl}**")
#                                 for ttm in st.session_state.gg_teams[key]["ttms"]:
#                                     st.write(ttm)
#             left, middle, right = st.columns([1,1,1])
#             with middle:
#                 confirm_leaders = st.button("Confirm Leader Roster", type="primary", use_container_width=True)
#             if confirm_leaders:
#                 with st.spinner("Confirming GGLs/TTMs...", show_time=True):
#                     timeslot_dict = {slot : 0 for slot in unique_timeslots}
#                     for i in range(num_timeslots):
#                         count = 0
#                         for keys in st.session_state.gg_teams.keys():
#                             key = keys.split("_")
#                             slot = int(key[0])
#                             if slot == i and st.session_state.gg_teams[keys].get("ggls"):
#                                 count+=1
#                                 timeslot_dict[unique_timeslots[i]] = count
#                     groups = {timeslot: [[] for _ in range(num_groups)] for timeslot, num_groups in timeslot_dict.items()}
#                     st.session_state.timeslot_dict = timeslot_dict
                    
                    
#                     leaders_names = []
#                     numConfirmedLeaders = 0
#                     numConfirmedTTs = 0
#                     for keys in st.session_state.gg_teams.keys():
#                         slot_index = int(keys.split("_")[0])
#                         full_timeslot = unique_timeslots[slot_index]
#                         group_index = int(keys.split("_")[1])
#                         team = st.session_state.gg_teams[keys]
#                         leaders = team.get("ggls")
#                         numConfirmedLeaders+=len(leaders)
#                         for leader in leaders:
#                             # Case-insensitive match
#                             match = dataframe[dataframe['Names'].str.lower() == leader.lower()]
                            
#                             if not match.empty:
#                                 row = match.iloc[0].to_dict()  # Convert the whole row to a dictionary
#                                 # st.write(row)
#                                 leader_info = {
#                                     'Names': row['Names'],
#                                     'Telehandle': row['Telehandle'],
#                                     'Gender': row['Gender'],
#                                     'Year': row['Year'],
#                                     'School': row['School'],
#                                     'Role': row['Role'],
#                                     'Available Timeslots': [full_timeslot],
#                                     'Group': group_index
#                                 }
#                                 # do something with leader_info
#                                 groups[full_timeslot][group_index].append(leader_info)
#                                 graph.add_node(row['Telehandle'], data=leader_info)
#                                 num_nodes+=1
#                             else:
#                                 print(f"Leader {leader} not found in dataframe!")
                            

#                             leaders_names +=leaders
#                         tts = team.get("ttms")
#                         numConfirmedTTs += len(tts)
#                         for tt in tts:
#                             match = dataframe[dataframe['Names'].str.lower() == tt.lower()]
                        
#                             if not match.empty:
#                                 row = match.iloc[0].to_dict()  # Convert the whole row to a dictionary
                                
#                                 leader_info = {
#                                     'Names': row['Names'],
#                                     'Telehandle': row['Telehandle'],
#                                     'Gender': row['Gender'],
#                                     'Year': row['Year'],
#                                     'School': row['School'],
#                                     'Role': row['Role'],
#                                     'Available Timeslots': [full_timeslot],
#                                     'Group': group_index
#                                 }
#                                 # st.write(leader_info)
#                                 # do something with leader_info
#                                 groups[full_timeslot][group_index].append(leader_info)
#                                 graph.add_node(row['Telehandle'], data=leader_info)
#                                 num_nodes+=1
                                
#                             else:
#                                 print(f"Leader {tt} not found in dataframe!")

#                         leaders_names +=tts
                    
#                     #To export roster
#                     confirmed_roster = []

#                     for timeslot, group_list in groups.items():
#                         for group_index, group_members in enumerate(group_list):
#                             for member in group_members:
#                                 confirmed_roster.append({
#                                     "Name": member["Names"],
#                                     "Telegram Handle": member["Telehandle"],
#                                     "Gender": member["Gender"],
#                                     "Year": member["Year"],
#                                     "School": member["School"],
#                                     "Role": member["Role"],
#                                     "Timeslot": timeslot,
#                                     "Group Index": group_index + 1
#                                 })
#                     # Create a DataFrame
#                     confirmed_df = pd.DataFrame(confirmed_roster)

#                     # # Define a nearby output path (e.g. ./output/)
#                     # output_dir = "saved_output"
#                     # os.makedirs(output_dir, exist_ok=True)

#                     # output_path = os.path.join(output_dir, "confirmed_roster.csv")

#                     # # Save to CSV
#                     # confirmed_df.to_csv(output_path, index=False)
#                     # 👇 Convert your DataFrame to a CSV string in memory
#                     csv_buffer = io.StringIO()
#                     confirmed_df.to_csv(csv_buffer, index=False)
#                     csv_data = csv_buffer.getvalue()
#                     st.download_button(
#                         label="📥 Download Confirmed Roster CSV",
#                         data=csv_data,
#                         file_name="confirmed_roster.csv",
#                         mime="text/csv"
#                     )

#                     # ✅ Streamlit download button (no disk write needed)
                    

#                     # st.success(f"📁 Confirmed roster exported to `{output_path}`")


#                 st.write(f"Total of {numConfirmedLeaders} GGLs and {numConfirmedTTs} TTMs have been confirmed")                
#             st.write(f"number of nodes added: {num_nodes}")
            
#             if groups:
#                 st.write(groups)
#                 st.session_state["groups"] = groups
#             if graph:
#                 st.session_state["graph"] = graph
#             if num_nodes:
#                 st.session_state["num_nodes"]=num_nodes
                    

                    



# with tab2:
#     st.markdown("# GG Members")

#     uploaded_file = st.file_uploader("Choose a file", key="GG_responses")
#     if uploaded_file is not None:
#         groups = st.session_state.groups
#         graph = st.session_state["graph"]
#         num_nodes = st.session_state["num_nodes"]
#         timeslot_dict = st.session_state.timeslot_dict
#         group_counters = {timeslot: 0 for timeslot in timeslot_dict}
#         members = pd.read_csv(uploaded_file)
#         members = members.iloc[:, 1:9]
#         members.columns = ["Names", "Telehandle", "Gender", "Year of Matriculation", "School", "Email", "Timeslots", "Preferred Partners"]
#         members['Timeslots'] = members['Timeslots'].apply(lambda x: [item.strip() for item in x.split(',')])
#         members["Preferred Partners"] = members["Preferred Partners"].apply(
#             lambda x: [item.strip() for item in str(x).split(',')] if pd.notna(x) else []
#         )
#         members['Telehandle'] = members['Telehandle'].str.lower() # Lowercase Telegram Handle
#         members['Year'] = members['Year of Matriculation'].apply(calculate_year)


#         gender_count = members['Gender'].value_counts()
#         year_count = members['Year'].value_counts()
#         names = members['Names']

#         col1, col2 = st.columns(2)
#         with col1:
#             st.write(gender_count)
#         with col2:
#             st.write(year_count)


#         st.write(members)
#         # print(graph.nodes)
#         # now_ggs = st.session_state.gg_teams.keys()
#         # st.write(now_ggs)
#         # st.write(st.session_state.gg_teams)
#         with st.spinner("Adding members to graph...", show_time=True):
#             for _, row in members.iterrows():
#                 member_info = {
#                     'Names': row['Names'],
#                     'Telegram Handle': row['Telehandle'],
#                     'Gender' : row['Gender'],
#                     'Year': row['Year'],
#                     'School': row['School'],
#                     'Role': "Member",
#                     'Available Timeslots' : [slot.split(' - ')[0] for slot in row['Timeslots']],
#                     'Preferred Partner' : row['Preferred Partners']
#                 }
#                 graph.add_node(row['Telehandle'], data=member_info)
#                 num_nodes+=1
#         st.write(f"number of nodes added: {num_nodes}")
#         if st.button("Generate Growth Groups", type="primary"):
#             with st.spinner("Generating Growth Groups", show_time=True):
#                 for node in graph.nodes:
#                     current_node = graph.nodes[node]['data']
#                     # print("current",current_node)

#                     if current_node['Role'] == 'Member':
#                         for partner in current_node['Preferred Partner']:
#                             if partner in graph.nodes:
#                                 partner_node = graph.nodes[partner]['data']
#                                 # print("partner", partner_node)

#                                 # Iterate through common timeslots
#                                 common_timeslots = set(current_node['Available Timeslots']).intersection(partner_node['Available Timeslots'])
#                                 # print("common",common_timeslots)
#                                 # Create edge for each common timeslot
#                                 for timeslot in common_timeslots:
#                                     # Use a unique edge key for each timeslot
#                                     edge_key = (node, partner, timeslot)
#                                     print(edge_key)

#                                     if not graph.has_edge(*edge_key[:2]):  # Avoid duplicate edges for same nodes
#                                         graph.add_edge(*edge_key[:2], timeslot=timeslot)  # Store timeslot as edge attribute
#                                         print(f"Partnered {node} with {partner} (common timeslot: {timeslot})")
                
#                 partner_groups = [list(component) for component in nx.connected_components(graph) if len(component) > 1]
#                 print("Partner Groups:")
#                 for group in partner_groups:
#                     print(group)  # Prints the nodes in the partner group
#                     # Print edges and timeslots within the group
#                     for node1 in group:
#                         for node2 in group:
#                             if node1 != node2 and graph.has_edge(node1, node2):
#                                 timeslot = graph.get_edge_data(node1, node2)['timeslot']
#                                 print(f"  Edge: ({node1}, {node2}), Timeslot: {timeslot}")

                
#                 for group in partner_groups:
#                     leader_found = False
#                     leader_group_key = None
#                     for node in group:
#                         if graph.nodes[node]['data']['Role'] in ['GGL', 'TT Member']:
#                             leader_found = True
#                             leader_name = node
#                             leader_timeslot = graph.nodes[node]['data']['Available Timeslots'][0]
#                             leader_group_key = graph.nodes[node]['data']['Group']
#                             visited.add(node)
#                             # if leader_found:
#                             #     print(leader_found, node)
#                             break
#                     if leader_found and leader_group_key and leader_timeslot:
#                         for node in group:
#                             if graph.nodes[node]['data']['Role'] == 'Member' and node not in visited:
#                                 groups[leader_timeslot][leader_group_key].append(graph.nodes[node]['data'])
#                                 visited.add(node)
#                                 print(f"{node} added to {leader_timeslot} {leader_group_key} with {leader_name}")
#                     if not leader_found:
#                         continue
#                 for group in partner_groups:
#                     group_timeslot = None

#                     # 🔍 Try to find any edge within the group to get the timeslot
#                     for i in range(len(group)):
#                         for j in range(i + 1, len(group)):
#                             node1 = group[i]
#                             node2 = group[j]
#                             if graph.has_edge(node1, node2):
#                                 group_timeslot = graph.get_edge_data(node1, node2)['timeslot']
#                                 break
#                         if group_timeslot:
#                             break

#                     if not group_timeslot:
#                         print(f"⚠️ No edge/timeslot found for group: {group}, skipping...")
#                         continue  # Skip group if no edge with timeslot

#                     group_index = group_counters[group_timeslot]
#                     for node in group:
#                         if node not in visited and graph.nodes[node]['data']['Role'] == "Member":
#                             groups[group_timeslot][group_index].append(graph.nodes[node]['data'])
#                             visited.add(node)
#                             print(f"{node} added to {group_timeslot} Group - {group_index + 1}")

#                     group_counters[group_timeslot] = (group_index + 1) % len(groups[group_timeslot])

#                 remaining = []
#                 for node in graph.nodes:
#                     if node not in visited and graph.nodes[node]['data']['Role'] == "Member":
#                         remaining.append(node)
#                 print(len(remaining))
#                 distributed = 0
#                 for node in remaining:
#                     added = add_to_group(node, group_counters)
#                     distributed +=1
#                     if not added:
#                         print(f"{node} not added")
#                 print(distributed)

#             st.success("Generated!")

#             st.markdown("## Growth Groups")
#             timeslot_names = list(groups.keys())
#             ggCols = st.columns(len(timeslot_names))
#             for idx, timeslot in enumerate(timeslot_names):
#                 count_per_timeslot = 0
#                 with ggCols[idx]:
#                     st.header(timeslot)

#                     timeslot_data = groups[timeslot]
                    
#                     for group in timeslot_data:
#                         count_per_group = len(group)
#                         with st.container(border=True):
#                             st.markdown(f"### Total: {count_per_group} ")
#                             for member in group:
#                                 if member["Role"] != "Member":
#                                     st.write(f"**{member["Names"]}**")
#                                 else:
#                                     st.write(member["Names"])
#                                 count_per_timeslot+=1
#                 st.write(f"Total for {timeslot}: {count_per_timeslot}")

            
            # for col_index, col in enumerate(grid_col):
            #     with col:
            #         st.markdown(f"### {timeslot_dict[col_index+1]}")