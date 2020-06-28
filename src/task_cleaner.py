#!/usr/bin/env python3

"""
This script prepares the task-file from the previous week for being used in the current week.
- Delete done items.
- Clear timer.
"""


__author__ = "emm"
__version__ = "20200621"  # "20200217"


import os
import re
import sys
from typing import List, Tuple, Union

from __init__ import logger
from task_utils import FORMAT, SPECIAL_CATEGORIES

# typing aliases
LINES_WITH_AMOUNT_OF_CHANGES = Tuple[List[str], int]
TSK_EXTENSION = ".tsk"
OUTPUT_EXTENSION = "_cleaned" + TSK_EXTENSION


def clean_tasks(input_task_xml_fn: str, output_task_xml_fn: Union[str, None]) -> None:
    
    msg = f"The output file name extension should be '{TSK_EXTENSION}'."
    if not (output_task_xml_fn is None or output_task_xml_fn.endswith(TSK_EXTENSION)):
        logger.error(msg)
        sys.exit(1)
    
    lines = __read_lines(input_task_xml_fn)
    logger.info("READ {} lines from '{}'.".format(len(lines), input_task_xml_fn))

    # clear done tasks
    cleared_lines, found_done_tasks = __remove_done_tasks(lines)
    logger.info("- cleared {} done tasks".format(found_done_tasks))

    # clear done efforts
    cleared_lines, found_efforts = __remove_efforts(cleared_lines)
    logger.info("- cleared {} efforts additionally".format(found_efforts))
    
    if output_task_xml_fn is None:
        output_task_xml_fn = os.path.splitext(input_task_xml_fn)[0] + OUTPUT_EXTENSION
    else:
        output_path = os.path.realpath(os.path.dirname(output_task_xml_fn))
        os.makedirs(output_path, exist_ok=True)
        
    write_lines(cleared_lines, output_task_xml_fn)
    logger.info("DONE. SEE cleared tasks in '{}'.".format(output_task_xml_fn))


def __read_lines(input_fn: str) -> List[str]:
    with open(input_fn) as f:
        lines = [line.strip() for line in f.readlines()]

    return lines


def __get_att2val_dict(line, tagname):
    
    stripped_line = line.lstrip(FORMAT.TAG_MARK_OPENING.value)
    stripped_line = stripped_line.lstrip(tagname)
    stripped_line = stripped_line.rstrip(FORMAT.TAG_MARK_CLOSING.value)
    stripped_line = stripped_line.rstrip(FORMAT.TAG_MARK_SLASH.value)
    stripped_line = stripped_line.strip()
    # print(f" only attvalues: {stripped_line}")
    
    att2val_dict = {}
    attval_items = FORMAT.ATTVAL_PATTERN.value.findall(stripped_line)
    # print(f"attval_items: {attval_items}")
    for attval_item in attval_items:
        att = attval_item[0].strip()
        val = attval_item[1].strip()
        att2val_dict[att] = val
    
    return att2val_dict


def __get_task_ids_with_recurrent_category(lines, recurring_category):
    
    # assumption: there is at most one recurring category line
    recurrent_task_ids = []
    for line in lines:
        if line.startswith(FORMAT.CATEGORY_LINE_BEGIN.value):
            att2val_dict = __get_att2val_dict(line, FORMAT.CATEGORY.value)
            if FORMAT.SUBJECT.value not in att2val_dict or FORMAT.CATEGORIZABLES.value not in att2val_dict:
                logger.error(f"NOT ASSUMED category line FORMAT. LINE = '{line}'")
                sys.exit(1)
            subject = att2val_dict[FORMAT.SUBJECT.value]
            if subject == recurring_category:
                return att2val_dict[FORMAT.CATEGORIZABLES.value].split()
               

def __get_task_id(line):
    att2val_dict = __get_att2val_dict(line, FORMAT.TASK.value)
    
    if not FORMAT.ID.value in att2val_dict:
        logger.error(f"NOT ASSUMED task line FORMAT. LINE = '{line}'")
        sys.exit(1)
    return att2val_dict[FORMAT.ID.value]


def __get_line_start_and_end(line):
    
    first_space_idx = line.index(FORMAT.SPACE.value)
    line_start = line[:first_space_idx]
    
    try:
        ending_idx = line.index(FORMAT.TAG_EMPTY_END.value)
    except ValueError:  # substring not found
        try:
            ending_idx = line.index(FORMAT.TAG_MARK_CLOSING.value)
        except ValueError:
            logger.error(f"NOT ASSUMED line FORMAT: '{line}'")
            sys.exit(1)
    line_end = line[ending_idx:]
    
    return line_start, line_end


