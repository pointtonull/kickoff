#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import xml.etree.cElementTree as et

import numpy as np

PRIORITIES = {
    "veryhigh": 1.,
    "high": 2.,
    "medium": 3.,
    "low": 4.,
    "verylow": 5.,
}

if __name__ == '__main__':

    
    tree = et.parse(open(".todo"))

    events = []

    for note in tree.findall('./note'):
        time = note.get("time")
        priority = note.get("priority")
        priority = PRIORITIES[priority]
        comment = next(note.itertext()).strip()
        events.append((time, 
            {"type": "added",
             "priority": priority,
             "comment": comment,
             "tree": note}
        ))

    for note in tree.findall("./note[@done]"):
        time = note.get("done")
        taskid = note.get("time")
        comment = note.find("comment")
        if comment != None:
            comment = "".join(comment.itertext()).strip()
        else:
            comment = ""
        events.append((time, 
            {"type": "done",
             "taskid": taskid,
             "comment": comment,
             "tree": note}
        ))

    notes = []
    tasksids = []
    priorities = np.array([])
    for time, event in sorted(events):
        if event["type"] == "added":
            notes.append(event["comment"])
            tasksids.append(time)
            priorities = np.append(priorities, event["priority"])
        elif event["type"] == "done":
            taskpos = tasksids.index(event["taskid"])
            del(notes[taskpos])
            del(tasksids[taskpos])
            priority = priorities[taskpos]
            np.delete(priorities, taskpos)
            priorities -= priority / priorities.sum()

    result = sorted(zip(priorities, notes))

    for tuple in result:
        print tuple

#    import IPython
#    IPython.embed()
    
