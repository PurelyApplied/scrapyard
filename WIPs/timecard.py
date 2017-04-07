#!/usr/bin/python3
import os
import pickle
import subprocess

_cache = ".timecard"
def main(*args):
    T = {}
    try:
        T = pickle.load(open(_cache, "rb"))
    except:
        print("Could not open timecard.  Creating new.")
        pickle.dump(T, open(_cache, "wb"))

    if len(args) == 0:
        print_clocks(T)
        return T
        
    if len(args) == 1:
        args = args[0].split()

    i = 0
    print(args)
    while i < len(args):
        cmd = args[i].lower()
        print("command =", cmd)

        if cmd == "start":
            i += 1
            tag = args[i]
            print("tag = ", tag)
            C = T.get(tag, Clock(tag))
            print("Clock fetched")
            C.start()
            print("Clock started")
            if not C.name in T:
                T[C.name] = C

        if cmd == "stop":
            i += 1
            tag = args[i]
            C = T[tag]
            C.stop()
        i += 1
    
    print("Exiting...")
    end = False
    while not end:
        try:
            print("Dumping clocks")
            pickle.dump(T, open(_cache, "wb"))
            end = True
        except:
            end = not "y" in input("Could not write timecards; try again?  (y/n) >> ")
    return T
    
def print_clocks(T):
    if len(T) == 0:
        print("No clocks to print.")
        return
    tag_len = max([len(t.name) for t in T.values()])
    fstring = "{:" + str(tag_len+2) + "s} : Active = {:5s} ; Time = {}"
    for k,t in sorted(T.items()):
        print(fstring.format(t.name, str(t.active), t.time))

def getTime():
    proc = subprocess.Popen('date +"%y-%m-%d-%H-%M-%S"', stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    now_clock = [int(i) for i in out.decode("utf-8").split("-")]
    return now_clock

class Clock:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.t_start = None
        self.time = [0]*6

    def start(self):
        assert not self.active, "{} already active!".format(self)
        self.active = True
        self.t_start = getTime()
        return self # allows `C = Clock(tag).start()` call

    def stop(self):
        assert self.active, "{} not active!".format(self)
        self.active = False
        now = getTime()
        for i in range(len(self.time)):
            self.time[i] += now[i] - self.t_start[i]
        self.carry_clocks()

    def adjust(self, timer):
        assert len(timer) == len(self.time), "Adjustments must be made with array of length {}".format(len(self.time))
        for i in range(len(self.time)):
            self.time[i] += timer[i] - self.t_start[i]
        self.carry_clocks()
        
    def carry_clocks(self):
        '''Carry the ones, etc'''
        pass

    def __repr__(self):
        return '<Clock "{}"{}>'.format(self.name, "; active" if self.active else "")
 
