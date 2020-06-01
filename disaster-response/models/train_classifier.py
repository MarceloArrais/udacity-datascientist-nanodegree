# import libraries
import sys
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import nltk
nltk.download(['punkt', 'wordnet'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def load_data(database_filepath):
    '''
    ** Load cleaned data and split into X and y to machine learning process
    >> Args:
        database_filepath - path of file 
    << return
        X - messages
        y - categories (more than one column) 
    '''
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql('messages_cleaned', engine)
    X =  df.message.values
    Y =  df.loc[:, 'related':'direct_report']
    
    categories = df.columns.difference(['id','message', 'original', 'genre']).values
    
    return X, Y, categories

def tokenize(text):
    '''
    ** Used to split some sentence into words and lemmatizer them  
    >> Args:
        text - a string that represent the message    
    << Return: 
        tokens_cleaned_lst: list of cleaned words
    '''   
    # normalize
    text = re.sub(r"[^a-zA-Z0-9]", " ", text) 
    
    tokens_lst = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    tokens_cleaned_lst = []
    for token in tokens_lst:
        if token not in stopwords.words("english"):  # remove stop words
            token_cleaned = lemmatizer.lemmatize(token, pos = 'v').strip()
            tokens_cleaned_lst.append(token_cleaned)
        
    return tokens_cleaned_lst


def build_model():
    '''
    << return: a trained multi-label classifier model.
    '''
    
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('best', TruncatedSVD()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])
    
    parameters = { 
        #'vect__ngram_range': ((1, 1), (1, 2)),
        #'vect__max_df': (0.75, 1.0),
        #'tfidf__use_idf': (True, False), 
        #'clf__estimator__n_estimators': [50, 100],
        #'clf__estimator__learning_rate': [1,2] 
    }
    
    return GridSearchCV(pipeline, param_grid=parameters)
 
def evaluate_model(model, X_test, Y_test, category_names):
    '''
    ** Predict on a test data and display the results. 
    >> Args:
        modelling - model Machine Learning / pipeline Machine Learning
        X_test - data to get predctions
        y_test - real values
    '''
    Y_predict = model.predict(X_test)
    
    for i, column in enumerate(Y_test.columns):
        Y_true =  Y_test[column].values
        Y_pred =  Y_predict[:, i]
        print(i, column)
        print(classification_report(Y_true, Y_pred))


def save_model(model, model_filepath):
    '''
    ** Saves a model as a pickle file.
    '''
    with open(model_filepath, 'wb') as pickle_file:
        pickle.dump(model, pickle_file)

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()