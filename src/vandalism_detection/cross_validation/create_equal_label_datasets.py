import csv
import random

def dataset_count(T, training_percent, validation_percent):
    training_count = (int)(training_percent * T)
    validation_count = (int)(validation_percent * T)
    test_count = T - training_count - validation_count
    return training_count, validation_count, test_count

def reservoir_sampling(indices, training_count, validation_count, test_count):
    training_samples = random.sample(indices, training_count)
    training_samples.sort()
    indices = [index for index in indices if index not in training_samples]
    validation_samples = random.sample(indices, validation_count)
    validation_samples.sort()
    indices = [index for index in indices if index not in training_samples]
    test_samples = random.sample(indices, test_count)
    test_samples.sort()
    return training_samples, validation_samples, test_samples

def create_dataset(samples, training_samples, validation_samples, test_samples, count):
    writer = open('../../../../training_set_' + str(count) + '.csv', 'w')
    for index in training_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    writer = open('../../../../validation_set_' + str(count) + '.csv', 'w')
    for index in validation_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    writer = open('../../../../test_set_' + str(count) + '.csv', 'w')
    for index in test_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    print 'Data splitting done.\nTraining Set - 60%\nValidation Set - 20%\nTest Set - 20%\n'

def create_equal_dataset(regular_indices, vandalism_indices, samples, count, training_percent, validation_percent):
    regular_training_count, regular_validation_count, regular_test_count = dataset_count(count, training_percent, validation_percent)
    vandalism_training_count, vandalism_validation_count, vandalism_test_count = dataset_count(count, training_percent, validation_percent)
    regular_training_samples, regular_validation_samples, regular_test_samples = reservoir_sampling(regular_indices, regular_training_count, regular_validation_count, regular_test_count)
    vandalism_training_samples, vandalism_validation_samples, vandalism_test_samples = reservoir_sampling(vandalism_indices, vandalism_training_count, vandalism_validation_count, vandalism_test_count)
    training_samples = regular_training_samples + vandalism_training_samples
    training_samples.sort()
    validation_samples = regular_validation_samples + vandalism_validation_samples
    validation_samples.sort()
    test_samples = regular_test_samples + vandalism_test_samples
    test_samples.sort()
    create_dataset(samples, training_samples, validation_samples, test_samples, count)

if __name__ == "__main__":    
    samples = []
    regular_indices = []
    vandalism_indices = []
    count = 0
    print 'Preparing to split data ..'
    reader = csv.reader(open('../../../../features.csv', 'r'))
    for row in reader:
        if row[17] == '0':
            regular_indices.append(count)
        else:
            vandalism_indices.append(count)
        samples.append(','.join(row))
        count = count + 1

    create_equal_dataset(regular_indices, vandalism_indices, samples, 700, 0.6, 0.2)
    create_equal_dataset(regular_indices, vandalism_indices, samples, 2394, 0.6, 0.2)
    