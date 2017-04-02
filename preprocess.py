import sys, string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *

#load all review texts
reviews = []
file="Data/Texts/hotel_72572_parsed.txt"
f = open(file,'r')
for line in f:
	l = line.strip().split('>')
	if l[0] == '<Content':
		#words to lower case
		s = l[1].lower()
		#remove punctuations and stopwords
		s = s.translate(None, string.punctuation)
		stop_words	 = set(stopwords.words('english'))
		word_tokens = word_tokenize(s)
		s = [w for w in word_tokens if not w in stop_words]
		#Porter Stemmer
		stemmed = [stemmer.stem(s) for w in s]
		reviews.append(' '.join(stemmed))
print len(reviews), reviews[1]