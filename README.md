# Vandalism Detection in Wikipedia

## Problem Statement

We plan to identify the cases of vandalism on Wikipedia articles by classifying edits as either *regular* or *vandalism*. This is clearly a Binary Classification task, but because of the skewed distribution of regular and vandalism cases in the dataset, we will also explore if this can be modeled as an Anomaly Detection problem.

## Dataset

We will use the corpus of vandalism cases found on Wikipedia which is available [here]
(http://www.uni-weimar.de/en/media/chairs/webis/corpora/pan-wvc-10/). The corpus consists of 32452 edits on 28468 Wikipedia articles among which 2391 edits have been labeled as vandalism, while the rest are labeled as regular.

## Experimental Setup

### Algorithms

We plan to implement these algorithms for the Binary Classification task: Multinomial Naive Bayes, Logistic Regression, and Linear and Radial Basis Kernel Support Vector Machine.
We can also model this problem as an Anomaly Detection task and implement the One-class Support Vector Machine with Linear and Radial Basis Kernels. For the Feature Selection task, we plan to use the Greedy Subset and Forward Fitting algorithms.

### Parameter Tuning

Nu - For the One-class SVM

Gamma - For the Radial Basis Kernel

C - For the Linear and Radial Basis Kernels

Alpha - Smoothing parameter for Multinomial Naive Bayes

L2 - Regularization parameter for Logistic Regression

We’ll use k-fold cross-validation for tuning these parameters and split the dataset randomly into training and testing sets with 70% reserved for training and the rest of 30% for testing.

### Experimental Plots

We plan to plot these graphs to validate our experiments: Accuracy vs training size for all al- gorithms, Accuracy vs features selected from different algorithms, Accuracy vs parameter values, Accuracy comparison for all algorithms and ROC curves to measure the accuracy of the tests.

Accuracy = (# Correct Predictions) / (# Data Points)