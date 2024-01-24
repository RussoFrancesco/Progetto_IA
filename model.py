from population import *
from individual import *
import keras
from keras.models import Sequential
from keras import datasets, layers
from keras.utils import to_categorical
import time
import gc


def create_model(n_conv, dim_conv, n_dense, dim_dense, model):
    for i in range(1, n_conv+1):
        if i == 1:
            model.add(layers.Conv2D(dim_conv, (3,3), padding='same', activation='relu', input_shape=(32,32,3)))
        else:
            model.add(layers.Conv2D(dim_conv*i, (3,3), padding='same', activation='relu'))
        model.add(layers.BatchNormalization())

        if i % 2 == 0:
            model.add(layers.MaxPooling2D(pool_size=(2,2)))
            model.add(layers.Dropout(0.5))
    
    model.add(layers.Flatten())
    
    for j in range(0, n_dense):
        model.add(layers.Dense(dim_dense, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.5))
    
    model.add(layers.Dense(num_classes, activation='softmax'))

def training_and_evaluate(model):
    model.compile(optimizer='adam', loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])

    start_time = time.time()
    history = model.fit(train_images, train_labels, epochs=7, verbose=2)
    end_time = time.time() - start_time
    results = model.evaluate(test_images, test_labels)
    print("test loss, test acc:", results)
    return results[1], end_time
    

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# Converting the pixels data to float type
train_images = train_images.astype('float32')
test_images = test_images.astype('float32')
 
# Standardizing (255 is the total number of pixels an image can have)
train_images = train_images / 255
test_images = test_images / 255 

# One hot encoding the target class (labels)
num_classes = 10
train_labels = to_categorical(train_labels, num_classes)
test_labels = to_categorical(test_labels, num_classes)

filename = "individui_gene.csv"
pop = Population(20, filename)
writing = False
running = True

while running:
    # Creating a sequential model and adding layers to it
    if pop.generation == 0:
        pop.add_generation()
    if writing is not False:
        for individual in pop.individuals:
            individual.write_on_file_gene("individui_gene.csv", pop.generation)
    writing = True
    for individual in pop.individuals:
        keras.backend.clear_session()
        model = Sequential()
        create_model(individual.dna[0], individual.dna[1], individual.dna[2], individual.dna[3], model)
        accuracy, training_time = training_and_evaluate(model)
        individual.set_accuracy(accuracy)
        individual.set_time(training_time)
        individual.evaluate()
        individual.write_on_file_result("individui_gene_result.csv", pop.generation)
        del model
        keras.backend.clear_session()
        gc.collect()

    pop.select()
    pop.crossover()
    pop.mutate()


    pop.individuals = pop.offspring

    if pop.getBestIndividual().fitness >= 0.32:
        running = False
    
    pop.add_generation()

    ''' 
    model.add(layers.Conv2D(32, (3,3), padding='same', activation='relu', input_shape=(32,32,3)))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(32, (3,3), padding='same', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Dropout(0.5))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(num_classes, activation='softmax'))    # num_classes = 10
    '''
    






