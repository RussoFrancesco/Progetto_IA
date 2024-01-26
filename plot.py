import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

reader = csv.DictReader(open("individui_gene_result.csv"))
dict_individui = {}

for row in reader:
    generazione = row['generazione']

    if generazione not in dict_individui.keys():
        dict_individui[generazione] = float(row['fitness'])
    elif dict_individui[generazione] < float(row['fitness']):
        dict_individui[generazione] = (float(row['fitness']))


generazioni = list(dict_individui.keys())

plt.figure(figsize=(8, 5))
plt.plot(generazioni, list(dict_individui.values()), label='Valori massimi di fitness')
plt.legend()
plt.title('Fitness massima per generazione')
plt.xlabel('Generazione')
plt.ylabel('Fitness')
plt.show()