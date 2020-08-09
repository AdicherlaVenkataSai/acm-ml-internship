import numpy as np
import pandas as pd
from flask import Flask, render_template, request

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel



def abc():
    data = pd.read_csv('final.csv')
    tfv = TfidfVectorizer(min_df = 3, max_features = None, strip_accents = 'unicode', analyzer = 'word', token_pattern = r'\w{1,}', ngram_range = (1, 3), stop_words = 'english')
    tfv_matrix = tfv.fit_transform(data['DESCRIPTION'])
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    indices = pd.Series(data.index, index = data['TRACK NAME']).drop_duplicates()
    
    return data, sig, indices

def get_rec(title):
    
    data, sig, indices = abc()    
    if title not in data['TRACK NAME'].unique():
        return(" OOPS! we haven't kept the track of these movie.\n Please check if you spelled it correctly or not")
        
    else:
        idx = indices[title]
        sig_scores = list(enumerate(sig[idx])
        sig_scores = sorted(sig_scores, key = lamnda x: x[1], reverse = True)
        sig_scores = sig_scores[1: 11]
        
        l = []
        for i in sig_scores:
            a = sig_scores[i][0]
            l.append(data['TRACK NAME'][a]
        
        return l
    
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')
 
@app.route("/results")

def results():

    title = request.args.get('title')
    r = get_rec(title)
    title = title.upper()
    if type(r) == type('string'):
        return render_template('results.html', movie = title, r = r, t = 's')
    
    else:
        return render_template('results.html', movie = title , r = r, t = 'l')
        

if __name__ == "__main__":
    app.run(debug = True)