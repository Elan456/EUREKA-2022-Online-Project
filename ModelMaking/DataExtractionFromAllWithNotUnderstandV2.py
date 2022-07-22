import pandas as pd
import numpy as np


df = pd.read_csv("ALLWithNotUnderstandV2.csv").to_numpy()[:, 1:]
print("number of reivews:", len(df))
c = 0
num_of_negative_reviews = 0
for review in df:
    if review[1] <= 3:
        if review[4] == 1:
            c += 1
        num_of_negative_reviews += 1

print("c:", c)
print("number of negative reviews:", num_of_negative_reviews)
print("c/num_negative_reviews", c/num_of_negative_reviews)
