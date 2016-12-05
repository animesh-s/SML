from __future__ import division
import sys
import numpy as np 
from scipy import stats
from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
import csv
sys.path.insert(0, '../PCA')
import pca_feature_selection as pca

NU = 0.128
GAMMA = 100

TRAINING_SET = "../../../../training_set.csv"
TESTING_SET = "../../../../test_set.csv"


CONTAMINATION = 0.16

def str_to_float(x):
    return float(x)

def get_svm_classifierObject(_nu,_gamma):
    return svm.OneClassSVM(nu=_nu,kernel="rbf",gamma=_gamma)

def get_elliptical_envelope(_contamination):
    return EllipticEnvelope(contamination = _contamination)

def get_isolation_forest(_contamination):
    return IsolationForest(contamination = _contamination)


def read_data(filename):
        
    X = []
    Y = []

    # Return only the inliers
    X_0 = []

    with open(filename, 'rb') as csvfile:
        
        sample_reader = csv.reader(csvfile,delimiter=',')
        sample_counter = 0
        
        for sample in sample_reader:
            
            sample_feature = sample[1:23]
            sample_feature_float = map(str_to_float,sample_feature)
            X.append(sample_feature_float)
            Y.append(int(sample[24]))
            if int(sample[24]) == 0:
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
        accuracy = (tp + tn)*1.0/total_samples
    except:
        accuracy = -1

    try:
        error = (fp+fn)*1.0/total_samples
    except:
        error = -1

    try:
        recall = tp*1.0/(tp+fn)
    except:
        recall = -1

    try:
        precision = tp*1.0/(tp+fp)
    except:
        precision = -1

    try:
        specificity = tn*1.0/(tn+fp)
    except:
        specificity = -1
    try:
        f_measure = 2*recall*precision/(precision+recall)
    except:
        f_measure = -1

    return [accuracy,error,recall,precision,specificity,f_measure]

def get_validation_statistics(classifier,validation_file):
    
    [X,Y,X_0] = read_data(validation_file)
    y_pred = classifier.predict(X)
    
    return  get_statistics(Y,y_pred)

def get_test_statistics(classifier):
    
    [X,Y,X_0] = read_data(TESTING_SET)
    y_pred = classifier.predict(X)
    
    return  get_statistics(Y,y_pred)

def start_validation_svm():
    
    [X,Y,X_0] = read_data(TRAINING_SET)
    nu_arr = [0.002,0.004,0.008,0.016,0.032,0.064,0.128,0.256]
    gamma_arr = [0.001,0.01,0.1,1,10,100]

    for nu in nu_arr:
        for gamma in gamma_arr:
            
            f_measure_sum = 0.0
            file_names = ['_1','_2','_3','_4','_5']

            for file_name in file_names:
                [X,Y,X_0] = read_data("../../../../k_fold_training_set"+file_name+".csv")
            # Classification task done
                classifier = get_svm_classifierObject(nu,gamma)
                classifier.fit(X_0)
            # Get the statistics on the validation set

                [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier,"../../../../k_fold_test_set"+file_name+".csv")

            # print nu,' ', gamma,' ', round(accuracy,2),' ', round(error,2),' ', round(recall,2),' ', round(precision,2),' ', round(specificity,2),' ',round(f_measure,2)
                if f_measure != -1:
                    f_measure_sum = f_measure_sum + f_measure
            f_measure_sum = f_measure_sum/5

            print nu,' ',gamma,' ', f_measure_sum

def start_validation_isolation_forest():
    contamination_arr = [0.01,0.02,0.04,0.08,0.16,0.32,0.64]

    file_names = ['_1','_2','_3','_4','_5']
    for contamination in contamination_arr:
        f_measure_sum = 0.0
        for file_name in file_names:
            [X,Y,X_0] = read_data("../../../../k_fold_training_set"+file_name+".csv")        
            classifier = get_isolation_forest(contamination)
            classifier.fit(X)

            [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier,"../../../../k_fold_test_set"+file_name+".csv")
            if f_measure != -1:
                f_measure_sum = f_measure_sum + f_measure

        f_measure_sum = f_measure_sum/5
        
        print contamination,' ', f_measure_sum

def start_testing_svm():

    classifier = get_svm_classifierObject(NU,GAMMA)
    [X,Y,X_0] = read_data(TRAINING_SET)
    classifier.fit(X)    
    [accuracy,error,recall,precision,specificity,f_measure] = get_test_statistics(classifier)
    print NU,' ',GAMMA,' ',accuracy,' ', error,' ', recall,' ', precision,' ', specificity,' ',f_measure

