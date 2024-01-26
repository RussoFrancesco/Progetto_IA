from population import *
from individual import *
import keras
from keras.models import Sequential
from keras import datasets, layers
from keras.utils import to_categorical
import time
import gc

#funzione per la creazione del modello
def create_model(n_conv, dim_conv, n_dense, dim_dense, model):
    for i in range(1, n_conv+1):
        if i == 1:
            #il primo strato convoluzionale ha l'argomento input_shape
            model.add(layers.Conv2D(dim_conv, (3,3), padding='same', activation='relu', input_shape=(32,32,3)))
        else:
            #dal secondo strato in poi aumento la dimensione dello strato convoluzionale
            model.add(layers.Conv2D(dim_conv*i, (3,3), padding='same', activation='relu'))

        #dopo ogni strato convoluzionale aggiungo uno strato BatchNormalization
        model.add(layers.BatchNormalization())

        #ogni due strati convoluzionali aggiungo uno strato di maxpooling e uno di dropout
        if i % 2 == 0:
            model.add(layers.MaxPooling2D(pool_size=(2,2)))
            model.add(layers.Dropout(0.5))
    
    #strato flatten prima degli strati densi
    model.add(layers.Flatten())
    
    for j in range(0, n_dense):
        model.add(layers.Dense(dim_dense, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.5))
    
    #strato denso di output
    model.add(layers.Dense(num_classes, activation='softmax'))

#funzione per addestrare e valutare il modello
def training_and_evaluate(model):
    #compilazione del modello
    model.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])

    #addestramento del modello e misurazione del tempo di addestramento
    start_time = time.time()
    history = model.fit(train_images, train_labels, epochs=7, verbose=2)
    end_time = time.time() - start_time

    #valutazione del modello sul test set
    results = model.evaluate(test_images, test_labels)
    print("test loss, test acc:", results)

    #ritorno della precisione misurata e del tempo di addestramento
    return results[1], end_time
    

#scarico il dataset
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

#dichiaro le label del dataset
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

#converto le immagini in float
train_images = train_images.astype('float32')
test_images = test_images.astype('float32')
 
#normalizzazione dell'immagine
train_images = train_images / 255
test_images = test_images / 255 

#one-hot encoding per le label
num_classes = 10
train_labels = to_categorical(train_labels, num_classes)
test_labels = to_categorical(test_labels, num_classes)

#filename se si vuole addestrare individui da file
filename = "individui_gene.csv"

#dichiarazione della popolazione con la size
pop = Population(20, filename)

#flag utili all'esecuzione
writing = False
running = True

while running:
    #se la generazione è 0 (quindi se è stata appena creata), la aumento a 1
    if pop.generation == 0:
        pop.add_generation()
    
    #se writing è False, vuol dire che si sta leggendo da file e non si riscrivono gli individui
    if writing is not False:
        #scrivo i geni della generazione sul file, utile nel caso si debba fermare l'addestramento per non perdere i geni
        for individual in pop.individuals:
            individual.write_on_file_gene("individui_gene.csv", pop.generation)
    writing = True

    #ciclo per l'addestramento e valutazione dell'individuo
    for individual in pop.individuals:
        #clear_session serve a rilasciare lo stato globale di keras, serve quando si creano modelli in loop 
        keras.backend.clear_session()

        #dichiarazione del modello
        model = Sequential()

        #aggiunta degli strati in base al dna dell'individuo
        create_model(individual.dna[0], individual.dna[1], individual.dna[2], individual.dna[3], model)

        #addestramento e valutazione del modello
        accuracy, training_time = training_and_evaluate(model)

        #setto le variabili dell'individuo e calcolo la fitness
        individual.set_accuracy(accuracy)
        individual.set_time(training_time)
        individual.evaluate()

        #scrivo le caratteristiche dell'individuo su file
        individual.write_on_file_result("individui_gene_result.csv", pop.generation)

        #libero per quanto possibile la memoria
        del model
        keras.backend.clear_session()
        gc.collect()

    #azioni di selezione, crossover e mutazione della popolazione
    pop.select()
    pop.crossover()
    pop.mutate()

    #sostituisco la vecchia generazione con quella nuova
    pop.individuals = pop.offspring

    #se un individuo ha superato la fitness soglia fermo l'esecuzione
    if pop.getBestIndividual().fitness >= 0.32:
        running = False
    
    #incremento la generazione
    pop.add_generation()

