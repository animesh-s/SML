import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels

def fit_and_predict(clf, alpha, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    print 'Alpha = ' + str(alpha) + '\nAccuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF Score = ' + str(f_score) + '\n'

def run_Multinomial_Naive_Bayes(clf, alpha, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, True)
    fit_and_predict(clf, alpha, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
    alpha_values = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.002, 0.003, 0.004, 
                    0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 
                    0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 20.0, 50.0, 100.0]
    for alpha in alpha_values:
        clf = MultinomialNB(alpha=alpha)
        run_Multinomial_Naive_Bayes(clf, alpha, 700)
        run_Multinomial_Naive_Bayes(clf, alpha, 2394)