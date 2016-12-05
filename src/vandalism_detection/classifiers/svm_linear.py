import csv
import sys
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_svm_linear, create_result_txt_for_roc_and_pr_plots
from pca_feature_selection import get_principal_components, read_data, store_in_file
from sklearn import svm
from sklearn.svm import LinearSVC

def fit_and_predict(clf,C,count,fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, specificity, f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_svm_linear(count, C,fold, accuracy, precision, recall,specificity, f_score, use_balanced_set, use_feature_selection)

def run_SVM_Linear(clf, C, count, fold, use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, fold, use_balanced_set, use_feature_selection)
    fit_and_predict(clf,C,count,fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

def test_SVM_Linear(tempC, count, use_balanced_set, use_feature_selection):
    clf = svm.LinearSVC(C=tempC)
    training_samples, training_labels, test_samples, test_labels = samples_and_labels(count, 0, use_balanced_set, use_feature_selection)
    clf.fit(training_samples, training_labels)
    result = clf.predict(test_samples)
    accuracy, precision, recall, specificity,f_score = calculate_precision_recall(test_labels, result)
    create_result_txt_for_roc_and_pr_plots('svm_linear', clf, test_samples, test_labels, use_feature_selection)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nSpecificity = ' + str(specificity) + '\nF1 Score = ' + str(f_score) + '\n'

if __name__ == "__main__":
    if sys.argv[1] == 'train':
        kArray = [1,2,3,4,5]
        CArray=[0.1,1,10,100,500,1000]
        for k in kArray:
            for tempC in CArray:
                print 'Running for C = ' + str(tempC) + '\n'
                clf = svm.LinearSVC(C=tempC)
                if sys.argv[2] == 'pca':
                    run_SVM_Linear(clf, tempC, 0, k, False, True)
                else:
                    run_SVM_Linear(clf, tempC, 0, k, False, False)
    else:
        tempC = sys.argv[2]
        if sys.argv[3] == 'pca':
            test_SVM_Linear((float)(tempC), 0, False, True)
        else:
            test_SVM_Linear((float)(tempC), 0, False, False)