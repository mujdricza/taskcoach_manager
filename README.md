# taskcoach_manager


TaskCoach ([https://www.taskcoach.org/](https://www.taskcoach.org/)) is an open source todo manager with easy time tracking.

This TaskCoach-manager makes the use of TaskCoach more convenient. It automates some steps in TaskCoach:
 - cleaning the current task plan for further use (e.g. if you have some tasks still "work in progress" at the end of a time period like at the end of the week);
 - making a daily overview of efforts (e.g. for the time records at work).
 


## Use

Requirements:
- python>=3.7
- pandas
- XlsxWriter (for xlsx outputs)


### Summarizing the efforts

The python script with modus `-s` / `--csv_summary`, or `-x` / `xlsx_summary`
- takes a given `.tsk` file,
- extracts the efforts (tracked time) to all tasks,
- organizes the efforts per day in a tabular form,
- writes the tabular into a `.csv` or `.xlsx` file.

Run:
```
python taskcoach_manager.py -s <input_fn.tsk> [<output_fn.csv>]
python taskcoach_manager.py -x <input_fn.tsk> [<output_fn.xlsx>]
```

NOTES:
 - Tasks or subtasks without a category will be assigned to an artificial `missing` category.
 - The category "Pause" is considered to be a "not working" category. The efforts with this category will be summarized separately. 
   * The "not working" categories can be customized in the code (`task_utils.SPECIAL_CATEGORIES.NOWORK_CATEGORIES`).

### Cleaning and recycling the task-file

The python script with modus `-c` / `--cleaner`
- takes a given `.tsk` file, 
- removes the done taks (marked with `percentageComplete="100"` in the attribute list of the task),
- removes all further efforts of not done tasks, 
- and writes the remaining tasks in another `.tsk` file. 

The output file can be opened in the TaskCoach for further use.

```
python taskcoach_manager.py -c <input_fn.tsk> [<output_fn.tsk>]
```

NOTES:
- If a 'done' task has the category "recurring", it won't be removed, but only its 'done' status.
  * The name of the "recurrent" category can be customized in the code (`task_utils.SPECIAL_CATEGORIES.RECURRENT`).

In the `data` directory, there are some example inputs and outputs

# Progress

## Todos

* include the task description into the summary output
* improve the style of the xlsx summary (problem: too narrow column width

## Versions

- 20200719:
  * in the summary file, also a track timeline per day is produced
  * tasks without any category will be assigned to a category "missing" in the summary
  * the user gets a warning on efforts with overlapping tracked time (which overlapping trackings are probably accidentally done)
  * new option `-x` creates an xlsx summary
  * `requirements.txt` file added
- 20200628:
  * count the overall efforts for each task during the tracked period, too
  * make sure the user doesn't overwrite the original file
  * handling negative duration with a warning (if the user accidentally set an effort end time before the effort start time, the duration will be negative)
  * handle recurring efforts (don't remove them completely in cleaning mode even if they are 'done')
  * remove 'already started' mark from tasks with efforts in cleaning mode 
- 20200620:
  * use default output file + optional output file parameter
  * make sure the file extensions are as expected
- 20200607:
  * enhanced command line parameters for modus
  * start and stop time per day in daily summary overview
  * tasks without an effort duration are not printed any more
- 20200601:
  * daily summary overview
- 20200217: 
  * init
  * clearing done tasks and further efforts
 
## Contact

Eva Mujdricza-Maydt (me.levelek@gmx.de)

https://github.com/mujdricza/taskcoach_manager/

