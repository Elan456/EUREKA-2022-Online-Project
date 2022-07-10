from Recoginition import not_recognize
import pandas as pd
import numpy as np
import random
import tqdm
import multiprocessing as mp

check = not_recognize.check_sent_for_poor_recognition



# for result in tqdm.tqdm([pool.apply(get_sentiment, args=(row,)) for row in all_data]):
#     results.append(result)

def add_if_understand(review):
    clauses = not_recognize.break_conjunctions(not_recognize.nlp(review[0]))
    c = 0
    for sent in clauses:  # If any of the clauses are positive, the whole review is
        if check(sent):
            c = 1
            break
    return np.append(review, c)

if __name__ == "__main__":
    reviews = pd.read_csv("WithSentimentALL.csv").to_numpy()[:, 1:]
    full_reviews = []
    pool = mp.Pool()
    results = []

    for result in tqdm.tqdm(pool.imap_unordered(add_if_understand, reviews), total=len(reviews)):
        results.append(result)

    pd.DataFrame(results, columns=["content", "rating", "clean text", "sentiment", "not understanding"]).to_csv("WithNotUnderstandALL.csv")