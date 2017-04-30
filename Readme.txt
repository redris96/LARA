Code Structure

preprocess.py : 
Input: Raw data
Output: Porocessed Data Per Review
Overview: Contain all the preprocessing for the data such as slitting data into reviews and each individual reviews into sentences and other operations such as stemming each word to it's root, removing stop words, etc.

aspect_segmentation.py:
Input: Processed Data
Output: Aspect Ratings for each review.
Overview: This takes all the review and identifies the sentences corresponding to various aspects such as Value, Room, Location, etc. and give rating to each aspect for all the reviews.

regression.py:
Input:Aspect Ratings
Output:Aspect Weights
Overview:In this module we find the aspect weights by maximizing the log-likelihood (This is done by Gradient descent) with respect to the aspect weights,subject to constraints.We initialize the parameters by random values and update the parameters after each iteration.

Dependencies
It requires the nltk dataset and additional packages for running. Use nltk.download() and download all the given packages. Also required is the vader package from nltk.
It requires tensorflow for python3.

Running Code
The code can be run manually by using aspect_segmentation or regression. But, it has all been incorporated into a website, included is a web2py folder. cd into it and run ./web2py and go to localhost:8000/LARA and it should give you a form to write your own review. On submitting it, it would give the results. 
Note: Make sure all dependacies are satisfied.

