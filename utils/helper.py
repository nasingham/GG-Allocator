from datetime import datetime

import utils.config


def calculate_year(year_of_matriculation):
    if str(year_of_matriculation).lower() == 'staff':
        return 'Staff'
    if str(year_of_matriculation).lower() == 'exchange student':
        return 'Exchange Student'
    return datetime.now().year - int(year_of_matriculation)



def add_to_group(graph, groups, node_name, group_counters):
    node_data = graph.nodes[node_name]['data']
    available_timeslots = node_data['Available Timeslots']

    best_timeslot = None
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

    # Add to the best group found
    if best_timeslot is not None and best_group_index != -1:
        group = groups[best_timeslot][best_group_index]
        node_data['Group'] = f'{best_timeslot} - Group {best_group_index + 1}'
        node_data['Role'] = 'Member'
        group.append(node_data)
        group_counters[best_timeslot] = (best_group_index + 1) % len(groups[best_timeslot])
        return groups, group_counters

    return False