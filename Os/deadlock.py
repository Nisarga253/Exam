class DeadlockDetector:
    def __init__(self, available, max_demand, allocation):
        self.available = available
        self.max_demand = max_demand
        self.allocation = allocation
        self.need = self.calculate_need()

    def calculate_need(self):
        need = []
        for i in range(len(self.max_demand)):
            need.append([self.max_demand[i][j] - self.allocation[i][j] for j in range(len(self.available))])
        return need

    def is_safe(self):
        work = self.available[:]
        finish = [False] * len(self.allocation)
        safe_sequence = []

        while len(safe_sequence) < len(self.allocation):
            allocated = False
            for i in range(len(self.allocation)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(self.available))):
                    for j in range(len(self.available)):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated = True
            if not allocated:
                break

        return len(safe_sequence) == len(self.allocation), safe_sequence

    def detect_and_recover(self):
        is_safe, safe_sequence = self.is_safe()
        if is_safe:
            print("System is in a safe state.")
            print("Safe sequence:", safe_sequence)
        else:
            print("System is in a deadlock state. Initiating recovery...")
            self.recover()

    def recover(self):
        for i in range(len(self.allocation)):
            for j in range(len(self.available)):
                self.available[j] += self.allocation[i][j]
            print(f"Terminated process {i} to release resources.")
            is_safe, safe_sequence = self.is_safe()
            if is_safe:
                print("System recovered to a safe state.")
                print("New safe sequence:", safe_sequence)
                return
        print("Failed to recover from deadlock.")

available = [3, 3, 2]
max_demand = [
    [7, 5, 3],  
    [3, 2, 2],  
    [9, 0, 2],   
    [2, 2, 2],
    [4, 3, 3]]

allocation = [
    [0, 1, 0],  # P0
    [2, 0, 0],  # P1
    [3, 0, 2],  # P2
    [2, 1, 1],  # P3
    [0, 0, 2]]  # P4
detector = DeadlockDetector(available, max_demand, allocation)
detector.detect_and_recover()
