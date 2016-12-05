import sys
import numpy as np 
from scipy import stats
from sklearn import svm

from sklearn import linear_model

import csv
sys.path.insert(0, '../PCA')

import pca_feature_selection as pca
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve


TRAINING_SET = "../../../../training_set.csv"
# VALIDATION_SET = "../../../../k_fold_training_set_1.csv"
TESTING_SET = "../../../../test_set.csv"

ROC_file_logistic = "../../../../Results/roc_logistic"
ROC_file_logistic_5 = "../../../../Results/roc_logistic_pca_5"
ROC_file_logistic_pca_15 = "../../../../Results/roc_logistic_pca_15"
ROC_file_logistic_pca_10 = "../../../../Results/roc_logistic_pca_10"

PR_file_logistic = "../../../../Results/pr_logistic"
PR_file_logistic_pca_10 = "../../../../Results/pr_logistic_pca_10"

# Parameter for the algorithm
C = 4500

# Model specific variables
PENALTY = 'l2' # Norm used in the penalization

def str_to_float(x):
    return float(x)

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

def get_validation_statistics(classifier,VALIDATION_SET):
    [X,Y,X_0] = read_data(VALIDATION_SET)
    y_pred = classifier.predict(X)
    return  get_statistics(Y,y_pred)

def start_validation():

    C_arr = [0.001,0.01,0.1,1,10,100,1000,10000]
    prefix_training = "../../../../k_fold_training_set_"
    prefix_test = "../../../../k_fold_test_set_"
    suffix = ".csv"
    file_names = ['1','2','3','4','5']
    for C in C_arr:
        classifier = get_classifier(C)
        f_measure_sum = 0.0
        count = 0
        for file_name in file_names:
            training_file = prefix_training + file_name + suffix
            test_file = prefix_test + file_name + suffix

            [X,Y,X_0] = read_data(training_file)

            classifier.fit(X,Y) 

            [accuracy,error,recall,precision,specificity,f_measure] = get_validation_statistics(classifier,test_file)
            
            if f_measure != -1:
                f_measure_sum = f_measure_sum + f_measure
                count = count + 1


        f_measure_sum = f_measure_sum/count

        print C,' ',f_measure_sum


def get_test_statistics(classifier):
    [X,Y,X_0] = read_data(TESTING_SET)

    y_pred = classifier.predict(X)

    return  get_statistics(Y,y_pred)

def print_roc_data(fpr,tpr):
    writer = open(ROC_file_logistic_pca_10,'w')

    for a,b in zip(fpr,tpr):
        writer.write(str(a)+' '+str(b)+'\n')

    writer.close()

def print_pr_data(precision,recall,filename):
    writer = open(filename,'w')
    for a,b in zip(precision,recall):
        writer.write(str(a)+' '+str(b)+'\n')

    writer.close()

def start_testing():
    [X,Y,X_0] = read_data(TRAINING_SET)

    classifier = get_classifier(C)
    classifier.fit(X,Y)

    # read the test data

    [X_test,Y_test,X_0_test] = read_data(TESTING_SET)


    prob_estimates = classifier.predict_proba(X_test)

    # ROC data
    fpr, tpr, thresholds = metrics.roc_curve(y_true=Y_test,y_score=prob_estimates[:,1],pos_label=1)

    # PR data
    precision,recall,_ = precision_recall_curve(y_true=Y_test,probas_pred=prob_estimates[:,1],pos_label=1)

    print_roc_data(fpr,tpr)    
    print_pr_data(precision,recall,PR_file_logistic)    

    y_pred = classifier.predict(X_test)

    [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(Y_test,y_pred)

    print C,' ',accuracy,' ',recall,' ',precision,' ',specificity,' ',f_measure

def start_pca_validation():
    prefix_training = "../../../../k_fold_training_set_"
    prefix_test = "../../../../k_fold_test_set_"
    suffix = ".csv"
    file_names = ['1','2','3','4','5']

    C_arr = [4000,4100,4200,4300,4400,4500,4600,4700,4800,4900,5000,6000,7000,8000,9000,10000]

    for c in C_arr:
        f_measure_sum = 0
        count = 0
        for file_name in file_names:
            classifier = get_classifier(c)
            training_file = prefix_training + file_name + suffix
            test_file = prefix_test + file_name + suffix

            indices_train,data_train,labels_train = pca.read_data(training_file)

            X_pc_train = pca.get_principal_components(data_train,10)

            classifier.fit(X_pc_train,labels_train) 

            indices_test,data_test,labels_test = pca.read_data(test_file)

            X_pc_test = pca.get_principal_components(data_test,10)

            y_pred = classifier.predict(X_pc_test)

            [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,y_pred)
            
            if f_measure != -1:
                f_measure_sum = f_measure_sum + f_measure
                count = count + 1


        f_measure_sum = f_measure_sum/count
        print c,' ',f_measure_sum

def start_testing_pca():

    indices_train,data_train,labels_train = pca.read_data(TRAINING_SET)

    data_train_pc = pca.get_principal_components(data_train,10)
    classifier = get_classifier(C)
    classifier.fit(data_train_pc,labels_train)

    # read the test data

    indices_test,data_test,labels_test = pca.read_data(TESTING_SET)
    data_test_pc = pca.get_principal_components(data_test,10)

    # Code For ROC curve
    prob_estimates = classifier.predict_proba(data_test_pc)

    fpr, tpr, thresholds = metrics.roc_curve(y_true=labels_test,y_score=prob_estimates[:,1],pos_label=1)

    precision,recall,_ = precision_recall_curve(y_true=labels_test,probas_pred=prob_estimates[:,1],pos_label=1)

    print_roc_data(fpr,tpr)
    print_pr_data(precision,recall,PR_file_logistic_pca_10)    
    y_pred = classifier.predict(data_test_pc)

    [accuracy,error,recall,precision,specificity,f_measure] = get_statistics(labels_test,y_pred)

    print C,' ',accuracy,' ',recall,' ',precision,' ',specificity,' ',f_measure

if __name__ == "__main__":

    mode = sys.argv[1]

    if mode == 'TEST':
        start_testing()
    
    if mode == 'TEST_PCA':
        start_testing_pca()

    if mode == 'KFOLD':
        start_validation()

    if mode == 'PCA_KFOLD':
        start_pca_validation()
