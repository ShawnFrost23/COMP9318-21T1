import numpy as np


def sigmoidFunction(x):
    sigmoid = 1/(1+np.exp(-x))
    return sigmoid
 
def logistic_regression(data, labels, weights, num_epochs, learning_rate): # do not change the heading of the function
    xVector = np.c_[np.ones(data.shape[0]), data]
    weightVector = weights
    labelVector = labels
    
    for counter in range(num_epochs):
        dotProduct = np.dot(xVector, weightVector)
        sigmoid = sigmoidFunction(dotProduct)
        gradientSlope = np.dot(xVector.T, (labelVector - sigmoid))
        weightVector += learning_rate * gradientSlope
     
    return weightVector
