import csv
import numpy as np
from numpy import genfromtxt
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_metrics

def samples_and_labels(count):
    training_samples = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
    training_labels = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18) , dtype=None)
    validation_samples = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
    validation_labels = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18), dtype=None)
    return training_samples, training_labels, validation_samples, validation_labels

def fit_and_predict(clf, alpha, training_samples, training_labels, validation_samples, validation_labels):
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
    print 'Alpha = ' + str(alpha) + '\nAccuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall)+ '\nPrecision = ' + str(precision) + '\n'

def run_Multinomial_Naive_Bayes(clf, alpha, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count)
    fit_and_predict(clf, alpha, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
    alpha_values = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 20.0, 50.0, 100.0]
    for alpha in alpha_values:
        clf = MultinomialNB(alpha=alpha)
        run_Multinomial_Naive_Bayes(clf, alpha, 700)
        run_Multinomial_Naive_Bayes(clf, alpha, 2394)