import sys
import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_multinomial_naive_bayes

def fit_and_predict(clf, alpha, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, specificity, f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_multinomial_naive_bayes(count, alpha, fold, accuracy, precision, recall, specificity, f_score, use_balanced_set, use_feature_selection)

def run_Multinomial_Naive_Bayes(clf, alpha, count, fold, use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, fold, use_balanced_set, use_feature_selection, True)
    fit_and_predict(clf, alpha, count, fold, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

def test_Multinomial_Naive_bayes(alpha, count, use_balanced_set, use_feature_selection):
    clf = MultinomialNB(alpha=alpha)
    training_samples, training_labels, test_samples, test_labels = samples_and_labels(count, 0, use_balanced_set, use_feature_selection, True)
    clf.fit(training_samples, training_labels)
    result = clf.predict(test_samples)
    accuracy, precision, recall, specificity, f_score = calculate_precision_recall(test_labels, result)
    print 'Accuracy = ' + str(accuracy) + '\nPrecision = ' + str(precision) + '\nRecall = ' + str(recall) + '\nSpecificity = ' + str(specificity) + '\nF1 Score = ' + str(f_score) + '\n'

if __name__ == "__main__":
    if sys.argv[1] == 'train':
        alpha_values = [0.0001, 0.0002, 0.0004, 0.0008, 0.0016, 0.0032, 0.0064, 0.0128, 0.0256, 0.0512, 0.1024, 0.2048, 0.4096, 
                        0.8192, 1.6384, 3.2768, 6.5536, 13.1072, 26.2144, 52.4288, 100.0]
        for fold in range(1,6):
            for alpha in alpha_values:
                print 'Running for alpha = ' + str(alpha) + '\n'
                clf = MultinomialNB(alpha=alpha)
                # run_Multinomial_Naive_Bayes(clf, alpha, 700, True, True)
                # run_Multinomial_Naive_Bayes(clf, alpha, 700, True, False)
                # run_Multinomial_Naive_Bayes(clf, alpha, 2394, True, True)
                # run_Multinomial_Naive_Bayes(clf, alpha, 2394, True, False)
                # run_Multinomial_Naive_Bayes(clf, alpha, 0, False, True)
                run_Multinomial_Naive_Bayes(clf, alpha, 0, fold, False, False)
    else:
        alpha = sys.argv[2]
        #alphas = sys.argv[2:]
        # test_Multinomial_Naive_bayes((float)(alphas[0]), 700, True, True)
        # test_Multinomial_Naive_bayes((float)(alphas[1]), 700, True, False)
        # test_Multinomial_Naive_bayes((float)(alphas[2]), 2394, True, True)
        # test_Multinomial_Naive_bayes((float)(alphas[3]), 2394, True, False)
        # test_Multinomial_Naive_bayes((float)(alphas[4]), 0, False, True)
        test_Multinomial_Naive_bayes((float)(alpha), 0, False, False)