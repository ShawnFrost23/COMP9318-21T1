## import modules here 
import pandas as pd
import numpy as np
import helper


################### Question 1 ###################

def checkAllInArray(array1, arrayOrg):
    
    arrayLen = len(array1) - 1
    while arrayLen >= 0:
        if array1[arrayLen] != 'ALL':
            array1[arrayLen] = 'ALL'
            return True
        else:
            array1[arrayLen] = arrayOrg[arrayLen]

        arrayLen -= 1

    return False


def singleTupleOptim(df):

    value = df.iloc[0,-1]
    
    dimensionLessArray = df.iloc[0, : -1]
    arrayOrg = np.copy(dimensionLessArray.values)
    array1 = np.zeros(df.values.shape[1] - 1, dtype = object)

    for i in range(len(array1)):
        array1[i] = arrayOrg[i]

    returnValue = []
    returnValue.append(df.values[0])

    while checkAllInArray(array1, arrayOrg):       
        
        rowArray = np.zeros(df.values.shape[1], dtype = object)

        for j in range(len(array1)):
            rowArray[j] = array1[j]

        rowArray[-1] = value
        returnValue.append(rowArray)

    return returnValue


def buc_rec_optimized(df):
    
    emptyDataFrame = pd.DataFrame(columns = df.columns)
    dictionary = {}

    for i in range(df.values.shape[0]):
        rows = singleTupleOptim(df.iloc[i:i+1, :])
        
        for element in rows:
            value = element[-1]
            key = ""

            for j in range(len(element) - 1):
                key += str(element[j])
                if j < len(element) - 2:
                    key += '~'
            
            if key in dictionary:
                dictionary[key] += int(value)
            else:
                dictionary[key] = int(value)

    index = 0
    for key, value in sorted(dictionary.items()):

        listString = key.split('~')
        newElementForRow = np.zeros((len(listString) + 1), dtype = object)
        
        for i in range(len(listString)):
                newElementForRow[i] = listString[i]

        newElementForRow[-1] = value

        emptyDataFrame.loc[index] = newElementForRow
        index += 1
            
    return emptyDataFrame


