import sys
import numpy as np 
from scipy import stats
from sklearn.decomposition import PCA
import csv

TRAINING_DATA = "../../../../training_set.csv"

OUTPUT_FILE_NAME = "../../../../principal_components_"

COMPONENT_COUNT = 10


def read_data():

    indices = []
    data = []
    labels = []

    with open(TRAINING_DATA,'rb') as csvfile:
        datareader = csv.reader(csvfile,delimiter=',')
        for row in datareader:
            indices.append(row[0])
            labels.append(row[-1])
            data.append(row[1:len(row)-2])

    return indices,data,labels

def get_principal_components(X):

    pca = PCA(n_components=COMPONENT_COUNT)
    X_r = pca.fit_transform(X)

    return X_r

def store_in_file(X_r,labels,indices):
    
    with open(OUTPUT_FILE_NAME+str(COMPONENT_COUNT), 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for index,sample,label in zip(indices,X_r,labels):
            outrow = [index,sample,label]
            unrolled_outrow = [item for sublist in outrow for item in sublist]
            writer.writerow(unrolled_outrow)

if __name__ == "__main__":

    indices,data,labels = read_data()
    X_r = get_principal_components(data)
    store_in_file(X_r,labels,indices)