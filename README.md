# taskcoach_manager
This TaskCoach-manager makes the use of TaskCoach more convenient. It automates some steps in TaskCoach:
 - cleaning the current task plan for further use (e.g. if you have some tasks still "work in progress" at the end of a time period like at the end of the week);
 - making a daily overview of efforts (e.g. for the time records at work).
 
 ---


TaskCoach ([https://www.taskcoach.org/](https://www.taskcoach.org/)) is an open source todo manager with easy time tracking.

TaskCoach saves the tasks and efforts in an XML file with extension `.tsk`. 


## Use

Requirements:
- python>=3.7
- pandas


```
python taskcoach_manager.py <modus> <input_fn> <output_fn>
```
If `modus` is
* `-s` or `--summary`: the script will extract a per-day summary on the taken efforts in a tabular format.
* `-c` or `--cleaner`: the script makes a copy of the tracked tasks without the already done efforts and done tasks, and thus recycles the task file for further use; e.g. if someone periodically tracks similar tasks. A new, cleaned task file is then ready to further use.

### Summarizing the efforts

The python script with modus `-s` or `--summary`
- takes a given `.tsk` file,
- extracts the efforts (tracked time) to all tasks,
- organizes the efforts per day in a tabular form,
- writes the tabular into a `.csv` file.

Run:
```
python taskcoach_manager.py -s <input_fn.tsk> [<output_fn.csv>]
```

Note that only tasks or subtasks with a category will be considered!

### Recycling the task-file

The python script with modus `-c` or `--cleaner`
- takes a given `.tsk` file, 
- removes the done taks (marked with `percentageComplete="100"` in the attribute list of the task),
- removes all further efforts of not done tasks, 
- and writes the remaining tasks in another `.tsk` file.

The output file can be opened in the TaskCoach for further use.

```
python taskcoach_manager.py -c <input_fn.tsk> [<output_fn.tsk>]
```

# Progress

## Todos

* check efforts with overlapping tracked time 
* make sure the user doesn't overwrite the original file
* get description into summary
* check daily non-tracked time slots 
* consider also tasks without any category in the summary


## Versions

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

