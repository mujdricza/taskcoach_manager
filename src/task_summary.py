#!/usr/bin/env python3

"""
This script generates a daily-wise overview of the efforts for each task in the given task-file.

NOTE:
- only efforts with a given category are considered --> Make sure that all task items with effort have a category assigned!
- categories not considered as "work" are hard coded now in task_utils.NOWORK_CATEGORIES

"""

__author__ = "emm"
__version__ = "20200607"


import xml.dom.minidom as mdom
import os
from pprint import pformat
from datetime import datetime
import time
import pandas as pd

from __init__ import logger
from task_utils import FORMAT, SUMMARY, NOWORK_CATEGORIES
from typing import List, Dict, Tuple
# typing aliases
Document = mdom.Document
LINES_WITH_AMOUNT_OF_CHANGES = Tuple[List[str], int]



def summarize_tasks(input_task_xml_fn: str, output_csv_fn: str) -> None:
    
    logger.info(f"READING doctree from '{input_task_xml_fn}'")
    doctree = __read_xml(input_task_xml_fn)
    
    logger.info(f"GETTING CATEGORIES")
    category_dict = __get_categories(doctree)

    logger.info("GETTING EFFORTS")
    task_dict = __get_efforts(doctree)
    
    logger.info("BUILDING SUMMARY TABLE")
    task_summary_df = __build_summary_df(category_dict, task_dict)
    
    logger.info(f"WRITING SUMMARY to '{output_csv_fn}'")
    __write_summary(task_summary_df, output_csv_fn)
    
    logger.info("WRITTEN task summary into '{}'.".format(output_csv_fn))


def __read_xml(input_fn: str) -> Document:
    
    tree = mdom.parse(input_fn)
    return tree


def __get_categories(doctree:Document):
    """
    NOTE: it is problematic that the children nodes of a "category" element are also named
    "category".
    
    <category categorizables="083b799e-49c2-11ea-b4f2-7cb27d86f5b0 0f75c180-4751-11ea-8dd7-7cb27d86f5b0 2109bede-473f-11ea-8cdf-7cb27d86f5b0 447916cf-9dd6-11ea-8f79-7cb27d86f5b4 9c1ccc6e-4745-11ea-bfbf-7cb27d86f5b0" creationDateTime="2020-02-18 10:24:45.383000" expandedContexts="('categoryviewer', 'categoryviewerintaskeditor')" id="805edd6e-5230-11ea-b2a1-7cb27d86f5b1" modificationDateTime="2020-02-18 10:30:48.253000" status="1" subject="Work">
<category categorizables="308977e1-4751-11ea-bfa8-7cb27d86f5b0 5fbe46cf-4751-11ea-bbf3-7cb27d86f5b0 6dc520a1-4751-11ea-ba4b-7cb27d86f5b0 99f450b0-4751-11ea-94d2-7cb27d86f5b0 bba82761-4740-11ea-a402-7cb27d86f5b0 bfa35980-47f3-11ea-8147-7cb27d86f5b0 f8af465e-9dd6-11ea-8788-7cb27d86f5b4" creationDateTime="2020-02-18 10:30:43.376000" expandedContexts="('categoryviewerintaskeditor',)" id="55c04300-5231-11ea-92eb-7cb27d86f5b1" modificationDateTime="2020-02-18 10:30:46.007000" status="1" subject="axx" />
<category categorizables="27d823e1-9dd6-11ea-ac93-7cb27d86f5b4 4de44870-9dd6-11ea-affd-7cb27d86f5b4 5e32a140-9dd6-11ea-aeb8-7cb27d86f5b4 a324edcf-9dd6-11ea-8500-7cb27d86f5b4 c386441e-9dd6-11ea-96ca-7cb27d86f5b4 ea5f7cb0-9dd6-11ea-b4b0-7cb27d86f5b4" creationDateTime="2020-02-18 10:30:48.252000" expandedContexts="('categoryviewerintaskeditor',)" id="58a86ecf-5231-11ea-bd01-7cb27d86f5b1" modificationDateTime="2020-02-18 10:30:56.029000" status="1" subject="dtk" />
</category>
<category categorizables="060c30cf-4741-11ea-82d1-7cb27d86f5b0 4b73c040-47f8-11ea-8a66-7cb27d86f5b0 b9f0e500-4741-11ea-98f2-7cb27d86f5b0" creationDateTime="2020-02-18 10:26:48.118000" expandedContexts="('categoryviewerintaskeditor',)" id="c986bd61-5230-11ea-a490-7cb27d86f5b1" modificationDateTime="2020-02-18 10:26:53.022000" status="1" subject="Pause" />
    :param lines:
    :return:
    """

    root = doctree.documentElement

    category_dict = {}  # key: category subject, value: list of task-ids for that category

    for element in root.childNodes:
        if element.nodeType == mdom.Node.ELEMENT_NODE:
            if element.tagName == FORMAT.CATEGORY.value:
                __get_category_info_rec(element, parent_names=[], concatenator="->", category_dict=category_dict)
    
    logger.debug(f"CATEGORY_DICT:\n{pformat(category_dict, indent=2, compact=False)}")
    return category_dict


