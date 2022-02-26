#!/usr/bin/env python3

"""
This script organizes the TaskCoach manager.

The tool TaskCoach is a freely available time tracker and task manager (https://www.taskcoach.org/).

"""

__author__ = "emm"
__version__ = "20220206"  # "20200607"


import argparse
from enum import Enum
import logging
import os
import sys
from tcm_utils.__init__ import logger
from tcm_utils import task_cleaner, task_summary
from tcm_utils.task_utils import IO


class MODUS(Enum):
    CLEANER = "cleaner"
    CSV_SUMMARY = "csv_summary"
    XLSX_SUMMARY = "xlsx_summary"


def get_arguments(args):
    
    parser = argparse.ArgumentParser(description="This TaskCoach-manager makes the use of TaskCoach more convenient.")
    parser.add_argument("input_fn",
                        help="Input filename with file extension .tsk.")
    parser.add_argument("-o", "--output_fn",
                        help=f"Output filename. "
                             f"This should have the file extension '.tsk' in modus '{MODUS.CLEANER.value}', "
                             f"and the file extension '.csv'/'.xlsx' in modi "
                             f"'{MODUS.CSV_SUMMARY.value}'/'{MODUS.XLSX_SUMMARY.value}' respectively. "
                             f"If not given, the outputs will be automatically saved in the folder of the input file "
                             f"with the expected file extension.")
    modus = parser.add_mutually_exclusive_group(required=True)
    modus.add_argument("-c", "--cleaner", action="store_true", dest="cleaner",
                       help="Cleaning modus: it takes a .tsk file and removes all efforts and done tasks; "
                            "this functionality is beneficial if someone tracks her/his tasks periodically, e.g. "
                            "each week, and would like to work on 'work-in-progress' tasks in the next time period.")
    modus.add_argument("-s", "--summary", action="store_true", dest="summary",
                       help="Summary modus with csv output: "
                            "a table-formatted per-day summary on the efforts will be extracted")
    modus.add_argument("-x", "--xlsx", action="store_true", dest="xlsx_summary",
                       help="Summary modus with xlsx output: "
                            "a table-formatted per-day summary on the efforts will be extracted")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="for printing debugging information")
    return parser.parse_args(args)


def main_cleaner(input_fn: str, output_fn: str) -> None:
    task_cleaner.clean_tasks(input_fn, output_fn)


def main_summary(input_fn: str, output_fn: str, extension:str) -> None:
    task_summary.summarize_tasks(input_fn, output_fn, extension)


if __name__ == "__main__":
    
    arguments = get_arguments(sys.argv[1:])
    if arguments.debug:
        logger.setLevel(logging.DEBUG)
    logger.debug(f"RUNNING: python {' '.join(sys.argv)}")
    
    cleaner = arguments.cleaner
    csv_summary = arguments.summary
    xlsx_summary = arguments.xlsx_summary
    input_fn = arguments.input_fn
    
    output_fn = None
    if arguments.output_fn:
        output_fn = arguments.output_fn
        if os.path.realpath(output_fn) == os.path.realpath(input_fn):
            msg = f"The outputs would overwrite the input file '{input_fn}'!\n" \
                  f"Please take another file name for the outputs."
            sys.exit(msg)
    
    if cleaner:
        main_cleaner(input_fn, output_fn)
    elif csv_summary:
        main_summary(input_fn, output_fn, IO.CSV_EXTENSION.value)
    elif xlsx_summary:
        main_summary(input_fn, output_fn, IO.XLSX_EXTENSION.value)
        
