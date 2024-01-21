from individual import *
import random 
import ast

class Population:
    
    mutation_rate = 0.2

    def __init__(self, size, file=None):
        self.size = size
        self.individuals = []
        self.selected = []
        self.offspring = []
        self.generation = 0
        if file is None:
            for i in range(size):
                self.individuals.append(Individual())
        else:
            with open(file, 'r') as f:
                righe = csv.DictReader(f)
                next(righe)
                lista_righe = list(righe)
                lista_righe = lista_righe[::-1]
                self.generation = lista_righe[0]["generazione"]
                if len(lista_righe)<size:
                    for i in range(len(lista_righe)):
                        self.individuals.append(Individual(ast.literal_eval(lista_righe[i]["dna"])))
                    for j in range(size-len(lista_righe)):
                        self.individuals.append(Individual())
                else:
                    for i in range(size):
                        self.individuals.append(Individual(ast.literal_eval(lista_righe[i]["dna"])))

    
    def select(self):
        self.normalize_fitness()
        selecting=True
        self.selected.clear()
        while selecting:
            for i in self.individuals:
                if random.random() < i.norm_fitness :
                    self.selected.append(i)
                if len(self.selected) == self.size:
                    selecting=False
                    break

    
    def crossover(self):
        for i in range(self.size):
            i1 = random.randint(0,self.size-1)
            i2 = random.randint(0,self.size-1)
            self.offspring.append(Individual(self.selected[i1].dna, self.selected[i2].dna))
        if len(self.offspring) > self.size:
            self.offspring = self.offspring[:self.size]

    def mutate(self):
        for i in self.offspring:
            if random.random() < self.mutation_rate:
                mutate_gene = random.randint(0, 3)
                if mutate_gene == 0:
                    i.dna[0] = random.randint(2, 10)
                    #i.dna[3] = i.dna[0]*i.dna[1]
                if mutate_gene == 1:
                    i.dna[1] = random.randint(8, 32)
                    #i.dna[3] = i.dna[0]*i.dna[1]
                if mutate_gene == 2:
                    i.dna[2] = random.randint(2, 5)
                if mutate_gene == 3:
                    i.dna[3] = random.randint(16, 320)

    
    def getBestIndividual(self):
        bi = self.individuals[0]
        bf = bi.fitness
        for i in self.individuals:
            if i.fitness > bf:
                bi = i
                bf = bi.fitness

        return bi

    def add_generation(self):
        self.generation = int(self.generation) + 1

    def normalize_fitness(self):
        min_fit = 1
        max_fit = 0
        for i in self.individuals:
            if i.fitness < min_fit:
                min_fit = i.fitness
            elif i.fitness > max_fit:
                max_fit = i.fitness
        for i in self.individuals:
            i.norm_fitness = (i.fitness - min_fit) / (max_fit - min_fit)
