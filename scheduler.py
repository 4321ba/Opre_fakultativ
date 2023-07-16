#!/usr/bin/env python3

class Task:
    def __init__(self, args):
        args = args.split(",")
        self.name = args[0]
        self.prio = int(args[1])
        self.start = int(args[2])
        self.length = int(args[3])
        self.remaining = self.length
        self.waittime = 0

tasks = []
try:
    while True:
        line = input()
        if line:
            tasks.append(Task(line))
except EOFError:
    pass

tasks.sort(key = lambda t: (t.start, t.name)) # in the order they need to enter
remaining_tasks = tasks.copy() # tasks that are waiting to be started

rr_queue = []
srtf_pqueue = []

res = [] # list of tasks, in the order they are run, res[-1] was the one that was running last time

def last_valid():
    return res and res[-1] != None

def finished_current():
    return not last_valid() or res[-1].remaining == 0

while remaining_tasks or rr_queue or srtf_pqueue or not finished_current():
    while remaining_tasks and remaining_tasks[0].start <= len(res): # new tasks arriving, len(res) = time passed
        task = remaining_tasks.pop(0)
        [srtf_pqueue, rr_queue][task.prio].append(task) # we put it in the queue it needs to be in
        srtf_pqueue.sort(key = lambda t: t.remaining)
    
    # rr time expired, and currently running task has run an even number of times, and someone is waiting
    # should be noticed: if a task from the rr_queue enters the CPU, it will for sure be there, until it runs out,
    # or someone else is waiting in the queue after an even number of ticks passed
    if last_valid() and res[-1].prio == 1 and (res[-1].length - res[-1].remaining) % 2 == 0 and rr_queue: 
        if (res[-1].remaining > 0):
            remaining_tasks.insert(0, res[-1])
        res.append(rr_queue.pop(0))
    elif finished_current() and rr_queue:
        res.append(rr_queue.pop(0))
    elif finished_current() and srtf_pqueue:
        res.append(srtf_pqueue.pop(0))
    elif last_valid() and res[-1].prio == 0 and rr_queue: # someone is waiting inside rr, while srtf job is running
        if (res[-1].remaining > 0):
            remaining_tasks.insert(0, res[-1])
        res.append(rr_queue.pop(0))
    elif last_valid() and res[-1].prio == 0 and srtf_pqueue and srtf_pqueue[0].remaining < res[-1].remaining:
        if (res[-1].remaining > 0):
            remaining_tasks.insert(0, res[-1])
        res.append(srtf_pqueue.pop(0)) # new task came with less time remaining
    elif not finished_current(): # nothing happened, continuing the previous one
        res.append(res[-1])
    else:
        res.append(None)
    
    for task in tasks:
        if task.remaining != 0 and task.start < len(res) and task != res[-1]:
            task.waittime += 1
    
    if last_valid():
        res[-1].remaining -= 1

#print("(Szépen:", "".join(t.name if t != None else "X" for t in res), ")")
res.append(None)
print("".join(res[i].name for i in range(len(res)-1) if res[i] != None and res[i] != res[i+1]))
print(",".join(f"{t.name}:{t.waittime}" for t in tasks))
