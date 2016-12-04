import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_svm_linear
from pca_feature_selection import get_principal_components, read_data, store_in_file
from sklearn import svm
from sklearn.svm import LinearSVC


def fit_and_predict(clf,C,count,fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
	clf.fit(training_samples, training_labels)
	result = clf.predict(validation_samples)
	accuracy, precision, recall, specificity, f_score = calculate_precision_recall(validation_labels, result)
	create_result_txt_for_svm_linear(count, C,fold, accuracy, precision, recall,specificity, f_score, use_balanced_set, use_feature_selection)
def run_SVM_Linear(clf,C, count,fold):
	training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, fold,  False,True)
	fit_and_predict(clf,C,count,fold, training_samples, training_labels, validation_samples, validation_labels, False,True)

def test_SVM_Linear(tempC, count,fold):
	clf = svm.LinearSVC(C=tempC)
	training_samples, training_labels, test_samples, test_labels = samples_and_labels(count, fold,  False,False)
	clf.fit(training_samples, training_labels)
	result = clf.predict(test_samples)
	accuracy, precision, recall, specificity,f_score = calculate_precision_recall(test_labels, result)
	print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nSpecificity = ' + str(specificity) + '\nF1 Score = ' + str(f_score) + '\n'



if __name__ == "__main__":
	kArray=[0]#,2,3,4,5];
	for k in kArray:
		CArray=[0.1,1,10,100,500,1000]
		for tempC in CArray:
				print 'Running for C = ' + str(tempC) + '\n'
				clf = svm.LinearSVC(C=tempC)
				run_SVM_Linear(clf, tempC, 0,k)
				#test_SVM_Linear(tempC,0,k)
