import streamlit as st
import pandas as pd
import utils.helper
import utils.config
from datetime import datetime
import networkx as nx
import os
import xlsxwriter


st.markdown("# GG Members")




# def export_groups_to_excel(groups: dict, output_dir="data", filename=None):
#     os.makedirs(output_dir, exist_ok=True)

#     if filename is None:
#         filename = f"gg_groups_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
#     output_path = os.path.join(output_dir, filename)

#     detail_cols = ["Names", "Telehandle", "Year", "Gender", "School", "Available Timeslots", "Role"]

#     try:
#         writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
#         workbook = writer.book
#         use_xlsxwriter = True
#     except Exception:
#         writer = pd.ExcelWriter(output_path, engine="openpyxl")
#         workbook = None
#         use_xlsxwriter = False

#     sheet_name = "Groups"
#     start_row_by_timeslot = {}
#     group_table_width = len(detail_cols) + 1
#     summary_width = 10
#     gap_cols_between_timeslots = 2

#     timeslot_list = list(groups.keys())
#     col_offsets = {}
#     for idx, ts in enumerate(timeslot_list):
#         col_offsets[ts] = idx * (group_table_width + summary_width + gap_cols_between_timeslots)
#         start_row_by_timeslot[ts] = 0

#     for ts in timeslot_list:
#         col_offset = col_offsets[ts]
#         groups_for_ts = groups[ts]
#         for group_idx, group in enumerate(groups_for_ts):
#             start_row = start_row_by_timeslot[ts]

#             leaders = [m for m in group if str(m.get("Role","")).lower() in ["ggl", "tt member"]]
#             members_only = [m for m in group if m not in leaders]
#             ordered = leaders + members_only

#             rows = []
#             for m in ordered:
#                 # Use exact keys, fallback if needed
#                 name = m.get("Names") or m.get("Name") or ""
#                 tele = m.get("Telehandle") or m.get("Telehandle") or ""
#                 year = m.get("Year") or m.get("Year of Matriculation") or ""
#                 gender = m.get("Gender") or ""
#                 school = m.get("School") or ""
#                 av_ts = m.get("Available Timeslots") or m.get("Timeslots") or ""
#                 if isinstance(av_ts, (list, tuple)):
#                     av_ts_str = ", ".join(map(str, av_ts))
#                 else:
#                     av_ts_str = str(av_ts)
#                 role = m.get("Role") or ""

#                 rows.append({
#                     "Names": name,
#                     "Telehandle": tele,
#                     "Year": year,
#                     "Gender": gender,
#                     "School": school,
#                     "Available Timeslots": av_ts_str,
#                     "Role": role
#                 })

#             df_group = pd.DataFrame(rows, columns=detail_cols)

#             header_text = f"{ts} — Group {group_idx + 1}"
#             df_header = pd.DataFrame([{"Names": header_text}])
#             df_header.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=col_offset, index=False, header=False)

#             header_row = start_row + 1
#             pd.DataFrame([detail_cols]).to_excel(writer, sheet_name=sheet_name, startrow=header_row, startcol=col_offset, index=False, header=False)

#             df_group.to_excel(writer, sheet_name=sheet_name, startrow=header_row+1, startcol=col_offset, index=False, header=False)

#             total = len(df_group)
#             males = int((df_group['Gender'].fillna("").str.lower() == "male").sum())
#             females = int((df_group['Gender'].fillna("").str.lower() == "female").sum())
#             year_counts = df_group['Year'].fillna("Unknown").value_counts().to_dict()

#             summary_start_col = col_offset + group_table_width
#             summary_rows = [
#                 ("Total members", total),
#                 ("Males", males),
#                 ("Females", females)
#             ]
#             for y, cnt in year_counts.items():
#                 summary_rows.append((f"Year {y}", int(cnt)))

#             summary_df = pd.DataFrame(summary_rows, columns=["Metric", "Value"])
#             summary_df.to_excel(writer, sheet_name=sheet_name, startrow=header_row, startcol=summary_start_col, index=False, header=False)

#             if use_xlsxwriter:
#                 worksheet = writer.sheets[sheet_name] if sheet_name in writer.sheets else workbook.add_worksheet(sheet_name)
#                 bold_fmt = workbook.add_format({"bold": True})
#                 header_fmt = workbook.add_format({"bold": True, "bg_color": "#DCE6F1"})
#                 leader_name_fmt = workbook.add_format({"bold": True})

#                 worksheet.write(start_row, col_offset, header_text, header_fmt)

