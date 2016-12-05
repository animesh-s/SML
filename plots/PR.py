from itertools import cycle
import matplotlib.pyplot as plt

PR_FILES = ["../../Results/pr_logistic","../../Results/pr_svm_rbf","../../Results/pr_svm_linear","../../Results/pr_random_forest",'../../Results/pr_multinomial_naive_bayes']
colors = cycle(['cyan', 'indigo', 'seagreen','darkorange','yellow'])
classifiers = ['Logistic','SVM RBF','SVM Linear','Random Forest','Multinomail Naive Bayes']

lw = 2

def read_data(filename):
    f = open(filename, 'r')

    precision = []
    recall = []
    for row in f:
        row = row.split(' ')
        precision.append(float(row[0]))
        recall.append(float(row[1]))

    return recall,precision

if __name__ == '__main__':
    for  f,color,classifier in zip(PR_FILES,colors,classifiers):
        recall,precision = read_data(f)
        plt.plot(precision, recall, lw=lw, color=color,
             label=classifier)

    # plt.plot([0, 1], [0, 1], linestyle='--', lw=lw, color='k')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.title('Precision-Recall Curve All Features')
    plt.legend(loc="upper right")
    plt.show()