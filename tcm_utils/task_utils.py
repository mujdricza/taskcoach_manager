#!/usr/bin/env python3

"""
Constants and util functions
"""

__author__ = "emm"
__version__ = "20200607"


from enum import Enum
import re

class IO(Enum):
    CSV_EXTENSION = ".csv"
    XLSX_EXTENSION = ".xlsx"

class FORMAT(Enum):
    # NOTE that a task is formulated in a task tag. It can be an empty or a filled element, it can also embed another
    # task element.
    TASK_LINE_BEGIN = "<task "
    TAG_EMPTY_END = "/>"
    TASK_TAG_CLOSING = "</task>"
    PERCENTAGE_100 = 'percentageComplete="100"'
    # all effort tags should be empty
    EFFORT_TAG_BEGIN = "<effort "
    NL = "\n"
    ATTVAL_SEP = "="
    TAG_MARK_OPENING = "<"
    TAG_MARK_CLOSING = ">"
    TAG_MARK_SLASH = "/"
    SPACE = " "
    
    CATEGORY = "category"
    CATEGORIZABLES = "categorizables"
    CATEGORY_LINE_BEGIN = "<category "  # empty tag
    SUBJECT = "subject"
    TASK = "task"
    ID = "id"
    ACTUALSTART_DATE = "actualstartdate"  # tasks with any effort (tracked time) have a start date
    PERCENTAGE_COMPLETE = "percentageComplete"  # 'percentageComplete="100"' == Done
    COMPLETION_DATE = "completiondate"  # done tasks have also a completion date
    DONE_VALUE = "100"
    
    EFFORT = "effort"
    START = "start"
    STOP = "stop"
    
    ATTVAL_PATTERN = re.compile('(?P<attribute>[^=]+)="(?P<value>[^"]+)"')
    GROUP_ATTRIBUTE = "attribute"
    GROUP_VALUE = "value"

class SUMMARY(Enum):
    WORK_CATEGORIES = "WORK-CATEGORIES"
    NONWORK_CATEGORIES = "NONWORK-CATEGORIES"
    
    TASK_NAME = "Task name"
    DESCRIPTION = "Description"
    CATEGORY = "Category"
    PROGRESS = "Progress"
    PROGRESS_WIP = "wip"
    PROGRESS_DONE = "done"
    
    EFFORTS = "Efforts"
    DURATIONS = "Durations"
    OVERALL_DURATION = "Period duration (min)"
    
    CATEGORY_TYPE = "Type"
    WORK = "WORK"
    NO_WORK = "NO-WORK"
    
    START_TIME = "Start (hh:mm:ss)"  # hh:mm:ss
    STOP_TIME = "Stop (hh:mm:ss)"    # hh:mm:ss
    UNTRACKED = "Untracked (minutes)"  # minutes
    

class SPECIAL_CATEGORIES(Enum):
    NOWORK_CATEGORIES = ["Pause"]
    RECURRING = "recurring"
    MISSING = "<missing>"


class DAILY_EFFORTS(Enum):
    BEGIN = "begin"
    END = "end"
    TASK = "task"


class DAY(Enum):
    BEGIN = "00:00:00"
    END = "23:59:59"
