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
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, fold,  use_balanced_set, use_feature_selection)
    fit_and_predict(clf, gamma, C, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

def test_svm_rbf(gamma, C, count, use_balanced_set, use_feature_selection):
    clf = svm.SVC(C=C, gamma=gamma)
    training_samples, training_labels, test_samples, test_labels = samples_and_labels(count, 0, use_balanced_set, use_feature_selection)
    clf.fit(training_samples, training_labels)
    result = clf.predict(test_samples)
    accuracy, precision, recall, specificity,f_score = calculate_precision_recall(test_labels, result)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nSpecificity = ' + str(specificity) + '\nF1 Score = ' + str(f_score) + '\n'

if __name__ == "__main__":
    if sys.argv[1] == 'train':
        kArray=[1,2,3,4,5]
        for k in kArray:
            CArray = [0.01,0.1,1,10,100,1000]
            GammaArray = [0.01,0.1,1,10,100]
            for C in CArray:
                for gamma in GammaArray:
                    print 'Running for gamma = ' + str(gamma) + ' and C = ' + str(C) + '\n'
                    clf = svm.SVC(C=C, gamma=gamma)
                    if sys.argv[2] == 'pca':
                        run_svm_rbf(clf, gamma, C, 0, k, False, True)
                    else:
                        run_svm_rbf(clf, gamma, C, 0, k, False, False)
    else:
        gamma, C = (float)(sys.argv[2]), (float)(sys.argv[3])
        if sys.argv[4] == 'pca':
            test_svm_rbf(gamma, C, 0, False, True)
        else:
            test_svm_rbf(gamma, C, 0, False, False)