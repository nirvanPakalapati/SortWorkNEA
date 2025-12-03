import allocateTime
import queue
import eventCreator
import quickstart

class FeedbackQueue:

    def __init__(self, processes):
#Array of process objects
        self.processes = processes


    #each of these should have public access
    class Process:
        def __init__(self, name, burstTime, type, priority):
            self.name = name
            self.burstTime = burstTime
            self.type = type
            self.priority = priority

    

#creates the multilevel feedback queue        
    def mlfq(processes):
        #3 levels of queues
        queues = [[], [], []]
        timeQuantum = 2

        for process in processes:
            index = process.priority -1
            queues[index].append(process)

#rotates between each one of the queues
        for i in range(0,3):
            currentTime = 0
            processedProcesses = 0

            #until all processes are completed2
            while processedProcesses < len(processes):

                for process in processes:
                    if 0 < process.burstTime <= timeQuantum:
                        process.burstTime = 0
                        queue.enqueue(queues[i], process)
                        processedProcesses +=1 
                        currentTime += process.burstTime

                    elif process.burstTime > timeQuantum:
                        process.burstTime -= timeQuantum
                        currentTime += timeQuantum

                for process in queues[i]:
                    if process.burstTime >0:
                        queue.enqueue(queues[i+1], process)

    
    
    def decideTime(processes):

        for process in processes:
            if process.type == "test revision":
                process.priority = 3
                process.burstTime = 1

            elif process.type == "hw":
                process.priority = 2
            #burst time will be set in initialisation of object
            
            elif process.type == "consolidation":
                process.priority = 1
                process.burstTime = 0.5
    
    def createProcesses():
        quickstart.main()
        





def main():
    queue = FeedbackQueue()

main()