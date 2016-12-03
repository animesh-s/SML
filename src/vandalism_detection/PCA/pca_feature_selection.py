import sys
import numpy as np 
from scipy import stats
from sklearn.decomposition import PCA
import csv

def read_data(training_filename):

    indices = []
    data = []
    labels = []

    with open(training_filename,'rb') as csvfile:
        datareader = csv.reader(csvfile,delimiter=',')
        for row in datareader:
            indices.append(row[0])
            labels.append(row[-1])
            data.append(row[1:len(row)-2])

    return indices,data,labels

def get_principal_components(data,n_components):

    pca = PCA(n_components=n_components)
    return pca.fit_transform(data)

def store_in_file(X_r,labels,indices,output_filename):
    
    with open(output_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for index,sample,label in zip(indices,X_r,labels):
            outrow = [index,sample,label]
            unrolled_outrow = [item for sublist in outrow for item in sublist]
            writer.writerow(unrolled_outrow)