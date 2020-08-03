from flask import Flask, render_template, redirect, request, jsonify, send_file
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter

app = Flask(__name__)
nlp = spacy.load('en_core_web_md')
stopwords = list(STOP_WORDS)
pos_tag = ['PROPN', 'ADJ', 'NOUN']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/spam', methods=["GET", "POST"])
def spam():
    s=request.form.get("usertext")
    s=str(s)
    doc = nlp(s)
    keyword = []
    label=[]
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.lemma_.capitalize())
            print(token.text,token.pos_)
    for token in doc.ents:
        if(token.label_ == 'ORG'):
            label.append(token.text.capitalize())
        print(token.text,token.label_)
    freq_word = Counter(keyword).most_common(5)
    spam=[]
    for i in range(5):
        spam.append(freq_word[i][0])
    #spam=[max(label)]+spam
    return render_template("result.html",li=spam[:5])


if __name__ == "__main__":
    app.debug = True
    app.run()
