import sys
import numpy as np 
from scipy import stats
from sklearn.decomposition import PCA
import csv

def read_data(training_filename):
    indices = []
    data = []
    labels = []
    with open('../../../../'+training_filename,'rb') as csvfile:
        datareader = csv.reader(csvfile,delimiter=',')
        for row in datareader:
            indices.append(row[0])
            labels.append(row[-1])
            data.append(row[1:len(row)-1])
    return indices, data, labels

def store_in_file(X_r,labels,indices,output_filename):
    writer = open('../../../../'+output_filename, 'w')
    count = len(indices)
    for index in range(count):
        sample = ','.join(["%.4f" % number for number in X_r[index].tolist()])
        writer.write(str(indices[index]) + ',' + str(sample) + ',' + str(labels[index]) + '\n')

def get_principal_components(data, n_components):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(data)