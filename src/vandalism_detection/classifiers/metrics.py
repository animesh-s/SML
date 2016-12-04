import csv
import sys
import numpy as np
from numpy import genfromtxt
sys.path.append('../PCA/')
from pca_feature_selection import get_principal_components

def calculate_metrics(true_positive, true_negative, false_positive, false_negative):
    if true_positive + false_positive == 0:
        return 0, 0, 0, 0, 0
    total_sample = true_positive + true_negative + false_positive + false_negative
    accuracy = ((float)(true_positive + true_negative) / (total_sample)) * 100
    precision = ((float)(true_positive) / (true_positive + false_positive)) * 100
    recall = ((float)(true_positive) / (true_positive + false_negative)) * 100
    specificity = ((float)(true_negative) / (true_negative + false_positive)) * 100
    if precision == 0 and recall == 0:
        f_score = 0
    else:
        f_score = (float)(2 * precision * recall) / (precision + recall)
    return accuracy, precision, recall, specificity, f_score

def calculate_precision_recall(validation_labels, result):
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
    return calculate_metrics(true_positive, true_negative, false_positive, false_negative)

def create_result_txt_for_svm_rbf(count, gamma, C,fold, accuracy, precision, recall,specificity, f_score, use_balanced_set, use_feature_selection):
    writer = open('../../../../svm_rbf_' + str(count) + '_' + str(fold) + '_' + str(use_feature_selection) + '.txt', 'a')
    writer.write(str(gamma) + ' ' + str(C) + ' ' + str(accuracy) + ' ' + str(precision) + ' ' + str(recall)+ ' ' + str(specificity) + ' ' + str(f_score) + '\n')
    writer.close()

def create_result_txt_for_svm_linear(count, C,fold, accuracy, precision, recall,specificity, f_score, use_balanced_set, use_feature_selection):
    writer = open('../../../../svm_linear_' + str(count) + '_' + str(fold) + '_' + str(use_feature_selection) + '.txt', 'a')
    writer.write(str(C) + ' ' + str(accuracy) + ' ' + str(precision) + ' ' + str(recall)+ ' ' + str(specificity) + ' ' + str(f_score) + '\n')
    writer.close()

def create_result_txt_for_multinomial_naive_bayes(count, alpha, fold, accuracy, precision, recall, specificity, f_score, use_balanced_set, use_feature_selection):
    writer = open('../../../../multinomial_naive_bayes_' + str(count) + '_' + str(fold) + '_' + str(use_feature_selection) + '.txt', 'a')
    writer.write(str(alpha) + ' ' + str(accuracy) + ' ' + str(precision) + ' ' + str(recall) + ' ' + str(specificity) + ' ' + str(f_score) + '\n')
    writer.close()

def create_result_txt_for_random_forest(count, num_tree, max_depth, fold, accuracy, precision, recall, specificity, f_score, use_balanced_set, use_feature_selection):
    writer = open('../../../../random_forest_' + str(count) + '_' + str(fold) + '_' + str(use_feature_selection) + '.txt', 'a')
    writer.write(str(num_tree) + ' ' + str(max_depth) + ' ' + str(accuracy) + ' ' + str(precision) + ' ' + str(recall) + ' ' + str(specificity) + ' ' + str(f_score) + '\n')
    writer.close()

def pca(training_samples, training_labels, test_samples, test_labels, use_feature_selection):
    if use_feature_selection:
        training_samples = get_principal_components(training_samples.tolist(), 10)
        test_samples = get_principal_components(test_samples.tolist(), 10)
    return training_samples, training_labels, test_samples, test_labels

def samples_and_labels(count, fold, use_balanced_set, use_feature_selection, naive_bayes = False):
    if naive_bayes:
        features = range(1,4) + range(5,24)
    else:
        features = range(1,24)
    if use_balanced_set:
        training_samples = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = features)
        training_labels = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = range(24,25) , dtype=None)
        validation_samples = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = features)
        validation_labels = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = range(24,25), dtype=None)
        test_samples = genfromtxt('../../../../test_set_' + str(count) + '.csv', delimiter=',', usecols = features)
        test_labels = genfromtxt('../../../../test_set_' + str(count) + '.csv', delimiter=',', usecols = range(24,25), dtype=None)
    else:
        if fold == 0:
            training_samples = genfromtxt('../../../../training_set.csv', delimiter=',', usecols = features)
            training_labels = genfromtxt('../../../../training_set.csv', delimiter=',', usecols = range(24,25) , dtype=None)
            test_samples = genfromtxt('../../../../test_set.csv', delimiter=',', usecols = features)
            test_labels = genfromtxt('../../../../test_set.csv', delimiter=',', usecols = range(24,25), dtype=None)
            return pca(training_samples, training_labels, test_samples, test_labels, use_feature_selection)
        else:
            training_samples = genfromtxt('../../../../k_fold_training_set_' + str(fold) + '.csv', delimiter=',', usecols = features)
            training_labels = genfromtxt('../../../../k_fold_training_set_' + str(fold) + '.csv', delimiter=',', usecols = range(24,25) , dtype=None)
            validation_samples = genfromtxt('../../../../k_fold_test_set_' + str(fold) + '.csv', delimiter=',', usecols = features)
            validation_labels = genfromtxt('../../../../k_fold_test_set_' + str(fold) + '.csv', delimiter=',', usecols = range(24,25), dtype=None)
            return pca(training_samples, training_labels, validation_samples, validation_labels, use_feature_selection)