def __get_efforts(doctree):
    root = doctree.documentElement
    
    task_dict = {}
    
    for element in root.childNodes:
        if element.nodeType == mdom.Node.ELEMENT_NODE:
            if element.tagName == FORMAT.TASK.value:
                __get_task_info_rec(element, current_task_id=None, task_dict=task_dict)
    
    logger.debug(f"TASK_DICT:\n{pformat(task_dict, indent=2, compact=False)}")
    return task_dict


def __get_task_info_rec(current_task_node, current_task_id=None, task_dict={}):
    """
    <task creationDateTime="2020-05-24 17:53:51.714000" expandedContexts="('taskviewer',)" id="c386441e-9dd6-11ea-96ca-7cb27d86f5b4" modificationDateTime="2020-05-29 11:44:24.750000" status="1" subject="SHI">
        <task actualstartdate="2020-05-27 09:36:13" creationDateTime="2020-05-27 09:13:22.096000" id="8c75fb00-9fe9-11ea-b5b5-7cb27d86f5b4" modificationDateTime="2020-05-27 09:36:13.670000" status="1" subject="20200525-results SHfirst">
            <effort id="bdfb9061-9fec-11ea-bb56-7cb27d86f5b4" start="2020-05-27 09:36:13" status="1" stop="2020-05-27 10:00:55" />
        </task>
        <task actualstartdate="2020-05-29 11:44:10" creationDateTime="2020-05-29 11:44:24.749000" id="fb0c95d1-a190-11ea-b7f8-7cb27d86f5b4" modificationDateTime="2020-05-29 11:44:31.952000" status="1" subject="Weiteres">
            <effort id="ff5785f0-a190-11ea-8a28-7cb27d86f5b4" start="2020-05-29 11:44:10" status="1" stop="2020-05-29 11:50:22" />
        </task>
    </task>
    :param current_task_node:
    :param parent_names:
    :param task_dict:
    :return:
    """
    if current_task_node.nodeType != mdom.Node.ELEMENT_NODE:
        return
    
    if current_task_node.tagName == FORMAT.TASK.value:
    
        task_id = None
        task_subject = None
        task_progress = SUMMARY.PROGRESS_WIP.value
        
        if not current_task_node.hasAttributes():
            raise ValueError(f"Node '{current_task_node}' doesn't have any attributes")
        
        curr_attributes = current_task_node.attributes  # xml.dom.minidom.NamedNodeMap
        for attname, attval in curr_attributes.items():
            if attname == FORMAT.ID.value:
                task_id = attval
            elif attname == FORMAT.PERCENTAGE_COMPLETE.value:
                if attval == FORMAT.DONE_VALUE.value:
                    task_progress = SUMMARY.PROGRESS_DONE.value
            elif attname == FORMAT.SUBJECT.value:
                task_subject = attval
            
        task_dict[task_id] = {SUMMARY.PROGRESS.value : task_progress,
                              SUMMARY.TASK_NAME.value : task_subject,
                              SUMMARY.EFFORTS.value : {},  # day : start : stop
                              SUMMARY.DURATIONS.value : {},  # day : minutes
                              SUMMARY.DESCRIPTION.value: ""}
        
        if current_task_node.hasChildNodes():
            for child_node in current_task_node.childNodes:
                
                __get_task_info_rec(child_node,
                                    current_task_id=task_id,
                                    task_dict=task_dict)
    
    elif current_task_node.tagName == FORMAT.EFFORT.value:
        # <effort id="ff5785f0-a190-11ea-8a28-7cb27d86f5b4" start="2020-05-29 11:44:10" status="1" stop="2020-05-29 11:50:22" />
        if not current_task_node.hasAttributes():
            raise ValueError(f"Node '{current_task_node}' doesn't have any attributes")

        curr_attributes = current_task_node.attributes  # xml.dom.minidom.NamedNodeMap
        start_val = None
        stop_val = None
        for attname, attval in curr_attributes.items():
            if attname == FORMAT.START.value:
                start_val = attval
            elif attname == FORMAT.STOP.value:
                stop_val = attval
        assert start_val != None
        assert stop_val != None
        
        day_dict = __get_effort_time(start_val, stop_val)
        for day, minutes in day_dict.items():
            task_dict[current_task_id][SUMMARY.DURATIONS.value].setdefault(day, 0)
            task_dict[current_task_id][SUMMARY.DURATIONS.value][day] += minutes
            
            task_dict[current_task_id][SUMMARY.EFFORTS.value].setdefault(day, {})
            task_dict[current_task_id][SUMMARY.EFFORTS.value][day][start_val] = stop_val
        
        
