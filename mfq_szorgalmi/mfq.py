#!/usr/bin/env python3

class Task:
    def __init__(self, args):
        args = args.split(",")
        self.name = args[0] # neve, egy karakteres
        self.prio = 2 # prioritás: legmagasabb szinten kezd
        self.start = int(args[1]) # második argumentum az indulási idő
        # az alábbi listák és elemeik a taszk futása során csökkennek
        # a lista elején levő elem az éppen aktuális
        # azt, hogy a taszk éppen cpura vár, vagy fut, vagy io-zik, azt az mondja meg,
        # hogy melyik (lentebb deklarált) listában van benne
        self.cpu_times = [] # a hátralevő cpu-löketek listája
        self.io_times = [] # a hátralevő io-löketek listája
        for i, time_slice in enumerate(args[2:]):
            # beletesszük az argumentumokat a tömbökbe, felváltva
            [self.cpu_times, self.io_times][i % 2].append(int(time_slice))
    
    def upgrade(self):
        self.prio = min(self.prio + 1, 2)
    def downgrade(self):
        self.prio = max(self.prio - 1, 0)

tasks = []
try:
    while True:
        line = input()
        if line:
            tasks.append(Task(line))
except EOFError:
    pass

tasks.sort(key = lambda t: (t.start, t.name)) # abban a sorrendben, ahogy belépniük kell
# a tasks-ban lesznek azok a taszkok, akik még nem indultak el

# a következő sorokban a [0] index a legelső elem, és sor végére [-1] érkeznek az új taszkok
prio2_queue = [] # a 2-es prioritási szint (legmagasabb) várakozási sora
prio1_queue = [] # az 1-es prioritási szint várakozási sora
prio0_queue = [] # a 0-sé
queues = [prio0_queue, prio1_queue, prio2_queue] # az összes sor, prioritással lehet indexelni
io_tasks = [] # az io-ra várakozó taszkok listája

curr = None # currently running: az a taszk, amelyik éppen fut
timeslice = -1 # az éppen futó taszk hátralevő időszelete az aktuális prioritási szinten, -1 ha curr==None
NEW_SLICES = [2**10, 4, 2] # újonnan jövő taszkok időszelete, valami kellően nagy szám az alacsony prioritáshoz

# egy még futó taszk egy időpillanatban a tasks, prio2_queue, prio1_queue, prio0_queue, io_tasks listák,
# illetve a currently_running változó közül pontosan egynek lesz az eleme

result = [] # tuple-ök listája, amivel az eredményt lehet majd kiírni: [(taszknév, prio), (...), ...] formában
# minden eltelt időpillanatban íródik bele valami, szóval len(result) == eltelt idő

while tasks or prio2_queue or prio1_queue or prio0_queue or io_tasks or curr:
    
    # beérkeznek az ebben az időpillanatban érkező taszkok
    while tasks and tasks[0].start <= len(result):
        task = tasks.pop(0)
        queues[task.prio].append(task) # megfelelő sorba betétel
    
    # io-ról visszatérnek a taszkok (iterálás közben nehéz törölni)
    visszatero = [task for task in io_tasks if task.io_times[0] == 0]
    io_tasks = [task for task in io_tasks if task.io_times[0] != 0]
    for task in visszatero:
        if task.cpu_times: # ha nincs cpu hátra, bár az helytelen bemenet volna, de akkor befejezzük a taszkot
            task.io_times.pop(0)
            queues[task.prio].append(task)
                
    # ha éppen befejeződött curr-nak az aktuális cpu-lökete, akkor vagy befejeződik, vagy lelép io-ra
    if curr != None and curr.cpu_times[0] == 0:
        if curr.io_times:
            curr.cpu_times.pop(0)
            io_tasks.append(curr)
            if timeslice != 0:
                curr.upgrade()
        curr = None
        timeslice = -1
    
    # ha épp lejár az időszelete, akkor downgrade-elődik
    if timeslice == 0:
        curr.downgrade()
        queues[curr.prio].append(curr)
        curr = None
        timeslice = -1
    
    # ha van magasabb prioritású várakozó taszk, akkor kirúgjuk az épp futót
    if curr and ((prio2_queue and curr.prio < 2) or (prio1_queue and curr.prio < 1)):
        queues[curr.prio].append(curr)
        curr = None
        timeslice = -1
    
    # ha új taszkra van szükség (beletartozik az is, ha az előbb kirúgott taszk helyére teszünk újat)
    if curr == None:
        if prio2_queue:
            curr = prio2_queue.pop(0)
            timeslice = NEW_SLICES[2]
        elif prio1_queue:
            curr = prio1_queue.pop(0)
            timeslice = NEW_SLICES[1]
        elif prio0_queue:
            curr = prio0_queue.pop(0)
            timeslice = NEW_SLICES[0]
    
    # kiválasztott taszk könyvelése
    result.append((curr.name, curr.prio) if curr != None else ("X", 0))
    
    # idő telése
    for task in io_tasks:
        task.io_times[0] -= 1
    if curr != None:
        curr.cpu_times[0] -= 1
        timeslice -= 1

# ha az utolsó elem az idle taszk, akkor azt nem akarjuk kiírni
if result and result[-1][0] == "X":
    result.pop(-1)

# számok kiírása
print("".join(str(i+1)[-1] for i in range(len(result))))
# taszkok kiírása
print("".join(i[0] if i[1] == 2 else " " for i in result))
print("".join(i[0] if i[1] == 1 else " " for i in result))
print("".join(i[0] if i[1] == 0 else " " for i in result))
