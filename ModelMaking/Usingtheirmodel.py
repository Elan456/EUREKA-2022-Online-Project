import pickle
import pandas as pd
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
sys.path.append(r"C:\Users\Ethan\PycharmProjects\EUREKA_2022_Online_Project\abin08_SentimentAnalysis")
import text_processor as tp

sia = SentimentIntensityAnalyzer()
sentiment_map = {'Negative':0, 'Positive':1, 'Compliant':2}

model = pickle.load(open(r"..\abin08_SentimentAnalysis\pickles\amazon\mnb_classifier.pickle", "rb"))
tfidf = pickle.load(open(r"..\abin08_SentimentAnalysis\pickles\amazon\tfidf.pickle", "rb"))
def get_sentiment(text):
    """
    Predicts the sentiment of text using the Multinomial Naive Bayes Model
    """
    sentiment_id = model.predict(tfidf.transform([text]))
    return get_name(sentiment_id)


def get_name(sentiment_id):
    """
    Gets sentiment name from sentiment_map using sentiment_id
    """
    for sentiment, id_ in sentiment_map.items():
        if id_ == sentiment_id:
            return sentiment

def top_pos_word(text):
    """
    Finds top positive word using nltk vader library
    """
    pos_polarity = dict()
    for word in tp.get_tokens(text):
        pos_score = sia.polarity_scores(word)['pos']
        if word not in pos_polarity:
            pos_polarity[word] = pos_score
        else:
            pos_polarity[word] += pos_score
    top_word = max(pos_polarity, key=pos_polarity.get)
    return top_word

def top_neg_word(text):
    """
    Finds top negative word using nltk vader library
    """
    neg_polarity = dict()
    for word in tp.get_tokens(text):
        neg_score = sia.polarity_scores(word)['neg']
        if word not in neg_polarity:
            neg_polarity[word] = neg_score
        else:
            neg_polarity[word] += neg_score
    top_word = max(neg_polarity, key=neg_polarity.get)
    return top_word


def get_noun(text):
    """
    Finds noun of the text
    """
    tokenizer = ToktokTokenizer()
    tokens = tokenizer.tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    nouns = []
    for word, tag in pos_tags:
        if tag == "NN" or tag == "NNP" or tag == "NNS":
            nouns.append(word)
    return nouns


def sentiment_analysis(text, text_already_clean=False, print_stuff=True):
    """
    Finds the sentiment of text, prints positive or negative word and
    prints the causing words of positivity or negativity
    """
    if not text_already_clean:
        text = tp.clean_text(text)
    sentiment = get_sentiment(text)
    if print_stuff:
        print(f'Sentiment: {sentiment}')
        if sentiment == 'Positive':
            nouns = get_noun(text)
            print(f'Positive word: {top_pos_word(text)}')
            print(f'Cause of positivity: {nouns}')
        elif sentiment == 'Negative':
            nouns = get_noun(text)
            print(f'Negative word: {top_neg_word(text)}')
            print(f'Cause of negativity: {nouns}')
    return sentiment

sentiment_analysis("I hate this product. I returned it instantly")
sentiment_analysis("it loads my books proper. worked on the first try erasing an dreregistering. screen perfectly dark")
sentiment_analysis("This is amazing love 100%")