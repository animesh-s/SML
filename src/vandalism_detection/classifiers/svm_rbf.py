import csv
import sys
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_svm_rbf
from sklearn import svm
from sklearn.svm import SVC

def fit_and_predict(clf, gamma, C, count, fold,training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, specificity,f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_svm_rbf(count, gamma, C, fold, accuracy, precision, recall,specificity, f_score, use_balanced_set, use_feature_selection)

def run_svm_rbf(clf, gamma, C, count, fold,  use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels, test_samples, test_labels = samples_and_labels(count, fold,  use_balanced_set, use_feature_selection)
    fit_and_predict(clf, gamma, C, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

def test_svm_rbf(gamma, C, count, fold, use_balanced_set, use_feature_selection):
    clf = svm.SVC(C=C, gamma=gamma)
    training_samples, training_labels, validation_samples, validation_labels, test_samples, test_labels = samples_and_labels(count, fold, use_balanced_set, use_feature_selection)
    clf.fit(training_samples, training_labels)
    result = clf.predict(test_samples)
    accuracy, precision, recall, specificity,f_score = calculate_precision_recall(test_labels, result)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF1 Score = ' + str(f_score) + '\n'

if __name__ == "__main__":
    if sys.argv[1] == 'train':
		kArray=[1,2,3,4,5];
		for k in kArray:	
		    CArray = [100,0.1,1,10,100,1000]
		    GammaArray = [0.01,0.1,1,10,100]
		    for C in CArray:
		        for gamma in GammaArray:
		            print 'Running for gamma = ' + str(gamma) + ' and C = ' + str(C) + '\n'
		            clf = svm.SVC(C=C, gamma=gamma)
		            #run_svm_rbf(clf, gamma, C, 700, True, True)
		            #run_svm_rbf(clf, gamma, C, 700, True, False)
		            #run_svm_rbf(clf, gamma, C, 2394, True, True)
		            #run_svm_rbf(clf, gamma, C, 2394, True, False)
		            #run_svm_rbf(clf, gamma, C, 0, False, True)
		            run_svm_rbf(clf, gamma, C, 0,k, False, False)
    else:
        gamma = sys.argv[2:8]
        C = sys.argv[8:]
        test_svm_rbf((float)(gamma[0]), (float)(C[0]), 700, True, True)
        test_svm_rbf((float)(gamma[1]), (float)(C[1]), 700, True, False)
        test_svm_rbf((float)(gamma[2]), (float)(C[2]), 2394, True, True)
        test_svm_rbf((float)(gamma[3]), (float)(C[3]), 2394, True, False)
        test_svm_rbf((float)(gamma[4]), (float)(C[4]), 0, False, True)
        test_svm_rbf((float)(gamma[5]), (float)(C[5]), 0, False, False)
