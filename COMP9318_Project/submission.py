import numpy as np
import pandas as pd
import math
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error


## Project-Part1
def predict_COVID_part1(svm_model, train_df, train_labels_df, past_cases_interval, past_weather_interval, test_feature):
    df2 = train_df[['max_temp', 'max_dew', 'max_humid', 'dailly_cases']]
    weatherFeatures = ['max_temp', 'max_dew', 'max_humid']
    weatherList = []
    for feature in weatherFeatures:
        for index in range(1, past_weather_interval + 1):
            newColName = feature + '-' + str(index)
            weatherList.append(newColName)
            df2[newColName] = np.nan
            for rowInd in range(30, len(df2)):
                df2.loc[rowInd, newColName] = df2.loc[rowInd - index, feature]
    
    casesCol = 'dailly_cases'
    casesList = []
    for index in range(1, past_cases_interval + 1):
        newColName = casesCol + '-' + str(index)
        casesList.append(newColName)
        df2[newColName] = np.nan
        for rowInd in range(30, len(df2)):
            df2.loc[rowInd, newColName] = int(df2.loc[rowInd - index, casesCol])
            
    x_train = df2.drop(['max_temp', 'max_dew', 'max_humid', 'dailly_cases'], 1)
    x_train = x_train.iloc[30:]
    
    y_train = train_labels_df.iloc[30:]
    y_train = y_train.drop(['day'], 1)
    dataColumns = weatherList + casesList
    dataList = {}
    print("Shape of x_train: ", x_train.shape)
    svm_model.fit(x_train, y_train)
    
    for data in dataColumns:
        dataList[data] = test_feature[data]
        
    newDataFrame = pd.DataFrame(dataList, index = [0])
    result = svm_model.predict(newDataFrame)
    return math.floor(result[0])


## Project-Part2

## Helper Function
def makePrediction(svrModelIncreasing, svrModelDecreasing, svrModelConstant, svrModelCombinedData, dataColumns, test_feature):    
    dataList = {}
    for data in dataColumns:
        dataList[data] = test_feature[data]
        
    newDataFrame = pd.DataFrame(dataList, index = [0])
    resultIncreasingModel = svrModelIncreasing.predict(newDataFrame)
    resultDecreasingModel = svrModelDecreasing.predict(newDataFrame)
    resultConstantModel = svrModelConstant.predict(newDataFrame)
    
    combinedAraay = [[resultIncreasingModel, resultDecreasingModel, resultConstantModel]]
    
    dataFrameForPrediction = pd.DataFrame(combinedAraay, columns=['increasingModelPrediction', 'decreasingModelPrediction', 'constantModelPrediction'])
    result = svrModelCombinedData.predict(dataFrameForPrediction)
    return math.floor(result[0])

def predict_COVID_part2(train_df, train_labels_df, test_feature):
    numberOFDaysToStartFrom = 50

    df2 = train_df[['dailly_cases']]

    casesCol = 'dailly_cases'
    casesList = []
    pastCase = 16
    for index in range(1, pastCase + 1):
        newColName = casesCol + '-' + str(index)
        casesList.append(newColName)
        df2[newColName] = np.nan
        for rowInd in range(numberOFDaysToStartFrom, len(df2)):
            df2.loc[rowInd, newColName] = int(df2.loc[rowInd - index, casesCol])
        
    dataFrameIncreasing = df2[50:80]
    dataFrameDecreasing = df2[81:137]
    dataFrameConstant = df2[138:]        

    svrModelIncreasing = SVR()
    svrModelDecreasing = SVR()
    svrModelConstant = SVR()

    svrModelIncreasing.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 9500,
                            'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 110})

    svrModelDecreasing.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 9500,
                            'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 110})

    svrModelConstant.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 9500,
                            'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 110})


    xTrainIncreasing = dataFrameIncreasing.drop(['dailly_cases'], 1)
    yTrainIncreasing = train_labels_df.iloc[50:80]
    yTrainIncreasing = yTrainIncreasing.drop(['day'], 1)

    xTrainDecreasing = dataFrameDecreasing.drop(['dailly_cases'], 1)
    yTrainDecreasing = train_labels_df.iloc[81:137]
    yTrainDecreasing = yTrainDecreasing.drop(['day'], 1)

    xTrainConstant = dataFrameConstant.drop(['dailly_cases'], 1)
    yTrainConstant = train_labels_df.iloc[138:]
    yTrainConstant = yTrainConstant.drop(['day'], 1)

    svrModelIncreasing.fit(xTrainIncreasing, yTrainIncreasing)

    svrModelDecreasing.fit(xTrainDecreasing, yTrainDecreasing)

    svrModelConstant.fit(xTrainConstant, yTrainConstant)

    testingForSeperateModels = df2.drop(['dailly_cases'], 1)
    testingForSeperateModels = testingForSeperateModels[numberOFDaysToStartFrom:]


    increasingModelPrediction = svrModelIncreasing.predict(testingForSeperateModels)
    decreasingModelPrediction = svrModelDecreasing.predict(testingForSeperateModels)
    constantModelPrediction = svrModelConstant.predict(testingForSeperateModels)

    combinedData = []
    for index in range(len(increasingModelPrediction)):
        newArray = []
        newArray.append(math.floor(increasingModelPrediction[index]))
        newArray.append(math.floor(decreasingModelPrediction[index]))
        newArray.append(math.floor(constantModelPrediction[index]))
        combinedData.append(newArray)

    xTrainCombinedModel = pd.DataFrame(combinedData, columns=['increasingModelPrediction', 'decreasingModelPrediction', 'constantModelPrediction'])
    yTrainCombinedModel =  train_labels_df.iloc[numberOFDaysToStartFrom:]
    yTrainCombinedModel = yTrainCombinedModel.drop(['day'], 1)

    svrModelCombined = SVR()

    svrModelCombined.set_params(**{'kernel': 'rbf', 'degree': 1, 'C': 9500,
                            'gamma': 'scale', 'coef0': 0.0, 'tol': 0.001, 'epsilon': 110})

    svrModelCombined.fit(xTrainCombinedModel, yTrainCombinedModel)

    dataColumns = casesList
    
    finalPrediction = makePrediction(svrModelIncreasing, svrModelDecreasing, svrModelConstant, svrModelCombined, dataColumns, test_feature)
    
    return finalPrediction
    
    


    
