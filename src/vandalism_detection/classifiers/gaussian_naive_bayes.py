import csv
import numpy as np
from numpy import genfromtxt
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_metrics

def samples_and_labels(count):
    training_samples = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
    training_labels = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18) , dtype=None)
    validation_samples = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
    validation_labels = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18), dtype=None)
    return training_samples, training_labels, validation_samples, validation_labels

def fit_and_predict(clf, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for sample, predicted_label in enumerate(result):
        if validation_labels[sample]==0 and predicted_label==0:
            true_negative = true_negative + 1             
        elif validation_labels[sample]==0 and predicted_label==1:
            false_positive = false_positive + 1
        elif validation_labels[sample]==1 and predicted_label==0:
            false_negative = false_negative + 1
        else:
            true_positive = true_positive + 1
    accuracy, precision, recall = calculate_metrics(true_positive, true_negative, false_positive, false_negative)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\n'

def run_Gaussian_Naive_Bayes(clf, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count)
    fit_and_predict(clf, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
    clf = GaussianNB()
    run_Gaussian_Naive_Bayes(clf, 700)
    run_Gaussian_Naive_Bayes(clf, 2394)
