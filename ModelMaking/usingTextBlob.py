from textblob import TextBlob
import nltk
import pandas as pd
from textblob.sentiments import NaiveBayesAnalyzer
import time
import tqdm
import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")
"""Necessary for the spacytextblob pipe to be added """
from spacytextblob.spacytextblob import SpacyTextBlob
nlp.add_pipe('spacytextblob')  # Adds sentiment analysis when nlp is used
import multiprocessing as mp


def get_sentiment(row):
    blob = TextBlob(row[0], analyzer=NaiveBayesAnalyzer())
    return [row[0], row[1], blob.sentiment[1]]


def spacy_get_sentiment(row):
    clean_text = row[2]  # Column 2 is the clean text
    try:
        doc = nlp(clean_text)
    except:
        print("ERROR THING IS HERE:", clean_text)
    p = doc._.blob.polarity
    return [row[0], row[1], row[2], p]


def remove_empty_content(all_data):
    filtered_rows = []
    for row in all_data:
        if type(row[2]) is not float:
            filtered_rows.append(row)
    pd.DataFrame(filtered_rows, columns=["content", "rating", "clean text"]).to_csv("Filtered_with_Clean_Text.csv")
    exit()



if __name__ == "__main__":
    all_data = pd.read_csv("Filtered_with_Clean_Text.csv").to_numpy()[:, 1:]

    # print(all_data[:5])
    print(len(all_data))
    #all_data = all_data[np.random.choice(all_data.shape[0], 10000, False), :]  # Takes some random reviews
    #print(all_data[0])
    #print(all_data[-1])
    #print(len(all_data))
    #remove_empty_content(all_data)
    pool = mp.Pool()
    results = []
    # for result in tqdm.tqdm([pool.apply(get_sentiment, args=(row,)) for row in all_data]):
    #     results.append(result)

    for result in tqdm.tqdm(pool.imap_unordered(spacy_get_sentiment, all_data), total=len(all_data)):
        results.append(result)
        # if len(results) % 2000 == 0:  # Saves progress every 1000 results
        #     print(len(results))
        #     pd.DataFrame(results, columns=["content", "rating", "clean text", "sentiment"]).to_csv("WithSentimentNEWALL.csv")

    pd.DataFrame(results, columns=["content", "rating", "clean text", "sentiment"]).to_csv("WithSentimentNEWALL.csv")