#                 for c_idx, col_name in enumerate(detail_cols):
#                     worksheet.write(header_row, col_offset + c_idx, col_name, bold_fmt)

#                 for r_idx in range(len(ordered)):
#                     name_cell_row = header_row + 1 + r_idx
#                     name_cell_col = col_offset
#                     if r_idx < len(leaders):
#                         worksheet.write(name_cell_row, name_cell_col, df_group.iloc[r_idx]["Names"], leader_name_fmt)

#                 widths = [20, 20, 10, 10, 20, 30, 12]
#                 for c_idx, w in enumerate(widths):
#                     worksheet.set_column(col_offset + c_idx, col_offset + c_idx, w)

#                 worksheet.set_column(summary_start_col, summary_start_col + 1, 15)

#             start_row_by_timeslot[ts] = (header_row + 1) + len(df_group) + 3

#     writer.save()
#     return output_path


uploaded_file = st.file_uploader("Choose a file",key = "GG_responses")
if uploaded_file is not None:
    visited = set()
    groups = st.session_state.get("groups",{})
    if "graph" in st.session_state:
        graph = st.session_state.graph
    timeslot_dict = st.session_state.get("timeslot_dict",{})
    group_counters = {timeslot : 0 for timeslot in timeslot_dict}
    members = pd.read_csv(uploaded_file)
    members = members.iloc[:, 1:9]
    members.columns = ["Names", "Telehandle", "Gender", "Year of Matriculation", "School", "Email", "Timeslots", "Preferred Partners"]
    members['Timeslots'] = members['Timeslots'].apply(lambda x: [item.strip() for item in x.split(',')])
    members["Preferred Partners"] = members["Preferred Partners"].apply(
        lambda x: [item.strip() for item in str(x).split(',')] if pd.notna(x) else []
    )
    members['Telehandle'] = members['Telehandle'].str.lower() # Lowercase Telegram Handle
    members['Year'] = members['Year of Matriculation'].apply(utils.helper.calculate_year)

    gender_count = members['Gender'].value_counts()
    year_count = members['Year'].value_counts()
    names = members['Names']

    col1, col2 = st.columns(2)
    with col1:
        st.write(gender_count)
    with col2:
        st.write(year_count)


    st.write(members)

    with st.spinner("Adding members to graph...", show_time=True):
        num_nodes = 0
        for _, row in members.iterrows():
            member_info = {
                'Names': row['Names'],
                'Telehandle': row['Telehandle'],
                'Gender' : row['Gender'],
                'Year': row['Year'],
                'School': row['School'],
                'Role': "Member",
                'Available Timeslots' : [slot.split(' - ')[0] for slot in row['Timeslots']],
                'Preferred Partner' : row['Preferred Partners']
            }
            graph.add_node(row['Telehandle'], data=member_info)
            num_nodes+=1
    st.write(f"number of nodes added: {num_nodes}")
    
    if st.button("Generate Growth Groups", type="primary"):
        with st.spinner("Generating Growth Groups", show_time = True):

            for node in graph.nodes:
                current_node = graph.nodes[node]['data']
                if current_node['Role'] == 'Member':
                    for partner in current_node['Preferred Partner']:
                        if partner in graph.nodes:
                            partner_node = graph.nodes[partner]['data']

                            #Iterate through commmon timeslots
                            common_timeslots = set(current_node['Available Timeslots']).intersection(partner_node['Available Timeslots'])
                            #Create edge for each common timeslot
                            for timeslot in common_timeslots:
                                edge_key = (node, partner, timeslot)

                                if not graph.has_edge(*edge_key[:2]):
                                    graph.add_edge(*edge_key[:2], timeslot = timeslot)
                                    print(f"Partnered {node} with {partner} (common timeslot: {timeslot})")
            partner_groups = [list(component) for component in nx.connected_components(graph) if len(component) > 1]
            for group in partner_groups:

                leader_found = False
                leader_group_key = None
                for node in group:
                    if graph.nodes[node]['data']['Role'] in ['GGL','TT Member']:
                        leader_found = True
                        leader_name = node
                        leader_timeslot = graph.nodes[node]['data']['Available Timeslots'][0]
                        leader_group_key = graph.nodes[node]['data']['Group']
                        visited.add(node)
                if leader_found and leader_group_key and leader_timeslot:
                    for node in group:
                        if all(node in visited for node in group):
                            continue
                        if graph.nodes[node]['data']['Role'] == 'Member' and node not in visited:
                            groups[leader_timeslot][leader_group_key].append(graph.nodes[node]['data'])
                            visited.add(node)
                            print(f"{node} added to {leader_timeslot} {leader_group_key} with {leader_name}")
                if not leader_found:
                    continue
            
            for group in partner_groups:
                group_timeslot = None
                # 🔍 Try to find any edge within the group to get the timeslot
                for i in range(len(group)):
                    for j in range(i + 1, len(group)):
                        node1 = group[i]
                        node2 = group[j]
                        if graph.has_edge(node1, node2):
                            group_timeslot = graph.get_edge_data(node1, node2)['timeslot']
                            break
                    if group_timeslot:
                        break   
                if not group_timeslot:
                    continue
                
                group_index = group_counters[group_timeslot]
                for node in group:
                    if node not in visited and graph.nodes[node]['data']['Role'] == "Member":
                        groups[group_timeslot][group_index].append(graph.nodes[node]['data'])
                        visited.add(node)
                        print(f"{node} added to {group_timeslot} Group - {group_index + 1}")
                group_counters[group_timeslot] = (group_index + 1) % len(groups[group_timeslot])
            
            remaining = []
            for node in graph.nodes:
                if node not in visited and graph.nodes[node]['data']['Role'] == "Member":
                    remaining.append(node)
            print(len(remaining))
            distributed = 0
            for node in remaining:
                node_data = graph.nodes[node]['data']
                available_timeslots = node_data['Available Timeslots']

                best_timeslot= None
                best_group_index = -1

                for timeslot in available_timeslots:
                    if timeslot in groups:
                        available_groups = groups[timeslot]
                        start_index = group_counters[timeslot]

                        for i in range(len(available_groups)):
                            group_index = (start_index + i) % len(available_groups)
                            group = available_groups[group_index]

                            if len(group) < utils.config.GROUP_SIZE:
                                # Check gender distribution
                                males = sum(1 for s in group if s['Gender'] == 'Male')
                                females = sum(1 for s in group if s['Gender'] == 'Female')
                                if (node_data['Gender'] == 'Male' and males < females + 1) or \
                                (node_data['Gender'] == 'Female' and females < males + 1):
                                    best_timeslot = timeslot
                                    best_group_index = group_index
                                    break
                        if best_timeslot and best_group_index != -1:
                            break
                                    
                            
                    
                if best_timeslot and best_group_index != -1:
                    groups[best_timeslot][best_group_index].append(node_data)
                    visited.add(node)
                    group_counters[best_timeslot] = (best_group_index +1) % len(groups[best_timeslot])
                    distributed +=1


                    # groups, group_counters = utils.helper.add_to_group(graph, groups, node, group_counters)
                    
                    # if not added:
                    #     print(f"{node} not added")
        print("distributed",distributed)

        st.write("The following members have not been added:")
        for node in graph.nodes:
            if node not in visited and graph.nodes[node]['data']['Role'] == "Member":
                print(node)
                st.write(node)
                
        st.success("Generated!")
        st.session_state.graph = graph
        st.session_state.groups = groups

        st.markdown("## Growth Groups")
        timeslot_names = list(groups.keys())
        ggCols = st.columns(len(timeslot_names))
        for idx, timeslot in enumerate(timeslot_names):
            count_per_timeslot = 0
            with ggCols[idx]:
                st.header(timeslot)

                timeslot_data = groups[timeslot]
                
                for group in timeslot_data:
                    count_per_group = len(group)
                    with st.container(border=True):
                        st.markdown(f"### Total: {count_per_group} ")
                        for member in group:
                            if member["Role"] != "Member":
                                st.write(f"**{member['Names']}**")
                            else:
                                st.write(member["Names"])
                            count_per_timeslot+=1
            st.write(f"Total for {timeslot}: {count_per_timeslot}")
        
        # if st.button("💾 Save Export"):
            # output_path = export_groups_to_excel(groups, output_dir="data")
            # st.success(f"Exported groups to {output_path}")


