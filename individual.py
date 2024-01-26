import random
import math
import os
import csv

class Individual:

    def __init__(self, dna1=None, dna2=None):

        self.dna = [None] * 4 #[n_conv, dim_conv, n_dense, dim_dense]
        self.accuracy = 0
        self.learning_time = 0
        self.fitness = 0.   #fitness calcolata come: accuracy/log10(learning_time)
        self.norm_fitness = 0 #fitness normalizzata sulla generazione

        if dna1 != None and dna2 != None:
            #caso di crossover
            cross = random.randint(1, len(self.dna)-1)
            self.dna = dna1[:cross] + dna2[cross:]
        elif dna1 != None:
            #copia del dna padre
            self.dna = dna1.copy()
        else:    
            self.randomize()
    
    def randomize(self):
       self.dna[0] = random.randint(2, 10) #n strati convoluzionali
       self.dna[1] = random.randint(8, 32) #dim strati convoluzionali
       self.dna[2] = random.randint(1, 5) #n strati densi
       self.dna[3] = random.randint(16, 320) #dim strati densi

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy
    
    def set_time(self, time):
        self.learning_time = time
    
    def evaluate(self):
        self.fitness = self.accuracy / math.log10(self.learning_time)
    
    def write_on_file_gene(self, filename, generazione):
        # Verifica se il file esiste già
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ['generazione', 'dna']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Scrivi gli header solo se il file è vuoto
            if not file_exists:
                writer.writeheader()

            #scrivo la generazione e il dna dell'individuo
            writer.writerow({'generazione': generazione, 'dna': self.dna})

            file.close()

    def write_on_file_result(self, filename, generazione):
        # Verifica se il file esiste già
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ['generazione', 'dna', 'tempo', 'accuracy', 'fitness']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Scrivi gli header solo se il file è vuoto
            if not file_exists:
                writer.writeheader()

            #scrivo la generazione, il dna, il tempo di addestramento, l'accuracy e la fitness
            writer.writerow({'generazione': generazione, 'dna': self.dna, 'tempo': self.learning_time, 
                             'accuracy': self.accuracy, 'fitness': self.fitness})
            
            file.close()

    def write_on_file_result_norm(self, filename, generazione):
        # Verifica se il file esiste già
        file_exists = os.path.isfile(filename)

        with open(filename, mode='a', newline='') as file:
            fieldnames = ['generazione', 'dna', 'tempo', 'accuracy', 'fitness', 'fitness_normalizzata']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Scrivi gli header solo se il file è vuoto
            if not file_exists:
                writer.writeheader()

            #scrivo la generazione, il dna, il tempo di addestramento, l'accuracy, la fitness e la fitness normalizzata
            writer.writerow({'generazione': generazione, 'dna': self.dna, 'tempo': self.learning_time, 
                             'accuracy': self.accuracy, 'fitness': self.fitness, 'fitness_normalizzata': self.norm_fitness})
            
            file.close()


    