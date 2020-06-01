#!/usr/bin/env python3

"""
This script organizes the TaskCoach manager.

The tool TaskCoach is a freely available time tracker and task manager (https://www.taskcoach.org/).


"""

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
    parser.add_argument("modus", choices=[MODUS.CLEANER.value, MODUS.SUMMARY.value],
                        help=f"Modus of the tool. Options: {MODUS.CLEANER.value}, {MODUS.SUMMARY.value}")
    parser.add_argument("input",
                        help="Input filename with file extension .tsk.")
    parser.add_argument("output",
                        help=f"Output filename. In case of modus '{MODUS.CLEANER.value}', it is another .tsk file "
                             f"generated."
                             f"If modus '{MODUS.SUMMARY.value}' is selected, the output file should have "
                             f"a file extension .csv or .tsv.")
    
    return parser.parse_args(args)




def main_cleaner(input_fn:str, output_fn:str) -> None:
    task_cleaner.clean_tasks(input_fn, output_fn)


def main_summary(input_fn:str, output_fn:str) -> None:
    task_summary.summarize_tasks(input_fn, output_fn)


if __name__ == "__main__":
    
    
    arguments = get_arguments(sys.argv[1:])
    logger.debug(f"python {' '.join(sys.argv)}")
    
    modus = arguments.modus
    input_fn = arguments.input
    output_fn = arguments.output
    
    if modus == MODUS.CLEANER.value:
        main_cleaner(input_fn, output_fn)
    elif modus == MODUS.SUMMARY.value:
        main_summary(input_fn, output_fn)
    
