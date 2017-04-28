# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import sys, string
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import os
stemmer = PorterStemmer()

#LARA Code
#preprocessing
#load all review texts
def load_file(file):
    reviews = []
    f = open(file,'r')
    for line in f:
        l = line.strip().split('>')
        if l[0] == '<Content':
            reviews.append(l[1])
    f.close()
    return reviews
# print len(reviews), reviews[1]

def parse_to_sentence(reviews):
    review_processed = []
    actual = []
    only_sent = []
    for r in reviews:
        sentences = nltk.sent_tokenize(r)
        actual.append(sentences)
        sent = []
        for s in sentences:
            #words to lower case
            s = s.lower()
            #remove punctuations and stopwords
            replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
            s = s.translate(replace_punctuation)
            stop_words   = list(stopwords.words('english'))
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
        review_processed.append(sent)
        only_sent.extend(sent)
    return review_processed, actual, only_sent

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
    #Assign a number corresponding to each word. Makes counting easier.
    vocab_dict = dict(zip(vocab, range(len(vocab))))
    return vocab, vocab_dict

#Aspect Segmentation
def get_aspect_terms(file, vocab_dict):
    aspect_terms = []
    w_notfound = []
    f = open(file, "r")
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

def aspect_segmentation(form_review):
    #Sentiment analysis
    sid = SIA()

    #INPUT
    #review, this algo needs all the review. Please process dataset.
    # file="Data/Texts/hotel_72572_parsed.txt"
    file = os.path.join(request.folder, 'static','hotel_72572_parsed.txt')
    reviews = load_file(file)
    reviews.append(form_review)

    #selection threshold
    p = 5
    #Iterations 
    # I = 10
    I = 1

    #Create Vocabulary
    review_sent, review_actual, only_sent = parse_to_sentence(reviews)
    vocab, vocab_dict = create_vocab(only_sent)

    #Aspect Keywords
    aspect_file = os.path.join(request.folder, 'static','aspect_keywords.csv')
    aspect_terms = get_aspect_terms(aspect_file, vocab_dict)

    label_text = ['Value', 'Rooms', 'Location', 'Cleanliness', 'Check in/Front Desk', 'Service', 'Business Service']
    # print aspect_terms

    #ALGORITHM
    review_labels = []
    k = len(aspect_terms)
    v = len(vocab)
    aspect_words = np.zeros((k,v))
    aspect_sent = np.zeros(k)
    num_words = np.zeros(v)

    for i in range(I):
        for r in review_sent:
            labels = []
            for s in r:
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
            review_labels.append(labels)
            # aspect_w_rank = chi_sq_mat()
            # new_labels = []
            # for na in aspect_w_rank:
            #   x = np.argsort(na)[::-1][:p]
            #   new_labels.append(x)
                # for k,v in vocab_dict.items():
                #   if vocab_dict[k] in x:
                #       print k
                # print 
            # sys.exit()


    ratings_sentiment = []
    for r in review_actual:
        sentiment = []
        #aspect ratings based on sentiment
        for s in r:
            ss = sid.polarity_scores(s)
            sentiment.append(ss['compound'])
        ratings_sentiment.append(sentiment)

    #Aspect Ratings Per Review
    aspect_ratings = []
    for i,r in enumerate(review_labels):
        rating = np.zeros(7)
        count = np.zeros(7)
        rs = ratings_sentiment[i] 
        for j,l in enumerate(r):
            for k in range(7):
                if k in l:
                    rating[k] += rs[j]
            for k in range(7):
                if count[k] != 0:
                    rating[k] /= count[k]
        #Map from -[-1,1] to [1,5]
        for k in range(7):
            if rating[k] != 0:
                rating[k] = int(round((rating[k]+1)*5/2))
        aspect_ratings.append(rating)
    n = -1
    return review_actual[n], aspect_ratings[n], review_labels[n], label_text
    # n = 0
    # print review_actual[n], '\n', review_labels[n]
    # print ratings_sentiment[n], '\n', aspect_ratings[n]

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL('input'))
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def input():
    return locals()

def output():
    data = request.vars
    review = data['review']
    rating = data['rating']
    a,b,c, lb = aspect_segmentation(review)
    color = ['#07bdff','#ed78e1', '#ea6060','#f4ef55','#58f24f', '#a3a6ff', '#bcafaf']
    return locals()


