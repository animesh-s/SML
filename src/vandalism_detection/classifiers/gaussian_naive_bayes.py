import csv
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels

def fit_and_predict(clf, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF Score = ' + str(f_score) + '\n'

def run_Gaussian_Naive_Bayes(clf, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, True)
    fit_and_predict(clf, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
    clf = GaussianNB()
    run_Gaussian_Naive_Bayes(clf, 700)
    run_Gaussian_Naive_Bayes(clf, 2394)
