import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_random_forest

def fit_and_predict(clf, num_tree, max_depth, count, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_random_forest(count, num_tree, max_depth, accuracy, precision, recall, f_score, use_balanced_set, use_feature_selection)

def run_Random_Forest(clf, num_tree, max_depth, count, use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, use_balanced_set, use_feature_selection)
    fit_and_predict(clf, num_tree, max_depth, count, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

if __name__ == "__main__":
    max_depths = [5,7,9,11,13,15]
    num_trees = [5,7,9,11,13,15]
    for max_depth in max_depths:
        for num_tree in num_trees:
            print 'Running for max_depth = ' + str(max_depth) + ' and num_tree = ' + str(num_tree) + '\n'
            clf = RandomForestClassifier(n_estimators=num_tree, max_depth=max_depth)
            run_Random_Forest(clf, num_tree, max_depth, 700, True, True)
            run_Random_Forest(clf, num_tree, max_depth, 700, True, False)
            run_Random_Forest(clf, num_tree, max_depth, 2394, True, True)
            run_Random_Forest(clf, num_tree, max_depth, 2394, True, False)
            run_Random_Forest(clf, num_tree, max_depth, 0, False, True)
            run_Random_Forest(clf, num_tree, max_depth, 0, False, False)
