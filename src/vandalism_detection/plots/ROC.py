from itertools import cycle
import matplotlib.pyplot as plt

ROC_FILES = ["../../Results/roc_logistic_pca_10","../../Results/roc_svm_rbf_pca","../../Results/roc_svm_linear_pca","../../Results/roc_random_forest_pca",'../../Results/roc_multinomial_naive_bayes']
colors = cycle(['cyan', 'indigo', 'seagreen','darkorange','yellow'])
classifiers = ['Logistic','SVM RBF','SVM Linear','Random Forest','Multinomial Naive Bayes']
lw = 2

def read_data(filename):
    f = open(filename, 'r')

    fpr = []
    tpr = []
    for row in f:
        row = row.split(' ')
        fpr.append(float(row[0]))
        tpr.append(float(row[1]))

    return fpr,tpr

if __name__ == '__main__':
    for  f,color,classifier in zip(ROC_FILES,colors,classifiers):
        fpr,tpr = read_data(f)
        plt.plot(fpr, tpr, lw=lw, color=color,
             label=classifier)

    plt.plot([0, 1], [0, 1], linestyle='--', lw=lw, color='k')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC All Features')
    plt.legend(loc="lower right")
    plt.show()
