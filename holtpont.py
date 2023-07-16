#!/usr/bin/env python3

resources = {}
tasks = {}
task_list = []
result = [] # kimenet: [(Task, művelet sorszáma, Resource), (...), ...]


# containing(tasks, resource) visszaadja, hogy melyik taszké a resource
# containing(resources, task) visszaadja, hogy melyik resourcera vár a taszk
def containing(container, obj_to_be_contained):
    for o in container.values():
        if obj_to_be_contained in o.neighbours:
            return o
    return None

# nagyon hatékonytalan, de legalább kevesebb állapotot kell tárolni, ami könnyebbség
def is_waiting(task):
    return containing(resources, task) != None
def is_used(resource):
    return containing(tasks, resource) != None

def prall():
    print("állapot:")
    print("   ","\n    ".join(str(r) for r in resources.values()))
    print("   ","\n    ".join(str(r) for r in tasks.values()))
    print("allvege")

def has_circle(fromm, searchable): # searchable egy üres lista legyen nem rekurzív híváskor
    if fromm in searchable:
        return True
    searchable.append(fromm)
    for n in fromm.neighbours:
        if has_circle(n, searchable):
            return True
    return False

class Resource:
    def __init__(self, name):
        self.name = name
        self.neighbours = [] # taszkok, akik várnak rá, fifo
    
    def freed(self):
        if self.neighbours:
            task = self.neighbours.pop(0)
            task.neighbours.append(self)
    
    def __repr__(self):
        return f"Resource({self.name},{[n.name for n in self.neighbours]},{is_used(self)})"


class Task:
    def __init__(self, args):
        args = args.split(",")
        self.name = args[0]
        self.operations = args[1:] # ahogy telik az idő, folyamatosan fogy
        for op in self.operations:
            if op != "0" and op[1:] not in resources:
                resources[op[1:]] = Resource(op[1:])
        self.neighbours = [] # erőforrások, akiket foglal, amilyen sorrendben foglal
        self.current_op = 0 # ahogy telik az idő, folyamatosan nő
    
    def step(self):
        if is_waiting(self):
            return
        if not self.operations: # ha végeztünk
            for resource in self.neighbours:
                resource.freed()
            self.neighbours = [] # kiürítés
            return
        op = self.operations.pop(0)
        self.current_op += 1
        if op == "0":
            return
        resource = resources[op[1:]]
        if op[0] == "-":
            if resource in self.neighbours:
                self.neighbours.remove(resource)
                resource.freed()
            return
        if op[0] == "+":
            if is_used(resource):
                resource.neighbours.append(self)
            else: # ha megkaptuk
                self.neighbours.append(resource)
            if (has_circle(self, [])):
                result.append((self, self.current_op, resource))
                #print("Holtpont elkerülve!", result[-1])
                resource.neighbours.pop(-1) # megszüntetjük a kört

    def __repr__(self):
        return f"Task({self.name},{self.operations},{[n.name for n in self.neighbours]},{self.current_op},{is_waiting(self)})"
    
try:
    while True:
        line = input()
        if line:
            task = Task(line)
            tasks[line.split(",")[0]] = task
            task_list.append(task)
except EOFError:
    pass

i = 0
while any(task.operations for task in task_list):
    i += 1
    if i > 3000: # végtelen ciklus ellen ideiglenesen
        break
    task = task_list.pop(0)
    #print("taszkfut:   ", task)
    task.step()
    #print("taszkleftt: ", task)
    task_list.append(task)
    #prall()
    
print("\n".join(f"{dl[0].name},{dl[1]},{dl[2].name}" for dl in result))
