import sys

def calculate_hyperparameters(classifier, use_feature_selection):
    if classifier == 'multinomial_naive_bayes':
        f_measure = [0]*21
        if use_feature_selection == 'true':
            return 0, 0, 0
    else:
        f_measure = [0]*36
    for fold in range(1,6):
        if use_feature_selection == 'true':
            file_name = classifier + '_0_' + str(fold) + '_True.txt'
        else:
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
    return max_index, max_f_measure/5, f_measure

if __name__ == "__main__":
    naive_bayes_index, naive_bayes_max_f_measure, naive_bayes_f_measure = calculate_hyperparameters('multinomial_naive_bayes', sys.argv[1])
    random_forest_index, random_forest_max_f_measure, random_forest_f_measure = calculate_hyperparameters('random_forest', sys.argv[1])
    print 'Optimal hyperparameters found at index:\n' + 'Multinomial Naive Bayes: ' + str(naive_bayes_index) + ', F1 Score: ' + str(naive_bayes_max_f_measure) + '\nRandom Forest: ' + str(random_forest_index) + ', F1 Score: ' + str(random_forest_max_f_measure)