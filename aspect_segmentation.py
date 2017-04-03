from preprocess import *
import numpy as np

#goal: map sentences to corresponding aspect.

def get_aspect_terms(file, vocab_dict):
	aspect_terms = []
	w_notfound = []
	f = open(aspect_file, "r")
	for line in f:
		s = line.strip().split(",")
		stem = [stemmer.stem(w.strip().lower()) for w in s]
		#we store words by their corresponding number.
		# aspect = [vocab_dict[w] for w in stem]
		aspect = []
		for w in stem:
			if vocab_dict.has_key(w):
				aspect.append(w)
			else:
				w_notfound.append(w)
		aspect_terms.append(aspect)
	#We are only using one hotel review file, as we keep inceasing the number of files words not found will decrease.
	# print "Words not found in vocab:", ' '.join(w_notfound)
	f.close()
	return aspect_terms

# def chi_sq(w, A, sent):


#INPUT
#review, this algo needs all the review. Please process dataset.
file="Data/Texts/hotel_72572_parsed.txt"
reviews = load_file(file)

#selection threshold
p = 5
#Iterations 
I = 10

#Create Vocabulary
sent = parse_to_sentence(reviews)
vocab, vocab_dict = create_vocab(sent)

#Aspect Keywords
aspect_file = "init_aspect_keywords.txt"
aspect_terms = get_aspect_terms(aspect_file, vocab_dict)
# print aspect_terms

#ALGORITHM
labels = []
k = len(aspect_terms)
v = len(vocab)
aspect_words = np.zeros((k,v))
aspect_sent = np.zeros(k)
num_words = np.zeros(v)

def chi_sq(a,b,c,d):
	c1 = a
	c2 = b - a
	c3 = c - a
	c4 = d - b - c + a
	nc =  d
	return nc * (c1*c4 - c2*c3) * (c1*c4 - c2*c3)/((c1+c3) * (c2+c4) * (c1+c2) * (c3+c4))


def chi_sq_mat():
	global aspect_words, aspect_sent, num_words
	asp_rank = np.zeros(aspect_words.shape)
	for i in range(len(aspect_terms)):
		for j in range(len(vocab)):
			asp_rank[i][j] = chi_sq(aspect_words[i][j], num_words[j], aspect_sent[i], len(sent))
	return asp_rank


for i in range(I):
	for s in sent:
		count = np.zeros(len(aspect_terms))
		i = 0
		for a in aspect_terms:
			for w in s:
				if vocab_dict.has_key(w):
					num_words[vocab_dict[w]] += 1
					if w in a:
						count[i] += 1
			i = i + 1
		if max(count) > 0:
			la = np.where(np.max(count) == count)[0].tolist()
			labels.append(la)
			for i in la:
				aspect_sent[i] += 1
				for w in s:
					if vocab_dict.has_key(w):
						aspect_words[i][vocab_dict[w]] += 1
		else:
			labels.append([])
	# aspect_w_rank = chi_sq_mat()
	# for na in aspect_w_rank:
	# 	x = np.argsort(na)[::-1][:p]
	# 	for k,v in vocab_dict.items():
	# 		if vocab_dict[k] in x:
	# 			print k
	# 	print 
	# sys.exit()


# print sent[5:9], labels[5:9]
print zip(sent, labels)[12:14]