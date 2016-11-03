import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels
from sklearn import svm
from sklearn.svm import LinearSVC


def fit_and_predict(clf,C, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    print 'C = ' + str(C)+ '\nAccuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF Score = ' + str(f_score) + '\n'


def run_SVM_Linear(clf,C, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, True)
    fit_and_predict(clf,C, training_samples, training_labels, validation_samples, validation_labels)


if __name__ == "__main__":
	CArray=[0.01,0.1,1,10,100,500,1000]
	for tempC in CArray:
			clf = svm.LinearSVC(C=tempC)#C=0.01,kernel='rbf',gamma=0.1)
			run_SVM_Linear(clf,tempC, 700)
			run_SVM_Linear(clf,tempC, 2394)  