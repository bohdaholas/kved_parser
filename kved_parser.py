"""
Github repository: https://github.com/bohdaholas/kved_parser
"""

import json


def get_kved_data(class_code):
    """
    Get the following kved data according to input class_code:
    section - division - group - class
    >>> len(get_kved_data("01.11"))
    4
    """
    with open("kved.json", encoding="utf-8") as file:
        kved_data = list(json.load(file).values())
        sections = kved_data[0][0]
        for section in sections:
            for division in section["divisions"]:
                if class_code.startswith(division["divisionCode"]):
                    for group in division["groups"]:
                        if class_code.startswith(group["groupCode"]):
                            for class_ in group["classes"]:
                                if class_code.startswith(class_["classCode"]):
                                    return section, division, group, class_
    return None


def invert_kved_data(section, division, group, class_):
    """
    Invert kved data
    >>> len(invert_kved_data(*get_kved_data("01.11")))
    3
    """
    section_data = {"name": section['sectionName'],
                    "type": "section",
                    "num_children": len(section['divisions'])}
    division_data = {"name": division['divisionName'],
                     "type": "division",
                     "num_children": len(division['groups']),
                     "parent": section_data}
    group_data = {"name": group['groupName'],
                  "type": "group",
                  "num_children": len(group['classes']),
                  "parent": division_data}
    class_data = {"name": class_['className'],
                  "type": "class",
                  "parent": group_data}
    return class_data


def parse_kved(class_code):
    """
    Write results to a json file
    >>> parse_kved("01.14")
    """
    results = invert_kved_data(*get_kved_data(class_code))
    with open("kved_results.json", 'w', encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)
