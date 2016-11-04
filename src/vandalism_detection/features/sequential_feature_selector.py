from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from numpy import genfromtxt
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

if __name__ == "__main__":
	X = genfromtxt('../../../../features.csv', delimiter=',',usecols = range(1,17))
	y = genfromtxt('../../../../features.csv', delimiter=',',usecols = range(17,18))
	clf = SVC()
	sfs = SFS(clf, k_features = 5, forward = True, floating = False, scoring = 'accuracy', cv = 0)
	sfs = sfs.fit(X, y)
	feature_count = len(sfs.k_feature_idx_)
	count = 0;	
	text_file = open("../../../../selected_features.txt", "w")
	for feature in sfs.k_feature_idx_:
		count = count + 1;
		text_file.write("%s" % feature)
		if count < feature_count:	
			text_file.write(",")
	text_file.close()
