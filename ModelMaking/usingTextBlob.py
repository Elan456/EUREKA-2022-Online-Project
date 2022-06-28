from textblob import TextBlob
import nltk
import pandas as pd
from textblob.sentiments import NaiveBayesAnalyzer
import time
import tqdm
import numpy as np

import multiprocessing as mp

def get_sentiment(row):
    blob = TextBlob(row[0], analyzer=NaiveBayesAnalyzer())
    return [row[0], row[1], blob.sentiment[1]]


if __name__ == "__main__":
    all_data = pd.read_csv("CombinedProcessed.csv").to_numpy()
    print(len(all_data))
    all_data = all_data[:, 1:]
    all_data = all_data[np.random.choice(all_data.shape[0], 10000, False), :]  # Takes some random reviews
    print(all_data[0])
    print(all_data[-1])
    print(len(all_data))
    pool = mp.Pool()
    results = []
    # for result in tqdm.tqdm([pool.apply(get_sentiment, args=(row,)) for row in all_data]):
    #     results.append(result)

    for result in tqdm.tqdm(pool.imap_unordered(get_sentiment, all_data), total=len(all_data)):
        results.append(result)
        if len(results) % 1000 == 0:  # Saves progress every 1000 results
            pd.DataFrame(results, columns=["content", "rating", "positivity"]).to_csv("WithSentiment10000random.csv")

    pd.DataFrame(results, columns=["content", "rating", "positivity"]).to_csv("WithSentiment10000random.csv")