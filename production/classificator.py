import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import xgboost as xgb
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import spacy

nltk.download('punkt')
nltk.download('stopwords')

# Define a function to remove stopwords and punctuation
def remove_stopwords_punctuation(text):
    stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token not in string.punctuation]
    return ' '.join(filtered_tokens)

class XGBoostClassifier(BaseEstimator, TransformerMixin):
    def __init__(self, model_path):
        self.model_path = model_path
        with open(self.model_path, 'rb') as file:
            self.model = pickle.load(file)
    def fit(self, X, y=None):
        return self
    def predict(self, X):
        dmatrix_data = xgb.DMatrix(X)
        probabilities = self.model.predict(dmatrix_data)
        return probabilities

# Load the TfidfVectorizer from the file
with open('tfidf_vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Create the pipeline
pipeline = Pipeline([
    ('combine_columns', FunctionTransformer(lambda x: x['DESCRICAO'] + ' ' + x['TITULO'] + ' ' + x['LOCAL'] + ' ' + x['EMPRESA'], validate=False)),
    ('add_text_column', FunctionTransformer(lambda x: pd.DataFrame({'TEXT': x}), validate=False)),
    ('remove_punctuation', FunctionTransformer(lambda x: x['TEXT'].apply(remove_stopwords_punctuation), validate=False)),
    ('drop_columns', FunctionTransformer(lambda x: x.drop(columns=['DESCRICAO', 'TITULO', 'LOCAL', 'EMPRESA']), validate=False)),
    ('tfidf_vectorizer', vectorizer),
    ('prediction', XGBoostClassifier('xgboost_model.pkl'))
])



#### Prevendo novos dados:

data_new = pd.read_csv("newly_fetched_data.csv")

predictions = pipeline.predict(data_new)

df_combined = pd.concat([data_new, pd.DataFrame(predictions)], axis=1)

df_combined.to_csv('data_predicted.csv', index=False)