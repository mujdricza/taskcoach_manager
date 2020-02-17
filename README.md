# taskcoach_manager
handling some steps in TaskCoach automatically -- e.g. clean the week plan

TaskCoach saves the tasks and efforts in an XML file with extension `.tsk`. 

This python script 
- takes a given `.tsk` file, 
- removes the done taks (marked with `percentageComplete="100"` in the attribute list),
- removes all further efforts of not done tasks, 
- and writes the remaining tasks in another `.tsk` file.

The output file can be opened in the TaskCoach for further use.

Use Python 3.4 (enum) or newer.

```
python3 task_cleaner.py <input tsk-file> <output tsk-file>
```

e.g.:
```
 python task_cleaner.py /mnt/d/emm/Verwaltung/Tasks/tasks_2020_0210-0214.tsk /mnt/d/emm/Verwaltung/Tasks/tasks_2020_0217-0220.tsk
```

Versions:
- 20200217: 
 * init
 * clearing done tasks and further efforts
 

Contact: Eva Mujdricza-Maydt (me.levelek@gmx.de)
