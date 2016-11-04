import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels
from sklearn import svm
from sklearn.svm import SVC

def fit_and_predict(clf, gamma, C, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    print 'Gamma = ' + str(gamma) + '\nC = ' + str(C)+ '\nAccuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF Score = ' + str(f_score) + '\n'

def run_SVM_RBF(clf, gamma, C, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, True)
    fit_and_predict(clf, gamma,C, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
	CArray = [0.01,0.1,1,10,100,500,1000]
	GammaArray = [0.01,0.1,1,10,100]
	for C in CArray:
		for gamma in GammaArray:
			clf = svm.SVC(C=C, gamma=gamma)
			run_SVM_RBF(clf, gamma, C, 700)
			run_SVM_RBF(clf, gamma, C, 2394)  
