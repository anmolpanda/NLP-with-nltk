import nltk
import random
from nltk.corpus import movie_reviews
import pickle

documents = [(list(movie_reviews.words(fileid)), category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

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
training_set = featuresets[:1900]
testing_set = featuresets[1900:]	

#Naive Bayes
# posterior = prior_occurances * likelihood / evidence

#classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()


print('Naive Bayes Algo accuracy percent:', (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

##save_classifier = open("naivebayes.pickle", "wb")
##pickle.dump(classifier, save_classifier)
##save_classifier.close()