def __remove_done_status(line):
    line_start, line_end = __get_line_start_and_end(line)
    att2val_dict = __get_att2val_dict(line, FORMAT.TASK.value)
    if FORMAT.PERCENTAGE_COMPLETE.value in att2val_dict:
        del att2val_dict[FORMAT.PERCENTAGE_COMPLETE.value]
    if FORMAT.COMPLETION_DATE.value in att2val_dict:
        del att2val_dict[FORMAT.COMPLETION_DATE.value]
    if FORMAT.ACTUALSTART_DATE.value in att2val_dict:
        del att2val_dict[FORMAT.ACTUALSTART_DATE.value]
    
    return "".join([line_start,
                    " ",
                    " ".join([att+FORMAT.ATTVAL_SEP.value+'"'+val+'"' for att, val in att2val_dict.items()]),
                    " ",
                    line_end])


def __remove_done_tasks(lines: List[str], recurring_category=SPECIAL_CATEGORIES.RECURRING.value) \
        -> LINES_WITH_AMOUNT_OF_CHANGES: # List[str]:

    # Stragtegy: We search for a FORMAT.PERTCENTAGE_100.value value, which is assumed to be in a task tag.
    # then try to find the beginning and end of the current tag.
    # We always remove only one case of "done", and continue to do changes till there is no "done" case any more.
    IS_THERE_ANY_DONE_CASE = True
    CHANGES = 0
    cleared_lines = lines
    
    # get task ids with recurring category
    recurring_task_ids = __get_task_ids_with_recurrent_category(lines, recurring_category)
    
    while IS_THERE_ANY_DONE_CASE == True:
        CHANGE = False
        for idx, line in enumerate(cleared_lines):
            line = line.strip()
            if FORMAT.PERCENTAGE_100.value in line:
                CHANGES += 1
                # check whether the task is recurring
                task_id = __get_task_id(line)
                # remove only the 'done' status
                if task_id in recurring_task_ids:
                    cleared_lines[idx] = __remove_done_status(line)
                # remove the whole task
                else:
                    CHANGE = True
                    # print("\t* candidate in {}. line: '{}'".format(idx, line))
                    # search for the beginning and end
                    start_idx = idx
                    if not line.startswith(FORMAT.TASK_LINE_BEGIN.value):
                        msg = f"PERCENTAGE ATTRIBUTE IS ASSUMED IN THE OPENING task TAG. " \
                              f"CURRENT {idx}. LINE IS NOT EXPECTED:\n{line}"
                        raise ValueError(msg)
    
                    end_idx = start_idx  # if task tag is empty
                    if not line.endswith(FORMAT.TAG_EMPTY_END.value):
                        # task tag is not empty -> search for the closing tag
                        while cleared_lines[end_idx].strip() != FORMAT.TASK_TAG_CLOSING.value:
                            #print("\t\tSEARCH FOR CLOSING: {}.: '{}'".format(end_idx, lines[end_idx]))
                            end_idx += 1
                            assert end_idx < len(lines)
            if CHANGE == True:
                # change the lines list
                # print("\t--> get lines from {}-{}".format(start_idx, end_idx))
                cleared_lines = cleared_lines[:start_idx] + cleared_lines[end_idx + 1:]
                break

        if CHANGE == False:
            IS_THERE_ANY_DONE_CASE = False

    return cleared_lines, CHANGES


def __remove_efforts(lines: List[str]) -> LINES_WITH_AMOUNT_OF_CHANGES: # List[str]:

    line_idx_not_relevant = []
    
    for idx, line in enumerate(lines):
        line = line.strip()
        # remove all efforts
        if line.startswith(FORMAT.EFFORT_TAG_BEGIN.value):
            if not line.endswith(FORMAT.TAG_EMPTY_END.value):
                msg = "EFFORT TAG IS ASSUMED TO BE EMPTY. CURRENT {}. LINE HAS A NOT EXPECTED FORMAT:\n{}".format(
                    idx, line)
                raise ValueError(msg)

            line_idx_not_relevant.append(idx)
        # remove all starting marks
        elif line.startswith(FORMAT.TASK_LINE_BEGIN.value):
            lines[idx] = __remove_done_status(line)
    # change the lines list
    cleared_lines = [line for idx, line in enumerate(lines) if idx not in line_idx_not_relevant]

    return cleared_lines, len(line_idx_not_relevant)


def write_lines(lines: List[str], output_fn: str) -> None:
    with open(output_fn, "w") as f:
        for line in lines:
            f.write(line)
            f.write(FORMAT.NL.value)


# # for inpection purposes only
# if __name__ == "__main__":
#
#     args = sys.argv
#
#     # default input
#     #input_path = "/mnt/d/emm/Verwaltung/Tasks/"
#     input_path = "../data/"
#     input_fn = input_path + "tasks_2020_0210-0214.tsk"
#     output_fn = input_path + "tasks_2020_0217-0220.tsk"
#
#     if len(args) > 2:
#         input_fn = args[1]
#         output_fn = args[2]
#
#     clean_tasks(input_fn, output_fn)
