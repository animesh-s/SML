import csv
import random
import math

def number_of_samples_and_folds():
    return 25951, 5

def number_of_samples_per_fold(n, k):
    vandalism_count_per_fold =  (int)((2394*n/32439)/k)
    regular_count_per_fold = (int)((n/k) - vandalism_count_per_fold)
    return regular_count_per_fold, vandalism_count_per_fold

def k_fold_data_splitting(k, indices, count_per_fold):
    n = count_per_fold * k
    test_samples = range((int)(math.floor(n*(i-1)/k)+1), (int)(math.floor(n*i/k)+1))
    N = range(1, n+1)
    training_samples = [index for index in N if index not in test_samples]
    return training_samples, test_samples

def create_dataset(fold, samples, training_samples, test_samples):
    writer = open('../../../../k_fold_training_set_'+str(fold)+'.csv', 'w')
    for index in training_samples:
        writer.write(samples[index-1] + '\n')
    writer.close()
    writer = open('../../../../k_fold_test_set_'+str(fold)+'.csv', 'w')
    for index in test_samples:
        writer.write(samples[index-1] + '\n')
    writer.close()

if __name__ == "__main__":
    n, k = number_of_samples_and_folds()
    regular_count_per_fold, vandalism_count_per_fold = number_of_samples_per_fold(n, k)
    samples, regular_indices, vandalism_indices, count = [], [], [], 0
    print 'Preparing to split data ..'
    reader = csv.reader(open('../../../../training_set.csv', 'r'))
    for row in reader:
        if row[24] == '0':
            regular_indices.append(count)
        else:
            vandalism_indices.append(count)
        samples.append(','.join(row))
        count = count + 1
    for i in range(1, k+1):
        regular_training_samples, regular_test_samples = k_fold_data_splitting(k, regular_indices, regular_count_per_fold)
        vandalism_training_samples, vandalism_test_samples = k_fold_data_splitting(k, vandalism_indices, vandalism_count_per_fold)
        training_samples = regular_training_samples + vandalism_training_samples
        training_samples.sort()
        test_samples = regular_test_samples + vandalism_test_samples
        test_samples.sort()
        create_dataset(i, samples, training_samples, test_samples)
    print str(k) + ' fold data splitting done.'