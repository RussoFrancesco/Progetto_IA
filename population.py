from individual import *
import random 
import ast

class Population:
    
    mutation_rate = 0.1

    def __init__(self, size, file=None):
        self.size = size
        self.individuals = []
        self.selected = []
        self.offspring = []
        self.generation = 0
        if file is None:
            #se il file è None, creo una popolazione di individui casuali
            for i in range(size):
                self.individuals.append(Individual())
        else:
            with open(file, 'r') as f:
                righe = csv.DictReader(f)
                #salto l'header
                next(righe)

                #creo una lista delle righe e la inverto per recuperare gli ultimi individui
                lista_righe = list(righe)
                lista_righe = lista_righe[::-1]

                #recupero la generazione dell'ultimo individuo addestrato
                self.generation = lista_righe[0]["generazione"]

                #se la lunghezza delle righe è minore della size dichiarata, alcuni sono presi dal file e altri sono creati randomicamente
                if len(lista_righe)<size:
                    for i in range(len(lista_righe)):
                        #ast.literal_eval serve a trasformare il dna da stringa a lista
                        self.individuals.append(Individual(ast.literal_eval(lista_righe[i]["dna"])))
                    for j in range(size-len(lista_righe)):
                        self.individuals.append(Individual())
                else:
                    for i in range(size):
                        self.individuals.append(Individual(ast.literal_eval(lista_righe[i]["dna"])))

    #metodo per selezionare gli individui su cui effettuare il crossover
    def select(self):

        #normalizzo la fitness degli individui
        self.normalize_fitness()
        for i in self.individuals:
            i.write_on_file_result_norm("individui_result_norm.csv", self.generation)
        selecting=True
        self.selected.clear()

        #fino a quando la lunghezza della lista "selected" è minore della size, seleziono gli individui
        while selecting:
            for i in self.individuals:
                if random.random() < i.norm_fitness :
                    self.selected.append(i)
                if len(self.selected) == self.size:
                    selecting=False
                    break

    #metodo per effettuare il crossover
    def crossover(self):
        self.offspring.clear()
        for i in range(self.size):
            #seleziono due individui random e creo un terzo individuo il cui dna sarà un misto dei due genitori
            i1 = random.randint(0,self.size-1)
            i2 = random.randint(0,self.size-1)
            self.offspring.append(Individual(self.selected[i1].dna, self.selected[i2].dna))
        
    #metodo per la mutazione casuale
    def mutate(self):
        for i in self.offspring:
            if random.random() < self.mutation_rate:
                mutate_gene = random.randint(0, 3)
                if mutate_gene == 0:
                    i.dna[0] = random.randint(2, 10)
                if mutate_gene == 1:
                    i.dna[1] = random.randint(8, 32)
                if mutate_gene == 2:
                    i.dna[2] = random.randint(1, 5)
                if mutate_gene == 3:
                    i.dna[3] = random.randint(16, 320)

    #metodo per recuperare l'individuo con la fitness più alta
    def getBestIndividual(self):
        bi = self.individuals[0]
        bf = bi.fitness
        for i in self.individuals:
            if i.fitness > bf:
                bi = i
                bf = bi.fitness
        return bi

    #metodo per incrementare la generazione
    def add_generation(self):
        self.generation = int(self.generation) + 1

    #metodo per normalizzare la fitness degli indivisui
    def normalize_fitness(self):
        min_fit = 1
        max_fit = 0
        for i in self.individuals:
            if i.fitness < min_fit:
                min_fit = i.fitness
            elif i.fitness > max_fit:
                max_fit = i.fitness
        for i in self.individuals:
            #normalizzazione min-max
            i.norm_fitness = (i.fitness - min_fit) / (max_fit - min_fit)
