import csv
import numpy as np
from numpy import genfromtxt

def calculate_metrics(true_positive, true_negative, false_positive, false_negative):
    if true_positive + false_positive == 0:
        return 0, 0, 0, 0
    total_sample = true_positive + true_negative + false_positive + false_negative
    accuracy = ((float)(true_positive + true_negative) / (total_sample)) * 100
    precision = ((float)(true_positive) / (true_positive + false_positive)) * 100
    recall = ((float)(true_positive) / (true_positive + false_negative)) * 100
    f_score = (float)(2 * precision * recall) / (precision + recall)
    return accuracy, precision, recall, f_score

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

def samples_and_labels(count, use_balanced_set):
    if use_balanced_set:
        training_samples = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
        training_labels = genfromtxt('../../../../training_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18) , dtype=None)
        validation_samples = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = (1,2,3,9,11))
        validation_labels = genfromtxt('../../../../validation_set_' + str(count) + '.csv', delimiter=',', usecols = range(17,18), dtype=None)
    else:
        training_samples = genfromtxt('../../../../training_set.csv', delimiter=',', usecols = range(1,17))
        training_labels = genfromtxt('../../../../training_set.csv', delimiter=',', usecols = range(17,18) , dtype=None)
        validation_samples = genfromtxt('../../../../validation_set.csv', delimiter=',', usecols = range(1,17))
        validation_labels = genfromtxt('../../../../validation_set.csv', delimiter=',', usecols = range(17,18), dtype=None)
    return training_samples, training_labels, validation_samples, validation_labels