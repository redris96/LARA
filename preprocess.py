import sys, string
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
stemmer = PorterStemmer()

#load all review texts
def load_file(file):
	reviews = []
	f = open(file,'r')
	for line in f:
		l = line.strip().split('>')
		if l[0] == '<Content':
			reviews.append(l[1])
	return reviews
# print len(reviews), reviews[1]

def parse_to_sentence(reviews):
	sent = []
	for r in reviews:
		sentences = nltk.sent_tokenize(r)
		for s in sentences:
			#words to lower case
			s = s.lower()
			#remove punctuations and stopwords
			s = s.translate(None, string.punctuation)
			stop_words	 = list(stopwords.words('english'))
			additional_stopwords = ["'s","...","'ve","``","''","'m",'--',"'ll","'d"]
			# additional_stopwords = []
			stop_words = set(stop_words + additional_stopwords)
			# print stop_words
			# sys.exit()
			word_tokens = word_tokenize(s)
			s = [w for w in word_tokens if not w in stop_words]
			#Porter Stemmer
			stemmed = [stemmer.stem(w) for w in s]
			if len(stemmed)>0:
				sent.append(stemmed)
	return sent

# sent = parse_to_sentence(reviews)
# print len(sent), sent[2]

def create_vocab(sent):
	words = []
	for s in sent:
		words += s
	freq = FreqDist(words)
	vocab = []
	for k,v in freq.items():
		if v > 5:
			vocab.append(k)
	return vocab
