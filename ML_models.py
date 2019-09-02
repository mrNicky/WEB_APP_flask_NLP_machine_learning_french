#Nos modules pour notre modèle
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
stopwords = stopwords.words('french')

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import re
import sys
import os



def save_model():
    df = pd.read_csv('tweets.csv', sep=";;;", error_bad_lines=False)
    df.columns = ['class','tweet']
    
    df2 = df.copy()

    #Preprocessing with regex
    p = r'[^\w\s]+'
    number = r'\d+'
    words = ['RT']
    user = r'@[^\s]+'
    link = r'((www\.[^\s]+)|(https?://[^\s]+))'
    two_letter = r'/^[a-z]{2}$'
    pat = r'\b(?:{})\b'.format('|'.join(words+stopwords))    
    for i in (user, link, p, pat, number, two_letter):
        df2.tweet = df2.tweet.str.replace(i, '')
 
    df2.tweet = df2.tweet.str.lower()
    df2.dropna(inplace=True)
   
  
    #Pipeline creation
    X = df2.tweet
    y = df2['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=1242)
    text_clf = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression())])
    text_clf.fit(X_train, y_train)
    
    #Save Model
    joblib.dump(text_clf, 'tweet_model.pkl')
    
def run_model(text):
    
    #Open model
    tweet_model = open(os.path.join(sys.path[0], 'tweet_model.pkl'),'rb')
    text_clf = joblib.load(tweet_model)

    #New predict value
    result = {'0': 'Plutot negatif', '4':'Plutot Positif'}
    new_prediction = result[text_clf.predict(text)[0]]
    return new_prediction


