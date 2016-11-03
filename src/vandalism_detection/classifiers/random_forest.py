import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, calculate_metrics, samples_and_labels

def fit_and_predict(clf, num_tree, max_depth, training_samples, training_labels, validation_samples, validation_labels):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    print 'Max Depth = ' + str(max_depth) + '\nNum Tree = ' + str(num_tree) + '\nAccuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nF Score = ' + str(f_score) + '\n'

def run_Random_Forest(clf, num_tree, max_depth, count):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, True)
    fit_and_predict(clf, num_tree, max_depth, training_samples, training_labels, validation_samples, validation_labels)

if __name__ == "__main__":
    max_depths = [5,6,7,8,9,10,11,12,13,14,15]
    num_trees = [5,6,7,8,9,10,11,12,13,14,15]
    for max_depth in max_depths:
        for num_tree in num_trees:
            clf = RandomForestClassifier(n_estimators=num_tree, max_depth=max_depth)
            run_Random_Forest(clf, num_tree, max_depth, 700)
            run_Random_Forest(clf, num_tree, max_depth, 2394)