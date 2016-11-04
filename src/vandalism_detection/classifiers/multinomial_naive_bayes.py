import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import preprocessing
from metrics import calculate_precision_recall, samples_and_labels, create_result_txt_for_multinomial_naive_bayes

def fit_and_predict(clf, alpha, count, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection):
    clf.fit(training_samples, training_labels)
    result = clf.predict(validation_samples)
    accuracy, precision, recall, f_score = calculate_precision_recall(validation_labels, result)
    create_result_txt_for_multinomial_naive_bayes(count, alpha, accuracy, precision, recall, f_score, use_balanced_set, use_feature_selection)

def run_Multinomial_Naive_Bayes(clf, alpha, count, use_balanced_set, use_feature_selection):
    training_samples, training_labels, validation_samples, validation_labels = samples_and_labels(count, use_balanced_set, use_feature_selection, True)
    fit_and_predict(clf, alpha, count, training_samples, training_labels, validation_samples, validation_labels, use_balanced_set, use_feature_selection)

if __name__ == "__main__":
    alpha_values = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
    for alpha in alpha_values:
        print 'Running for alpha = ' + str(alpha) + '\n'
        clf = MultinomialNB(alpha=alpha)
        run_Multinomial_Naive_Bayes(clf, alpha, 700, True, True)
        run_Multinomial_Naive_Bayes(clf, alpha, 700, True, False)
        run_Multinomial_Naive_Bayes(clf, alpha, 2394, True, True)
        run_Multinomial_Naive_Bayes(clf, alpha, 2394, True, False)
        run_Multinomial_Naive_Bayes(clf, alpha, 0, False, True)
        run_Multinomial_Naive_Bayes(clf, alpha, 0, False, False)