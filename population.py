from individual import *
import random 

class Population:
    
    mutation_rate = 0.1

    def __init__(self, size):
        self.size = size
        self.individuals = []
        self.selected = []
        self.offspring = []
        for i in range(size):
            self.individuals.append(Individual())
    
    def evaluate(self):
        for i in self.individuals:
            i.evaluate()
    
    def select(self):
        selecting = True
        self.selected.clear()
        while selecting:
            for i in self.individuals:
                if random.random() < i.accuracy:
                    self.selected.append(i)                    
                if len(self.selected) == self.size:
                    selecting = False
                    break
    
    def crossover(self):
        for i in range(self.size):
            i1 = random.randint(0,self.size-1)
            i2 = random.randint(0,self.size-1)
            self.offspring.append(Individual(self.selected[i1].dna, self.selected[i2].dna))

    def mutate(self):
        for i in self.offspring:
            if random.random() < self.mutation_rate:
                i1 = random.randint(0,7)
                i2 = random.randint(0,7)
                i.dna[i1] = i2
    
    def getBestIndividual(self):
        bi = self.individuals[0]
        bf = bi.fitness
        for i in self.individuals:
            if i.fitness > bf:
                bi = i
                bf = bi.fitness

        return bi