def start_testing_isolation_forest():
    classifier = get_isolation_forest(CONTAMINATION)
    [X,Y,X_0] = read_data(TRAINING_SET)
    classifier.fit(X)    
    [accuracy,error,recall,precision,specificity,f_measure] = get_test_statistics(classifier)
    print CONTAMINATION,' ', round(accuracy,2),' ', round(error,2),' ', round(recall,2),' ', round(precision,2),' ', round(specificity,2),' ',round(f_measure,2)



def start_pca_isolation_forest():
    f_measure_sum = 0
    count = 0

    contamination_arr = [0.01,0.02,0.04,0.08,0.16,0.32,0.64]

    file_names = ['1','2','3','4','5']
    training_prefix = "k_fold_training_set_"
    test_prefix = "k_fold_test_set_"
    suffix = '.csv'

    for contamination in contamination_arr:
        for file_name in file_names:
                indices_train,data_train,labels_train = pca.read_data(training_prefix+file_name+suffix)

                data_pc = pca.get_principal_components(data_train,10)
                classifier = get_isolation_forest(contamination)
                classifier.fit(data_pc)

                indices_test,data_test,labels_test = pca.read_data(test_prefix+file_name+suffix)
                data_test_pc = pca.get_principal_components(data_test,10)

                labels_pred = classifier.predict(data_test_pc)            
                [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,labels_pred)
                if f_measure != -1:
                    f_measure_sum = f_measure_sum + f_measure
                    count = count + 1

        f_measure_sum = f_measure_sum/count
        print contamination,' ',f_measure_sum


def start_pca_svm():
    f_measure_sum = 0
    count = 0

    nu_arr = [0.008,0.016,0.032,0.064,0.128,0.256]
    gamma_arr = [0.01,0.1,1,10,100]

    file_names = ['1','2','3','4','5']
    training_prefix = "../../../../k_fold_training_set_"
    test_prefix = "../../../../k_fold_test_set_"
    suffix = '.csv'

    for nu in nu_arr:
        for gamma in gamma_arr:
            for file_name in file_names:
                    indices_train,data_train,labels_train = pca.read_data(training_prefix+file_name+suffix)

                    data_pc = pca.get_principal_components(data_train,15)
                    classifier = get_svm_classifierObject(nu,gamma)
                    classifier.fit(data_pc)

                    indices_test,data_test,labels_test = pca.read_data(test_prefix+file_name+suffix)
                    data_test_pc = pca.get_principal_components(data_test,15)

                    labels_pred = classifier.predict(data_test_pc)            
                    [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,labels_pred)
                    if f_measure != -1:
                        f_measure_sum = f_measure_sum + f_measure
                        count = count + 1

            f_measure_sum = f_measure_sum/count
            print nu,' ',gamma,' ',f_measure_sum

def start_testing_isolation_forest_pca():
    classifier = get_isolation_forest(CONTAMINATION)
    indices_train,data_train,labels_train = pca.read_data(TRAINING_SET)

    data_train_pc = pca.get_principal_components(data_train,10)

    classifier.fit(data_train_pc)

    indices_test,data_test,labels_test = pca.read_data(TESTING_SET)
    data_test_pc = pca.get_principal_components(data_test,10)

    y_pred = classifier.predict(data_test_pc)

    [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,y_pred)
    print CONTAMINATION,' ', round(accuracy,2),' ', round(error,2),' ', round(recall,2),' ', round(precision,2),' ', round(specificity,2),' ',round(f_measure,2)

def start_testing_svm_pca():
    classifier = get_svm_classifierObject(NU,GAMMA)
    indices_train,data_train,labels_train = pca.read_data(TRAINING_SET)

    data_train_pc = pca.get_principal_components(data_train,10)

    classifier.fit(data_train_pc)

    indices_test,data_test,labels_test = pca.read_data(TESTING_SET)
    data_test_pc = pca.get_principal_components(data_test,10)

    y_pred = classifier.predict(data_test_pc)

    [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,y_pred)
    print NU,' ',GAMMA,' ',accuracy,' ', error,' ', recall,' ', precision,' ', specificity,' ',f_measure    

if __name__ == "__main__":

    mode = sys.argv[1]
    algo = sys.argv[2]

    if mode == 'VALIDATION':
        if algo == 'SVM':
            start_validation_svm()
        if algo == 'ISOLATION_FOREST':
            start_validation_isolation_forest()

    if mode == 'TEST':
        if algo == 'SVM':
            start_testing_svm()
        if algo == 'ISOLATION_FOREST':
            start_testing_isolation_forest()

    if mode == 'TEST_PCA':
        if algo == 'SVM':
            start_testing_svm_pca()
        if algo == 'ISOLATION_FOREST':
            start_testing_isolation_forest_pca()

    if mode == 'PCA_VALIDATION':
        if algo == 'SVM':
            start_pca_svm()
        if algo == 'ISOLATION_FOREST':
            start_pca_isolation_forest()