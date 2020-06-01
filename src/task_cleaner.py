#!/usr/bin/env python3

"""
This script prepares the task-file from the previous week for being used in the current week.
- Delete done items.
- Clear timer.

__author__ = "emm"
__version__ = "20200217"
"""

from typing import List, Tuple
import sys
from enum import Enum

from __init__ import logger
from task_utils import FORMAT

# typing aliases
LINES_WITH_AMOUNT_OF_CHANGES = Tuple[List[str], int]


def clean_tasks(input_task_xml_fn: str, output_task_xml_fn: str) -> None:

    lines = __read_lines(input_task_xml_fn)
    logger.info("READ {} lines from '{}'.".format(len(lines), input_task_xml_fn))

    # clear done tasks
    cleared_lines, found_done_tasks = __remove_done_tasks(lines)
    logger.info("- cleared {} done tasks".format(found_done_tasks))

    # clear done efforts
    cleared_lines, found_efforts = __remove_efforts(cleared_lines)
    logger.info("- cleared {} efforts additionally".format(found_efforts))

    write_lines(cleared_lines, output_task_xml_fn)
    logger.info("WRITTEN cleared tasks into '{}'.".format(output_task_xml_fn))


def __read_lines(input_fn: str) -> List[str]:
    with open(input_fn) as f:
        lines = [line.strip() for line in f.readlines()]

    return lines


def __remove_done_tasks(lines: List[str]) -> LINES_WITH_AMOUNT_OF_CHANGES: # List[str]:

    # Stragtegy: We search for a FORMAT.PERTCENTAGE_100.value value, which is assumed to be in a task tag.
    # then try to find the beginning and end of the current tag.
    # We always remove only one case of "done", and continue to do changes till there is no "done" case any more.
    IS_THERE_ANY_DONE_CASE = True
    CHANGES = 0
    cleared_lines = lines

    while IS_THERE_ANY_DONE_CASE == True:
        CHANGE = False
        for idx, line in enumerate(cleared_lines):
            line = line.strip()
            if FORMAT.PERCENTAGE_100.value in line:
                CHANGE = True
                CHANGES += 1
                # print("\t* candidate in {}. line: '{}'".format(idx, line))
                # search for the beginning and end
                start_idx = idx
                if not line.startswith(FORMAT.TASK_LINE_BEGIN.value):
                    msg = "PERCENTAGE ATTRIBUTE IS ASSUMED IN THE OPENING task TAG. CURRENT {}. LINE IS NOT EXPECTED:\n{}".format(
                        idx, line)
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

    # Stragtegy: We search for a FORMAT.EFFORT_TAG_BEGIN.value value, which is assumed to be an empty tag on just one line.
    IS_THERE_ANY_DONE_CASE = True

    line_idx_not_relevant = []

    for idx, line in enumerate(lines):
        line = line.strip()
        if line.startswith(FORMAT.EFFORT_TAG_BEGIN.value):
            if not line.endswith(FORMAT.TAG_EMPTY_END.value):
                msg = "EFFORT TAG IS ASSUMED TO BE EMPTY. CURRENT {}. LINE HAS A NOT EXPECTED FORMAT:\n{}".format(
                    idx, line)
                raise ValueError(msg)

            line_idx_not_relevant.append(idx)

    # change the lines list
    cleared_lines = [line for idx, line in enumerate(lines) if idx not in line_idx_not_relevant]

    return cleared_lines, len(line_idx_not_relevant)


def write_lines(lines: List[str], output_fn: str) -> None:
    with open(output_fn, "w") as f:
        for line in lines:
            f.write(line)
            f.write(FORMAT.NL.value)


if __name__ == "__main__":

    args = sys.argv

    # default input
    #input_path = "/mnt/d/emm/Verwaltung/Tasks/"
    input_path = "../data/"
    input_fn = input_path + "tasks_2020_0210-0214.tsk"
    output_fn = input_path + "tasks_2020_0217-0220.tsk"

    if len(args) > 2:
        input_fn = args[1]
        output_fn = args[2]

    clean_tasks(input_fn, output_fn)
