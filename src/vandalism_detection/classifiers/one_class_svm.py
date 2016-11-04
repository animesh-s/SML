import sys
import numpy as np 
from scipy import stats
from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest

import csv

NU = 0.07
GAMMA = 0.0001

TRAINING_SET = "../../../../training_set.csv"
VALIDATION_SET = "../../../../validation_set.csv"
TESTING_SET = "../../../../test_set_700.csv"

VALIDATION_STATISTICS = "../../../../validation_statistics.csv"
TEST_STATISTICS = "../../../../test_statistics.csv"

SAMPLE_FLAG = 'FULL' # 'PARTIAL' : means only N_SAMPLE_FLAG features will be loaded
N_SAMPLE_FLAG = 20000
SAMPLE_SIZE = 32439

def str_to_float(x):
    return float(x)

def get_svm_classifierObject(_nu,_gamma):
    return svm.OneClassSVM(nu=_nu,kernel="rbf",gamma=_gamma)

def get_elliptical_envelope(_contamination):
    return EllipticEnvelope(contamination = _contamination)

def get_isolation_forest(_contamination):
    return IsolationForest(max_samples = SAMPLE_SIZE,contamination = _contamination)
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

def get_statistics(y_true,y_pred):

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for (u,v) in zip(y_true,y_pred):
        if u == 1 and v == 1:
            fn += 1
        if u == 0 and v == 1:
            tn += 1
        if u == 1 and v == -1:
            tp += 1
        if u == 0 and v == -1:
            fp += 1

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

def get_test_statistics(classifier):
    
    [X,Y] = read_data(TESTING_SET)
    y_pred = classifier.predict(X)
    
    return  get_statistics(Y,y_pred)

def start_training_svm(algo):
    
    [X,Y,X_0] = read_data(TRAINING_SET)
    nu_arr = [0.00000001,0.0000001,0.000001,0.00001,0.0001,0.001,0.01,0.1]
    gamma_arr = [0.00000001,0.0000001,0.000001,0.00001,0.0001,0.001,0.01,0.1,1,10,100]

    for nu in nu_arr:
        for gamma in gamma_arr:
            
            # Classification task done
            classifier = get_svm_classifierObject(nu,gamma)
            if algo == 'NOVELTY':
                classifier.fit(X_0)
            if algo == 'OUTLIER':
                classifier.fit(X)
            # Get the statistics on the validation set

            [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier)

            print nu,' ', gamma,' ', round(accuracy,2),' ', round(error,2),' ', round(recall,2),' ', round(precision,2),' ', round(specificity,2),' ',round(f_measure,2)


def start_training_isolation_forest():
    [X,Y,X_0] = read_data(TRAINING_SET)

    contamination_arr = np.arange(0.01,1,0.01)


    for contamination in contamination_arr:
        classifier = get_isolation_forest(contamination)
        classifier.fit(X)

        [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier)

        print contamination,' ', round(accuracy,2),' ', round(error,2),' ', round(recall,2),' ', round(precision,2),' ', round(specificity,2),' ',round(f_measure,2)
def start_testing():

    classifier = get_trained_classifier()
    get_test_statistics(classifier)

if __name__ == "__main__":

    mode = sys.argv[1]
    algo = sys.argv[2]
    perspective = sys.argv[3]

    if mode == 'TRAIN':
        if algo == 'SVM':
            start_training_svm(perspective)
        if algo == 'ISOLATION_FOREST':
            start_training_isolation_forest()

    if mode == 'TEST':
        start_testing()