import csv

def recupera_valori_fitness(file_csv):
    with open(file_csv, 'r') as csvfile:
        lettore_csv = csv.DictReader(csvfile)
        
        min_fit = 1
        max_fit = 0
        for row in lettore_csv:
            if float(row['fitness']) < min_fit:
                min_fit = float(row['fitness'])
            elif float(row['fitness']) > max_fit:
                max_fit = min_fit
        print(min_fit)
        print(max_fit)
        for row in lettore_csv:
            print((float(row['fitness']) - min_fit) / (max_fit - min_fit))

# Sostituisci 'nome_del_tuo_file.csv' con il percorso e il nome effettivi del tuo file CSV
file_csv = 'individui_result_2.csv'
recupera_valori_fitness(file_csv)