def __get_effort_time(start_val:str, stop_val:str) -> Dict[str, int]:
    """NOTE that for now, only the effort on the first day is considered. E.g., if you are working over night, only the part of the effort until midnight is counted.
    
    :param start_val:
    :param stop_val:
    :return:
    """
    # start="2020-05-29 11:44:10"
    # stop="2020-05-29 11:50:22"
    # https://stackoverflow.com/questions/2788871/date-difference-in-minutes-in-python
    
    
    start_day = start_val.split(" ")[0]
    stop_day = stop_val.split(" ")[0]
    if start_day != stop_day:
        logger.warning(f"Effort done over multiple days ({start_val} -> {stop_val})! Only the part upto midnight of the first day will be considered!")
        stop_val = start_day + " 23:59:59"
    

    fmt = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime(start_val, fmt)
    d2 = datetime.strptime(stop_val, fmt)
    
    # Convert to Unix timestamp
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())

    # They are now in seconds, subtract and then divide by 60 to get minutes.
    effort_in_minutes = int(d2_ts - d1_ts) // 60
    
    return {start_day : effort_in_minutes}
    

def __get_id(currnode):
    id = None
    if currnode.hasAttributes():
        id_att = currnode.getAttributeNode(FORMAT.ID.value)
        id_val = id_att.value
    return id


def __get_category_info_rec(current_category_node,
                            parent_names=[],
                            concatenator="->",
                            category_dict={}):
    
    if current_category_node.nodeType != mdom.Node.ELEMENT_NODE:
        return
    
    cat_name = None
    task_ids = []
    if not current_category_node.hasAttributes():
        raise ValueError(f"Node '{current_category_node}' doesn't have any attributes")
    
    curr_attributes = current_category_node.attributes  # xml.dom.minidom.NamedNodeMap
    for attname, attval in curr_attributes.items():
        if attname == FORMAT.CATEGORIZABLES.value:
            task_ids = attval.strip().split(" ")
        if attname == FORMAT.SUBJECT.value:
            cat_name = concatenator.join(parent_names + [attval])
    category_dict[cat_name] = task_ids
    
    if current_category_node.hasChildNodes():
        parent_names.append(cat_name)
        for child_node in current_category_node.childNodes:
            __get_category_info_rec(child_node,
                                    parent_names=parent_names,
                                    concatenator=concatenator,
                                    category_dict=category_dict)

