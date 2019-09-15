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

def preprocessing(df):
  #Preprocessing with regex
  p = r'[^\w\s]+'
  number = r'\d+'
  words = ['RT']
  user = r'@[^\s]+'
  link = r'((www\.[^\s]+)|(https?://[^\s]+))'
  #two_letter = r'^\w{2}$' #r'/^w{2}$'
  pat = r'\b(?:{})\b'.format('|'.join(words+stopwords))

  for i in (user, link, p, number, pat):
    try:
      df.tweet = df.tweet.str.replace(i, '')
      #df.tweet = df.tweet.apply(lambda x: " ".join(x.split()))
      df.tweet = df.tweet.str.lower()
    except AttributeError:
      df = re.sub(i, ' ', df)
      df = " ".join(df.split())
      df = df.lower()
  return df

def save_model():
    df = pd.read_csv('tweets.csv', sep=";;;", error_bad_lines=False)
    df.columns = ['class','tweet']

    df2 = df.copy()
    preprocessing(df)
    df2.dropna(inplace=True)


    #Pipeline creation
    X = df2.tweet
    y = df2['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=1242)
    text_clf = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression())])
    text_clf.fit(X_train, y_train)

    toBePersisted = dict({
    'model': text_clf,
    'metadata': {
        'name': 'mrNicky',
        'author': 'Zakaria TAHI',
        'date': '4 septembre 2019',
        'source_code_version': '001',
        'metrics': {
            'accuracy': '0.78' }}})
    #Save Model
    joblib.dump(text_clf, 'tweet_model.pkl')

def run_model(text):
    text = [preprocessing(text[0])]
    #Open model
    tweet_model = open(os.path.join(sys.path[0], 'tweet_model.pkl'),'rb')
    text_clf = joblib.load(tweet_model)

    #New predict value
    result = {'0': 'Plutot negatif', '4':'Plutot Positif'}
    new_prediction = result[text_clf.predict(text)[0]]
    return new_prediction
