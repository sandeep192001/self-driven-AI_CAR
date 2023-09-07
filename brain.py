import tensorflow as tf
import numpy as np
import random

class NeuralNetwork:

    def __init__(self, input, hidden, output) :
        self.input = input
        self.hidden = hidden
        self.output = output
        self.model = self.create_neural_network()

    def create_neural_network(self):
        model = tf.keras.Sequential()

        model.add(tf.keras.layers.Dense(self.hidden, activation='relu', input_shape=[self.input]))
        model.add(tf.keras.layers.Dense(self.output, activation='sigmoid'))

        return model

        # self.model.compile('adam', loss=tf.losses.BinaryCrossentropy, metrics=['accuracy'])
        # self.model.summary()





    def mutate(self, rate):

        weights = self.model.get_weights()[:]
        mutated_weights = []

        for i in range(len(weights)):
            shape = weights[i].shape

            values = weights[i][:].flatten()

            for j in range(len(values)):
                if random.uniform(0, 1) < rate:
                    values[j] = random.uniform(-1, 1)

            values = np.reshape(values, shape)
            mutated_weights.append(values)

        self.model.set_weights(mutated_weights)


    def predict(self, X):
        return self.model.predict(np.array([X]))



def copy(brain):

    new_brain = NeuralNetwork(5, 8, 4)
    new_brain.model.set_weights(brain.model.get_weights()[:])

    return brain