# ... your existing code above

    if st.button("💾 Save Export", type="primary"):
        groups = st.session_state.get("groups", {})
        graph = st.session_state.get("graph", None)
        if not graph or not groups:
            st.warning("No graph or groups data available to export.")
        else:

            sample_node = next(iter(graph.nodes), None)
            if not sample_node:
                st.warning("Graph has no nodes to export.")
            else:
                member_keys = list(graph.nodes[sample_node]['data'].keys())

                output_path = "data/growth_groups_export.xlsx"
                writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
                workbook = writer.book
                worksheet = workbook.add_worksheet("Growth Groups")
                writer.sheets["Growth Groups"] = worksheet

                # Define formats
                bold_format = workbook.add_format({'bold': True, 'text_wrap': True})
                header_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1, 'text_wrap': True})
                border_format = workbook.add_format({'border': 1, 'text_wrap': True})
                bold_name_format = workbook.add_format({'bold': True, 'border': 1, 'text_wrap': True})
                title_format = workbook.add_format({'bold': True, 'font_size': 14, 'text_wrap': True})
                timeslot_format = workbook.add_format({'bold': True, 'font_size': 16, 'text_wrap': True})

                max_rows_per_group = 20  # vertical spacing

                # Keep track of max width per column (col index within group box)
                # This will be a dict: col_index -> max width seen
                col_widths = {}

                def update_col_width(col_idx, text):
                    text_len = len(str(text))
                    if col_idx not in col_widths or text_len > col_widths[col_idx]:
                        col_widths[col_idx] = text_len

                def write_group_box(ws, start_row, start_col, group_members, group_name):
                    # Write group title
                    ws.write(start_row, start_col, group_name, title_format)
                    update_col_width(start_col, group_name)
                    start_row += 1

                    # Write headers
                    for c_idx, key in enumerate(member_keys):
                        ws.write(start_row, start_col + c_idx, key, header_format)
                        update_col_width(start_col + c_idx, key)
                    start_row += 1

                    # Sort leaders first
                    leaders = [m for m in group_members if m.get('Role') in ['GGL', 'TT Member']]
                    members_ = [m for m in group_members if m.get('Role') == 'Member']
                    ordered_members = leaders + members_

                    for r_idx, member in enumerate(ordered_members):
                        for c_idx, key in enumerate(member_keys):
                            val = member.get(key, "")
                            if isinstance(val, list):
                                val = ", ".join(str(x) for x in val)
                            if key == 'Names' and member.get('Role') in ['GGL', 'TT Member']:
                                ws.write(start_row + r_idx, start_col + c_idx, val, bold_name_format)
                            else:
                                ws.write(start_row + r_idx, start_col + c_idx, val, border_format)
                            update_col_width(start_col + c_idx, val)

                    data_rows = len(ordered_members)
                    summary_start = start_row + data_rows + 1
                    summary_col = start_col + len(member_keys) + 2

                    ws.write(summary_start, summary_col, "Summary", bold_format)
                    update_col_width(summary_col, "Summary")
                    summary_start += 1

                    total = len(group_members)
                    males = sum(1 for m in group_members if m.get('Gender') == 'Male')
                    females = sum(1 for m in group_members if m.get('Gender') == 'Female')

                    ws.write(summary_start, summary_col, "Total Members:")
                    ws.write(summary_start, summary_col + 1, total)
                    update_col_width(summary_col, "Total Members:")
                    update_col_width(summary_col + 1, total)
                    summary_start += 1

                    ws.write(summary_start, summary_col, "Males:")
                    ws.write(summary_start, summary_col + 1, males)
                    update_col_width(summary_col, "Males:")
                    update_col_width(summary_col + 1, males)
                    summary_start += 1

                    ws.write(summary_start, summary_col, "Females:")
                    ws.write(summary_start, summary_col + 1, females)
                    update_col_width(summary_col, "Females:")
                    update_col_width(summary_col + 1, females)
                    summary_start += 1

                    return max(data_rows + 5, 15)

                # Write timeslot headers horizontally on row 0, spaced 15 columns apart
                timeslot_names = list(groups.keys())
                for col_idx, timeslot in enumerate(timeslot_names):
                    worksheet.write(0, col_idx * 15, f"Timeslot: {timeslot}", timeslot_format)
                    update_col_width(col_idx * 15, f"Timeslot: {timeslot}")

                max_rows_per_group = 20

                for col_idx, timeslot in enumerate(timeslot_names):
                    group_list = groups[timeslot]

                    for group_idx, group_members in enumerate(group_list):
                        group_start_row = 1 + group_idx * (max_rows_per_group + 3)
                        group_name = f"Group {group_idx + 1}"
                        write_group_box(worksheet, group_start_row, col_idx * 15, group_members, group_name)

                # After writing all data, set column widths based on collected max widths
                # Add some padding (+2) for better readability
                for col_idx, width in col_widths.items():
                    adjusted_width = min(width + 2, 50)  # limit max width to 50 chars approx.
                    worksheet.set_column(col_idx, col_idx, adjusted_width)

                writer.close()
                st.success(f"Exported groups to {output_path}")
                st.write(f"File saved at: {output_path}")






                    


    



