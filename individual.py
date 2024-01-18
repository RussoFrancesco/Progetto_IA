import random
import math

class Individual:

    def __init__(self, dna1=None, dna2=None):

        self.dna = [None] * 4
        self.accuracy = 0
        self.learning_time = 0
        self.fitness = 0.

        if dna1 != None and dna2 != None:
            cross = random.randint(0, 2)
            self.dna = dna1[:cross] + dna2[cross:]
            self.dna[3] = self.dna[0]*self.dna[1]
        elif dna1 != None:
            self.dna = dna1.copy()
        else:    
            self.randomize()
    
    def randomize(self):
       self.dna[0] = random.randint(2, 10) #n strati convoluzionali
       self.dna[1] = random.randint(8, 32) #dim strati convoluzionali
       self.dna[2] = random.randint(2, 5) #n strati densi
       self.dna[3] = self.dna[0]*self.dna[1] #dim strati densi

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy
    
    def set_time(self, time):
        self.learning_time = time
    
    def evaluate(self):
        self.fitness = self.accuracy / math.log10(self.learning_time)


    