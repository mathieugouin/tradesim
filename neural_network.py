# Back-Propagation Neural Networks
#
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

# To make print working for Python2/3
from __future__ import print_function

import math
import random
import numpy as np


# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a


def make_matrix(i, j, fill=0.0):
    """Make a matrix i x j, with init value fill."""
    return np.matrix(np.ones((i, j))) * fill


def sigmoid(x):
    """Our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)."""
    return math.tanh(x)


def dsigmoid(y):
    """Derivative of our sigmoid function, in terms of the output (i.e. y)."""
    return 1.0 - y**2


class NeuralNetwork(object):
    """Neural Network class."""

    def __init__(self, ni, nh, no):
        """Creates a Neural Network object with the number of input, hidden, and output nodes."""
        self.ni = ni + 1  # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = np.ones(self.ni)
        self.ah = np.ones(self.nh)
        self.ao = np.ones(self.no)

        # create weights
        self.wi = make_matrix(self.ni, self.nh)
        self.wo = make_matrix(self.nh, self.no)
        # set them to random values
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i, j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j, k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = make_matrix(self.ni, self.nh)
        self.co = make_matrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.ni-1):
            # self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            summ = 0.0
            for i in range(self.ni):
                summ = summ + self.ai[i] * self.wi[i, j]
            self.ah[j] = sigmoid(summ)

        # output activations
        for k in range(self.no):
            summ = 0.0
            for j in range(self.nh):
                summ = summ + self.ah[j] * self.wo[j, k]
            self.ao[k] = sigmoid(summ)

        return self.ao[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j, k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j, k] = self.wo[j, k] + N*change + M*self.co[j, k]
                self.co[j, k] = change
                # print(N*change, M*self.co[j][k])

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i, j] = self.wi[i, j] + N*change + M*self.ci[i, j]
                self.ci[i, j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error

    def test(self, patterns):
        for p in patterns:
            print(p[0], '->', self.update(p[0]))

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print("")
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print('error %-14f' % error)


def _demo():
    # Teach network XOR function
    pat = [
        [[0, 0], [0]],
        [[0, 1], [1]],
        [[1, 0], [1]],
        [[1, 1], [0]]
    ]

    # create a network with two input, two hidden, and one output nodes
    n = NeuralNetwork(2, 5, 1)
    print("Training:")
    n.train(pat)
    print("Test:")
    n.test(pat)
    print("Info:")
    n.weights()


def _main():
    _demo()


if __name__ == '__main__':
    _main()
