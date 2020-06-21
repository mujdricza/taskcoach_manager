#!/usr/bin/env python3

"""
This script organizes the TaskCoach manager.

The tool TaskCoach is a freely available time tracker and task manager (https://www.taskcoach.org/).

"""

__author__ = "emm"
__version__ = "20200607"


import argparse
from enum import Enum
import logging
import os
import sys
from __init__ import logger
import task_cleaner
import task_summary


class MODUS(Enum):
    CLEANER = "cleaner"
    SUMMARY = "summary"


def get_arguments(args):
    
    parser = argparse.ArgumentParser(description="This TaskCoach-manager makes the use of TaskCoach more convenient.")
    # parser.add_argument("modus", choices=[MODUS.CLEANER.value, MODUS.SUMMARY.value],
    #                     help=f"Modus of the tool. Options: {MODUS.CLEANER.value}, {MODUS.SUMMARY.value}")
    #
    parser.add_argument("input",
                        help="Input filename with file extension .tsk.")
    parser.add_argument("-o", "--output_fn",
                        help=f"Output filename. "
                             f"This should have the file extension '.tsk' in modus '{MODUS.CLEANER.value}', "
                             f"and the file extension '.csv' in modus '{MODUS.SUMMARY.value}'. "
                             f"If not given, the outputs will be saved in the folder of the input file.")
    modus = parser.add_mutually_exclusive_group(required=True)
    modus.add_argument("-c", "--cleaner", action="store_true", dest="cleaner",
                       help="Cleaning modus.")
    modus.add_argument("-s", "--summary", action="store_true", dest="summary",
                       help="Summary modus.")
    
    return parser.parse_args(args)


def main_cleaner(input_fn: str, output_fn: str) -> None:
    task_cleaner.clean_tasks(input_fn, output_fn)


def main_summary(input_fn: str, output_fn: str) -> None:
    task_summary.summarize_tasks(input_fn, output_fn)


if __name__ == "__main__":
    
    arguments = get_arguments(sys.argv[1:])
    logger.debug(f"python {' '.join(sys.argv)}")
    
    cleaner = arguments.cleaner
    summary = arguments.summary
    input_fn = arguments.input
    
    output_fn = None
    if arguments.output_fn:
        output_fn = arguments.output_fn
        
    
    if cleaner:
        main_cleaner(input_fn, output_fn)
    elif summary:
        main_summary(input_fn, output_fn)
