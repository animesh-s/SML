import sys

def calculate_hyperparameters(classifier):
    if classifier == 'multinomial_naive_bayes':
        f_measure = [0]*21
    else:
        f_measure = [0]*36
    for fold in range(1,6):
        file_name = classifier + '_0_' + str(fold) + '_False.txt'
        reader = open('../../../../' + file_name, 'r')
        index = 0
        for row in reader:
            values = row.split()
            if classifier == 'multinomial_naive_bayes':
                f_measure[index] = f_measure[index] + (float)(values[5])
            else:
                f_measure[index] = f_measure[index] + (float)(values[6])
            index = index + 1
    max_index, max_f_measure = 0, 0
    for index in range(len(f_measure)):
        if f_measure[index] > max_f_measure:
            max_f_measure = f_measure[index]
            max_index = index
    return max_index

if __name__ == "__main__":
    naive_bayes_index = calculate_hyperparameters('multinomial_naive_bayes')
    random_forest_index = calculate_hyperparameters('random_forest')
    print 'Optimal hyperparameters found at index:\n' + 'Multinomial Naive Bayes: ' + str(naive_bayes_index) + '\nRandom Forest: ' + str(random_forest_index)