import random
import keras

class Individual:

    def __init__(self, dna1=None, dna2=None):

        self.dna = [None] * 4
        self.accuracy = 0
        self.learning_time = 0
        self.fitness = 0.

        if dna1 != None and dna2 != None:
            cross = random.randint(0, 3)
            self.dna = dna1[:cross] + dna2[cross:]
        elif dna1 != None:
            self.dna = dna1.copy()
        else:    
            self.randomize()
    
    def randomize(self):
       self.dna[0] = random.randint(1, 8) #n strati convoluzionali
       self.dna[1] = random.randint(32, 256) #dim strati convoluzionali
       self.dna[2] = random.randint(2, 5) #n strati densi
       self.dna[3] = random.randint(32, 256) #dim strati densi

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy
    
    def set_time(self, time):
        self.learning_time = time
    
    def set_fitness(self):
        self.fitness = ((self.accuracy*2)+(self.learning_time)/(self.accuracy+self.learning_time))/100


    