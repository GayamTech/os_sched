#!/usr/bin/env python

class Scheduler(object):

    def __init__(self):
        self.QUANTUM = 3
        self.programs = {
            "A": [0, "B", 0, "B", 0,0,"B",0],
            "B": [0,"C", 0,"C",0,0],
            "C": [0]*4,
        }
        self.ready_queue = [
            {"pid": 1, "program" : "A", "last_step": -1, "ppid": 0},
            {"pid": 2, "program" : "B", "last_step": -1, "ppid": 0},
        ]
        self.completed = []
        self.last_pid = 2
        self.tick = 0
        self.MAX_TICKS = 1000
        self.running_process = None #
        self.curr_ticks_used = 0

    def schedule_next(self):
        self.curr_ticks_used = 0
        if self.running_process:
            self.ready_queue.append(self.running_process)
        self.running_process = self.get_next_from_ready()
        print("scheduling {}".format(self.running_process))

    def get_next_from_ready(self):
        next_proc = self.ready_queue[0]
        self.ready_queue = self.ready_queue[1:]
        return next_proc

    def fork(self, program_name):
        self.last_pid += 1
        proc = {"pid": self.last_pid, "program": program_name, "last_step": -1, "ppid": self.running_process["pid"]}
        print(" ==> Forking {}\n".format(proc))
        self.ready_queue.append(proc)

    def execute(self):
        pid = self.running_process["pid"]
        program = self.running_process["program"]
        last_step = self.running_process["last_step"]
        self.running_process["last_step"] += 1
        program_code = self.programs[program]
        if len(program_code) > (last_step+1):
            next_instruction = program_code[last_step + 1]
            if next_instruction:
                print("Tick {}: Forking {}.  pid {}, program {}".format(self.tick,  next_instruction, pid, program,))
                self.fork(next_instruction)
            else:
                print("Tick {}: Running Logic pid {}, program {}".format(self.tick, pid, program))
            return False
        else:
            print("Completed pid {}, program {}".format(self.tick, pid, program))
            self.completed.append(self.running_process)
            self.running_process = None
            if len(self.ready_queue) > 0:
                self.schedule_next()
                if self.running_process:
                    return self.execute()
            return True

    def print_state(self):
        def fmt_ready_queue(q):
            return "\n".join([str(i) for i in q])

        print ("========\nTick {}\nReady queue \n{}\n last_pid:{}\nrunning_process:{}\ncurr_ticks_used:{}\n\n".format(
            self.tick, fmt_ready_queue(self.ready_queue), self.last_pid, self.running_process, self.curr_ticks_used))

    def curr_process_still_going(self):
        if not self.running_process:
            return False
        program_name = self.running_process['program']
        code = self.programs[program_name]
        return self.running_process['last_step'] <  len(code)

    def run(self):
        while len(self.ready_queue) > 0 or self.curr_process_still_going():
            assert self.tick < self.MAX_TICKS
            self.tick += 1
            self.print_state()
            if self.running_process is None:
                self.schedule_next()
            else:
                if self.curr_ticks_used >= self.QUANTUM:
                    self.schedule_next()

            # Execute the program
            completed = self.execute()
            self.curr_ticks_used += 1
            print("DBG: {}".format(len(self.ready_queue)))

        print ("\nCompleted:")
        for c in self.completed:
            print ("{}".format(c))

S = Scheduler()
S.run()
