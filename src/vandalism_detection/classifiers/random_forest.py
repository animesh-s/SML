import sys
import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_random_forest, create_result_txt_for_roc_and_pr_plots

def fit_and_predict(clf, num_tree, max_depth, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, specificity, f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_random_forest(count, num_tree, max_depth, fold, accuracy, precision, recall, specificity, f_score, use_balanced_set, use_feature_selection)

def run_Random_Forest(clf, num_tree, max_depth, count, fold, use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, fold, use_balanced_set, use_feature_selection)
    fit_and_predict(clf, num_tree, max_depth, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

def test_Random_Forest(num_tree, max_depth, count, use_balanced_set, use_feature_selection):
    clf = RandomForestClassifier(n_estimators=num_tree, max_depth=max_depth)
    training_samples, training_labels, test_samples, test_labels = samples_and_labels(count, 0, use_balanced_set, use_feature_selection)
    clf.fit(training_samples, training_labels)
    result = clf.predict(test_samples)
    accuracy, precision, recall, specificity, f_score = calculate_precision_recall(test_labels, result)
    create_result_txt_for_roc_and_pr_plots('random_forest', clf, test_samples, test_labels, use_feature_selection)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nSpecificity = ' + str(specificity) + '\nF1 Score = ' + str(f_score) + '\n' 

if __name__ == "__main__":
    if sys.argv[1] == 'train':
        max_depths = [5,7,9,11,13,15]
        num_trees = [5,7,9,11,13,15]
        for fold in range(1,6):
            for max_depth in max_depths:
                for num_tree in num_trees:
                    print 'Running for max_depth = ' + str(max_depth) + ' and num_tree = ' + str(num_tree) + '\n'
                    clf = RandomForestClassifier(n_estimators=num_tree, max_depth=max_depth)
                    # run_Random_Forest(clf, num_tree, max_depth, 700, True, True)
                    # run_Random_Forest(clf, num_tree, max_depth, 700, True, False)
                    # run_Random_Forest(clf, num_tree, max_depth, 2394, True, True)
                    # run_Random_Forest(clf, num_tree, max_depth, 2394, True, False)
                    if sys.argv[2] == 'pca':
                        run_Random_Forest(clf, num_tree, max_depth, 0, fold, False, True)
                    else:
                        run_Random_Forest(clf, num_tree, max_depth, 0, fold, False, False)
    else:
        num_trees, max_depth = sys.argv[2], sys.argv[3]
        # num_trees = sys.argv[2:8]
        # max_depths = sys.argv[8:]
        # test_Random_Forest((int)(num_trees[0]), (int)(max_depths[0]), 700, True, True)
        # test_Random_Forest((int)(num_trees[1]), (int)(max_depths[1]), 700, True, False)
        # test_Random_Forest((int)(num_trees[2]), (int)(max_depths[2]), 2394, True, True)
        # test_Random_Forest((int)(num_trees[3]), (int)(max_depths[3]), 2394, True, False)
        if sys.argv[4] == 'pca':
            test_Random_Forest((int)(num_trees), (int)(max_depth), 0, False, True)
        else:
            test_Random_Forest((int)(num_trees), (int)(max_depth), 0, False, False)