import csv
import random

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

def create_dataset(samples, training_samples, validation_samples, test_samples):
    writer = open('../../../../training_set.csv', 'w')
    for index in training_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    writer = open('../../../../validation_set.csv', 'w')
    for index in validation_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    writer = open('../../../../test_set.csv', 'w')
    for index in test_samples:
        writer.write(samples[index] + '\n')
    writer.close()
    print 'Data splitting done.\nTraining Set - 60%\nValidation Set - 20%\nTest Set - 20%'

if __name__ == "__main__":
    T = 32439
    training_count = (int)(0.6 * T)
    validation_count = (int)(0.2 * T)
    test_count = T - training_count - validation_count
    samples = []
    indices = []
    count = 0
    print 'Preparing to split data ..'
    reader = csv.reader(open('../../../../features.csv', 'r'))
    for row in reader:
        indices.append(count)
        samples.append(','.join(row))
        count = count + 1
        
    training_samples, validation_samples, test_samples = reservoir_sampling(indices, training_count, validation_count, test_count)
    create_dataset(samples, training_samples, validation_samples, test_samples)