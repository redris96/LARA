from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sentences=["decor beauti lobbi furnitur fit time period still comfi","The decor is beautiful, the lobby furniture fits the time period  is still comfy","The rooms in the hotel are really good"]
sid = SIA()
for sentence in sentences:
    ss = sid.polarity_scores(sentence)
    print ss