def __get_days(task_dict):
    
    days = set()
    # task_dict: { current_task_id : { SUMMARY.DURATIONS.value: {day:minutes} } }
    for task_id, duration_dict in task_dict.items():
        days |= duration_dict[SUMMARY.DURATIONS.value].keys()
    
    return days


def __is_earlier(datum, saved_datum):
    if saved_datum is None:
        return True
    day, time = datum.split()
    saved_day, saved_time = saved_datum.split()
    
    if day < saved_day:
        return True
    elif day == saved_day:
        if time < saved_time:
            return True
    return False


def __is_later(datum, saved_datum):
    if saved_datum is None:
        return True
    
    day, time = datum.split()
    saved_day, saved_time = saved_datum.split()
    
    if day > saved_day:
        return True
    elif day == saved_day:
        if time > saved_time:
            return True
    return False


def __get_offsets_per_day(task_dict):
    
    days = sorted(list(__get_days(task_dict)))
    
    offsets_per_day_dict = {day: {SUMMARY.START_TIME.value:None,
                                  SUMMARY.STOP_TIME.value:None,
                                  SUMMARY.UNTRACKED.value:"(todo)"  # TODO
                                  } for day in days}
    
    for task_id, task_info_dict in task_dict.items():
        for day, start2stop_dict in task_info_dict[SUMMARY.EFFORTS.value].items():
            for start, stop in start2stop_dict.items():
                saved_start = offsets_per_day_dict[day][SUMMARY.START_TIME.value]
                saved_stop = offsets_per_day_dict[day][SUMMARY.STOP_TIME.value]
                
                if __is_earlier(start, saved_start):
                    offsets_per_day_dict[day][SUMMARY.START_TIME.value] = start
                if __is_later(stop, saved_stop):
                    offsets_per_day_dict[day][SUMMARY.STOP_TIME.value] = stop
    
    return offsets_per_day_dict
                
    

