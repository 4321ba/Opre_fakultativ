#!/usr/bin/env python3

class Frame:
    def __init__(self, name, page):
        self.name = name
        self.freeze = 4
        self.used = False
        self.page = page

line = input()
while not line:
    line = input()
pages = [abs(int(p)) for p in line.split(",")]
#print(pages)

fifo = [] # [-1] arrived last, so we want to pop [0]

res = [] # list of characters, in the order that pages are loaded into frames

for page in pages:
    if any(f.page == page for f in fifo):
        frame = [f for f in fifo if f.page == page][0]
        frame.freeze = 0
        frame.used = True
        res.append('-')
    elif len(fifo) < 3:
        fifo.append(Frame(['A', 'B', 'C'][len(fifo)], page))
        res.append(fifo[-1].name)
    elif all(f.freeze > 0 for f in fifo):
        res.append('*')
    else:
        idx = 0
        while fifo[idx].used or fifo[idx].freeze > 0:
            if (fifo[idx].used):
                fifo.append(fifo.pop(idx))
                fifo[-1].used = False
            elif fifo[idx].freeze > 0:
                idx += 1
        frame = fifo.pop(idx)
        res.append(frame.name)
        frame.freeze = 4
        frame.page = page
        frame.used = False
        fifo.append(frame)
        
    for frame in fifo:
        if frame.freeze > 0:
            frame.freeze -= 1

#print(res)
print("".join(res))
print(len(res) - res.count('-'))
