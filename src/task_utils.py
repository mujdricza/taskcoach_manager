
from enum import Enum

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
    
    CATEGORY = "category"
    CATEGORIZABLES = "categorizables"
    SUBJECT = "subject"
    TASK = "task"
    ID = "id"
    PERCENTAGE_COMPLETE = "percentageComplete"  # 'percentageComplete="100"' == Done
    DONE_VALUE = "100"
    
    EFFORT = "effort"
    START = "start"
    STOP = "stop"

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
    
    CATEGORY_TYPE = "Type"
    WORK = "WORK"
    NO_WORK = "NO-WORK"
    

NOWORK_CATEGORIES = ["Pause"]