def __build_summary_df(category_dict,
                       task_dict,
                       nowork_categories=NOWORK_CATEGORIES,
                       drop_task_without_effort=True) -> pd.DataFrame:
    
    days = sorted(list(__get_days(task_dict)))
    logger.debug(f"Days: {days}")
    item_list = []
    
    for category, task_id_list in category_dict.items():
        label = SUMMARY.NO_WORK.value if category in nowork_categories else SUMMARY.WORK.value
        
        for task_id in task_id_list:
            task_effort_dict = task_dict[task_id]
            if drop_task_without_effort:
                if not task_effort_dict[SUMMARY.DURATIONS.value]:
                    continue
            task_name = task_effort_dict[SUMMARY.TASK_NAME.value]
            duration_per_day_dict = task_effort_dict[SUMMARY.DURATIONS.value]
            progress = task_effort_dict[SUMMARY.PROGRESS.value]
            description = task_effort_dict[SUMMARY.DESCRIPTION.value]
    
            item = {
                SUMMARY.CATEGORY_TYPE.value : label,
                SUMMARY.CATEGORY.value : category,
                SUMMARY.TASK_NAME.value : task_name,
                SUMMARY.PROGRESS.value : progress,
                SUMMARY.DESCRIPTION.value : description
            }
            
            # duration
            for day in days:
                duration = 0
                if day in duration_per_day_dict:
                    duration = duration_per_day_dict[day]
                item[day] = duration
            
            item_list.append(item)

    item_start = {
        SUMMARY.CATEGORY_TYPE.value: "",
        SUMMARY.CATEGORY.value: "",
        SUMMARY.TASK_NAME.value: SUMMARY.START_TIME.value,
        SUMMARY.PROGRESS.value: "",
        SUMMARY.DESCRIPTION.value: ""
    }
    item_stop = {
        SUMMARY.CATEGORY_TYPE.value: "",
        SUMMARY.CATEGORY.value: "",
        SUMMARY.TASK_NAME.value: SUMMARY.STOP_TIME.value,
        SUMMARY.PROGRESS.value: "",
        SUMMARY.DESCRIPTION.value: ""
    }
    item_untracked = {
        SUMMARY.CATEGORY_TYPE.value: "",
        SUMMARY.CATEGORY.value: "",
        SUMMARY.TASK_NAME.value: SUMMARY.UNTRACKED.value,
        SUMMARY.PROGRESS.value: "",
        SUMMARY.DESCRIPTION.value: ""
    }

    # duration
    offsets_per_day_dict = __get_offsets_per_day(task_dict)
    for day in days:
        item_start[day] = offsets_per_day_dict[day][SUMMARY.START_TIME.value].split()[1]
        item_stop[day] = offsets_per_day_dict[day][SUMMARY.STOP_TIME.value].split()[1]
        item_untracked[day] = offsets_per_day_dict[day][SUMMARY.UNTRACKED.value]
    
    item_list_2 = []
    item_list_2.append(item_start)
    item_list_2.append(item_stop)
    item_list_2.append(item_untracked)
    
    task_summary_df = pd.DataFrame(item_list)
    to_append_df_list = []
    offsets_df = pd.DataFrame(item_list_2)
    to_append_df_list.append(offsets_df)
    
    # get some overview measures, too
    work_sums_minutes = task_summary_df.sum(numeric_only=True, axis=0)
    work_sums_hours = task_summary_df.sum(numeric_only=True, axis=0) / 60

    work_sums_minutes[SUMMARY.TASK_NAME.value] = f"SUMMED ALL (minutes)"
    work_sums_hours[SUMMARY.TASK_NAME.value] = f"SUMMED ALL (hours)"

    work_sums_minutes_df = pd.DataFrame([work_sums_minutes], columns=task_summary_df.columns)
    work_sums_hours_df = pd.DataFrame([work_sums_hours], columns=task_summary_df.columns)

    # task_summary_df = task_summary_df.append(work_sums_minutes_df).reset_index(drop=True)
    # task_summary_df = task_summary_df.append(work_sums_hours_df).reset_index(drop=True)
    
    to_append_df_list.append(work_sums_minutes_df)
    to_append_df_list.append(work_sums_hours_df)

    for category_type in [SUMMARY.WORK.value, SUMMARY.NO_WORK.value]:
        work_df = task_summary_df[task_summary_df[SUMMARY.CATEGORY_TYPE.value]==category_type]
        
        work_sums_minutes = work_df.sum(numeric_only=True, axis=0)
        work_sums_hours = work_df.sum(numeric_only=True, axis=0)/60
        
        work_sums_minutes[SUMMARY.TASK_NAME.value] = f"SUMMED {category_type} (minutes)"
        work_sums_hours[SUMMARY.TASK_NAME.value] = f"SUMMED {category_type} (hours)"
        
        work_sums_minutes_df = pd.DataFrame([work_sums_minutes], columns = task_summary_df.columns)
        work_sums_hours_df = pd.DataFrame([work_sums_hours], columns = task_summary_df.columns)

        # task_summary_df = task_summary_df.append(work_sums_minutes_df).reset_index(drop=True)
        # task_summary_df = task_summary_df.append(work_sums_hours_df).reset_index(drop=True)

        to_append_df_list.append(work_sums_minutes_df)
        to_append_df_list.append(work_sums_hours_df)
    
    for to_append_df in to_append_df_list:
        task_summary_df = task_summary_df.append(to_append_df).reset_index(drop=True)
    
    return task_summary_df


def __write_summary(overview_df: pd.DataFrame, output_fn: str) -> None:
    
    path_name = os.path.dirname(output_fn)
    os.makedirs(path_name, exist_ok=True)
    
    with open(output_fn, "w") as f:
        overview_df.to_csv(f, index=False)
