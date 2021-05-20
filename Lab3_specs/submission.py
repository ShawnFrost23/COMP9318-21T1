################# Question 1 #################
## import modules here 
import math

def processTrainData(training_data):

    vocabulary = set([])

    spamDictionary = {}
    lengthSpamDict = 0
    totalSpamMessages = 0

    hamDictionary = {}
    lengthHamDict = 0
    totalHamMessages = 0

    for (dict, category) in training_data:

        for key in dict:
            vocabulary.add(key)

        if category == 'spam':
            totalSpamMessages += 1

            for key, value in dict.items():
                
                lengthSpamDict += value
                
                if key not in spamDictionary:
                    spamDictionary[key] = value
                else:
                    spamDictionary[key] += value


        elif category == 'ham':
            totalHamMessages += 1

            for key, value in dict.items():

                lengthHamDict += value

                if key not in hamDictionary:
                    hamDictionary[key] = value
                else:
                    hamDictionary[key] += value

    return spamDictionary, lengthSpamDict, totalSpamMessages, hamDictionary, lengthHamDict, totalHamMessages, vocabulary, len(vocabulary)



def multinomial_nb(training_data, sms):# do not change the heading of the function


    spamDictionary, lengthSpamDict, totalSpamMessages, hamDictionary, lengthHamDict, totalHamMessages, vocabulary, lengthVocabulary = processTrainData(training_data)

    spamProbablity = math.log(totalSpamMessages);
    hamProbablity = math.log(totalHamMessages);

    spamWordsFraction = lengthSpamDict + lengthVocabulary;
    hamWordsFraction = lengthHamDict + lengthVocabulary;
    
    smoothing = 1

    for word in sms:

        if word not in vocabulary:
            spamProbablity += 0
        elif word not in spamDictionary:
            spamProbablity += math.log(1 / spamWordsFraction)
        else:
            spamProbablity += math.log((spamDictionary[word] + smoothing) / spamWordsFraction)

        if word not in vocabulary:
            hamProbablity += 0
        elif word not in hamDictionary:
            hamProbablity += math.log(1 / hamWordsFraction)
        else:
            hamProbablity += math.log((hamDictionary[word] + smoothing) / hamWordsFraction)

    return math.exp(spamProbablity) / math.exp(hamProbablity)
