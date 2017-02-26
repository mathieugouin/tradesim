#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      temp
#
# Created:     21/02/2013
# Copyright:   (c) temp 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# http://pybrain.org/docs/quickstart/dataset.html
# http://pybrain.org/docs/api/datasets/superviseddataset.html
# http://pybrain.org/docs/tutorial/datasets.html


# NN with pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.structure import LinearLayer
#from pybrain.structure import SoftmaxLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

#net = buildNetwork(2, 3, 1, hiddenclass=TanhLayer, outclass=SoftmaxLayer, bias=True)
net = buildNetwork(2, 12, 1, bias=True, hiddenclass=TanhLayer)
net.modules

ds = SupervisedDataSet(2, 1)

# XOR data
for i in xrange(5):
    ds.addSample([0, 0], [0])
    ds.addSample([0, 1], [1])
    ds.addSample([1, 0], [1])
    ds.addSample([1, 1], [0])

print ds['input']
print ds['target']

print len(ds)

for inpt, target in ds:
    print "input:", inpt, " target:", target

print ds.getSample(0)
print ds.getSample(0)[0]
print ds.getSample(0)[1]

trainer = BackpropTrainer(net, ds)
trainer.trainUntilConvergence(validationProportion=.25) # TBD what?

print net.activate(ds.getSample(0)[0])

def main():
    pass

if __name__ == '__main__':
    main()
