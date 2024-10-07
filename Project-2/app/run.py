import json
import plotly
import pandas as pd
import numpy as np
import re

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar,Layout
import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

        
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

# load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table('EDA', engine)

# load model
model = joblib.load("./cls.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    graphs=[]
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graph_one=[]
    graph_one.append(
        Bar(
                x=genre_names,
                y=genre_counts
            )
        )
    layout_one = Layout(title = 'Distribution of Message Genres',
               yaxis = {'title': "Count"},
                xaxis = {'title': "Genre"}
                )

    graphs.append(dict(data=graph_one, layout=layout_one))
    
    #Show Distribution of different categories
    category_name = list(df.columns[4:])
    category_counts = [np.sum(df[col]) for col in category_name]

    graph_two = []
    graph_two.append(
            Bar(
                x=category_name,
                y=category_counts
            )
        )
    layout_two =  Layout(title = 'Distribution of Message Categories',
                yaxis = {'title': "Count"},
                xaxis = {'title': "Genre"})

    graphs.append(dict(data=graph_two, layout=layout_two))
    
    # extract data exclude related
    categories = df.iloc[:,4:]
    categories_mean = categories.mean().sort_values(ascending=False)[1:11]
    categories_names = list(categories_mean.index)

    graph_three = []
    graph_three.append(
            Bar(
                x=category_name,
                y=category_counts
            )
        )
    layout_three =  Layout(title = 'Top 10 Message Categories',
                yaxis = {
                    'title': "Percentage", 
                    'titlefont': {'color': 'black', 'size': 12}
                },
                xaxis = {
                'title': "Category", 
                'titlefont': {'color': 'black', 'size': 12},
                'tickangle':45
                  }
                )
    
    graphs.append(dict(data=graph_three, layout=layout_three))


    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()