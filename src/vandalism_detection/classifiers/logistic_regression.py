import sys
import numpy as np 
from scipy import stats
from sklearn import svm

from sklearn import linear_model

import csv


TRAINING_SET = "../../../../training_set_2394.csv"
VALIDATION_SET = "../../../../validation_set_2394.csv"
TESTING_SET = "../../../../test_set_2394.csv"

SAMPLE_FLAG = 'FULL' # 'PARTIAL' : means only N_SAMPLE_FLAG features will be loaded
N_SAMPLE_FLAG = 20000
SAMPLE_SIZE = 32439

# Parameter for the algorithm
C = 100


# Model specific variables
PENALTY = 'l2' # Norm used in the penalization

def str_to_float(x):
    return float(x)

def read_data(filename):
    
    is_full = (SAMPLE_FLAG == 'FULL')
    
    X = []
    Y = []

    # Return only the inliers
    X_0 = []

    with open(filename, 'rb') as csvfile:
        
        sample_reader = csv.reader(csvfile,delimiter=',')
        sample_counter = 0
        
        for sample in sample_reader:
            
            if (not is_full) and sample_counter >= N_SAMPLE_FLAG: break
            sample_feature = sample[1:17]
            sample_feature_float = map(str_to_float,sample_feature)
            # sample_feature_float = []
            # sample_feature_float.append(float(sample[1]))
            # sample_feature_float.append(float(sample[2]))
            # sample_feature_float.append(float(sample[3]))
            # sample_feature_float.append(float(sample[9]))
            # sample_feature_float.append(float(sample[11]))
            X.append(sample_feature_float)
            Y.append(int(sample[17]))
            if int(sample[17]) == 0:
                X_0.append(sample_feature_float)
            sample_counter += 1

        return [X,Y,X_0]

def get_classifier(_C):

    return linear_model.LogisticRegression(C = _C,penalty=PENALTY)

def get_statistics(y_true,y_pred):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for (u,v) in zip(y_true,y_pred):
        if u == 1 and v == 1:
            tp += 1
        if u == 0 and v == 1:
            fp += 1
        if u == 1 and v == 0:
            fn += 1
        if u == 0 and v == 0:
            tn += 1

    total_samples = fn + tn + fp + tp

    try:
        accuracy = (tp + tn)*100.0/total_samples
    except:
        accuracy = -1

    try:
        error = (fp+fn)*100.0/total_samples
    except:
        error = -1

    try:
        recall = tp*100.0/(tp+fn)
    except:
        recall = -1

    try:
        precision = tp*100.0/(tp+fp)
    except:
        precision = -1

    try:
        specificity = tn*100.0/(tn+fp)
    except:
        specificity = -1
    try:
        f_measure = 2*recall*precision/(precision+recall)
    except:
        f_measure = -1

    return [accuracy,error,recall,precision,specificity,f_measure]

def get_validation_statistics(classifier):
    [X,Y,X_0] = read_data(VALIDATION_SET)
    y_pred = classifier.predict(X)
    return  get_statistics(Y,y_pred)

def start_training():

    [X,Y,X_0] = read_data(TRAINING_SET)

    C_arr = [0.0001,0.001,0.01,0.1,1,10,100,1000,10000]

    for C in C_arr:
        classifier = get_classifier(C)
        classifier.fit(X,Y) 

        [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier)

        print C,' ',accuracy,' ',recall,' ',precision,' ',specificity,' ',f_measure

def get_test_statistics(classifier):
    [X,Y,X_0] = read_data(TESTING_SET)

    y_pred = classifier.predict(X)

    return  get_statistics(Y,y_pred)

def start_testing():
    [X,Y,X_0] = read_data(TRAINING_SET)

    classifier = get_classifier(C)
    classifier.fit(X,Y)

    [accuracy,error,recall,precision,specificity,f_measure] = get_test_statistics(classifier)

    print C,' ',accuracy,' ',recall,' ',precision,' ',specificity,' ',f_measure


if __name__ == "__main__":

    mode = sys.argv[1]

    if mode == 'TRAIN':
        start_training()
    if mode == 'TEST':
        start_testing()

