'''Function to train a model to classify disaster messages.
Usage: `python train_classifier.py <database_filepath> <model_filepath>`
'''

# import libraries
import sys
import re
import pickle
import pandas as pd
from sqlalchemy import create_engine

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split, GridSearchCV


import nltk
nltk.download(['punkt', 'wordnet']) 
# (In MacOS) if you encounter the hanging nltk download, uncomment the following line
# nltk.download('all')


def load_data(database_filepath):
    """
    Loads data from SQLite database.
    
    Args:
        database_filepath: Filepath to the database
    
    Returns:
        X: Features
        Y: Target
        category_names: Target names
    """
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    # Default name to EDA
    df = pd.read_sql_table('EDA', engine)
    X = df.message
    y = df[df.columns[4:]]
    category_names = y.columns
    return X, y, category_names


def tokenize(text):
    """
    Tokenizes and lemmatizes text.
    
    Args:
        text: Text to be tokenized
    
    Returns:
        new_tokens: Returns cleaned tokens 
    """
    lemmatizer = WordNetLemmatizer()
    # normalize case and remove punctuation
    text = re.sub(r"[^A-Za-z0-9]",' ',text)

    tokenized_text = word_tokenize(text)

    new_tokens = []
    for token in tokenized_text:
        token = str(token).lower().strip()
        token = lemmatizer.lemmatize(token).strip()
        new_tokens.append(token)

    return new_tokens


def build_model():
    """
    Builds classifier and tunes model using GridSearchCV.
    
    Returns:
        cv: Classifier 
    """

    pipeline = Pipeline([
        ('vt', CountVectorizer(tokenizer=tokenize)),
        ('tf-idf', TfidfTransformer()),
        ('cls', MultiOutputClassifier(RandomForestClassifier()))
    ])
    
    parameters = {
        #'tf-idf__use_idf': (True, False),
        'cls__estimator__n_estimators': [50, 100],
        'cls__estimator__min_samples_split': [2, 3, 4],
        #'vt__max_df': (0.5, 0.75, 1.0),
        #'vt__max_features': (None, 5000, 10000),
    }

    cv = GridSearchCV(pipeline, param_grid=parameters, verbose=2)
    
    return cv


def evaluate_model(model, X_test, y_test):
    """
    Evaluates the performance of model and returns classification report. 
    
    Args:
        model: classifier
        X_test: test dataset
        Y_test: labels for test data in X_test
    
    Returns:
        None
    """
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    print('Accuracy: ', accuracy)
    print('--------------------------------------')
    print('Classification Report:')
    print('--------------------------------------')
    for i in range(10):
        print(y_test.columns[i])
        print(classification_report(y_test.iloc[:,i], y_pred[:,i]))

        
def save_model(model, model_filepath):
    """ Exports the final model as a pickle file.
    
    Args:
        model: classifier
        model_filepath: Filepath to save the model

    Returns:
        None
    """
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    """ Builds the model, trains the model, evaluates the model, saves the model."""
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, _ = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test)

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