import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers
	
	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)
		
	def confidence(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		
		choice_votes = votes.count(mode(votes))
		conf = float(choice_votes) / len(votes)
		return conf
		
		
		

documents = [(list(movie_reviews.words(fileid)), category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]

#random.shuffle(documents)

#print (documents)

all_words = []
for w in movie_reviews.words():
	all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

#print len(all_words.keys())
word_features = list(all_words.keys())[:3000]; #use only top 3000 most common words

def find_features(document):
	words = set(document)
	features = {}
	for w in word_features:
		features[w] = (w in words) # returns boolean 
	
	return features
	
#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

#print(len(documents))

#positive reviews data
training_set = featuresets[:1900]
testing_set = featuresets[1900:]	

#negative reviews data
#training_set = featuresets[100:]
#testing_set = featuresets[:100]	


#Naive Bayes
# posterior = prior_occurances * likelihood / evidence

#classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()


print('Original Naive Bayes Algo accuracy percent:', (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

#MultinomialNB from scikitlearn
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print('MultinomialNB Algo accuracy percent:', (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

#GaussianNB
#GNB_classifier = SklearnClassifier(GaussianNB())
#GNB_classifier.train(training_set)
#print('GaussianNB Algo accuracy percent:', (nltk.classify.accuracy(GNB_classifier, testing_set))*100)

#BernoulliNB
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print('BernoulliNB Algo accuracy percent:', (nltk.classify.accuracy(BNB_classifier, testing_set))*100)

#LogisticRegression, SDGClassifier
#SVC, LinearSVC, NuSVC

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print('LogisticRegression Algo accuracy percent:', (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print('SGDClassifier Algo accuracy percent:', (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print('LinearSVC Algo accuracy percent:', (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print('NuSVC Algo accuracy percent:', (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

## Vote Classifier & Confidence 

## 7 classfiers
voted_classifier =  VoteClassifier(MNB_classifier, BNB_classifier, LogisticRegression_classifier, LinearSVC_classifier, NuSVC_classifier)



print('voted_clasifier Algo accuracy percent:', (nltk.classify.accuracy(voted_classifier, testing_set))*100)



#print (testing_set[0][0])


