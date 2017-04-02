from preprocess import *

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
				aspect.append(vocab_dict[w])
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
for i in range(I):
