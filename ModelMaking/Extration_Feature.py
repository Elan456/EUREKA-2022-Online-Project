"""Cleans all the content from CombinedProcessed.csv and saves it as SuperProcessed.csv"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from multiprocessing import Pool
import sys
pd.set_option('display.max_columns', None)
sys.path.append(r"C:\Users\Ethan\PycharmProjects\EUREKA_2022_Online_Project\abin08_SentimentAnalysis")
import text_processor as tp


def process_txt(df):
    """
    Apply clean_text method of text_processor in the column 'content'
    """
    df['cleaned_text'] = df['content'].apply(tp.clean_text)
    return df


data_set = pd.read_csv("CombinedProcessed.csv")
print(data_set.head())


data_set = process_txt(data_set)
data_set.to_csv("SuperProcessed.csv")
print(data_set.head())
print(data_set.shape)
