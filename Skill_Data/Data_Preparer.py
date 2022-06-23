import pandas as pd
import random
import sys

sentiment_map = {'Negative': 0, 'Positive': 1, 'Compliant': 2}
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn'


def process_df(df):
    """
    Filters the dataframe and creates dataframe which contains
    the fields [reviews.text, reviews.rating, sentiment]
    Rating below 3 and above 3 are taken as negative and positive respectively
    """
    df1 = df[['content', 'star']]
    # exit()
    df1_filtered = df1[df1['star'] != "3.0 out of 5 stars"]
    sentiment_dict = {"1.0 out of 5 stars": 0, "2.0 out of 5 stars": 0, "4.0 out of 5 stars": 1, "5.0 out of 5 stars": 1}
    df1_filtered['sentiment'] = df1_filtered['star'].map(sentiment_dict)
    #print(df1.head())
    #print(df1.tail())
    return df1_filtered


data_files_names = ["skills_review_Business & Finance", "skills_review_Connected Car", "skills_review_Education & Reference", "skills_review_Food & Drink", "skills_review_Games & Trivia", "skills_review_Health & Fitness", "skills_review_Kids", "skills_review_Lifestyle", "skills_review_Local", "skills_review_Movies & TV", "skills_review_Music & Audio", "skills_review_News", "skills_review_Novelty & Humor", "skills_review_Productivity", "skills_review_Shopping", "skills_review_Smart Home", "skills_review_Social", "skills_review_Sports", "skills_review_Travel & Transportation", "skills_review_Utilities", "skills_review_Weather"]

all_data_files = []
for i in range(len(data_files_names)):
    all_data_files.append(process_df(pd.read_csv(data_files_names[i] + ".csv")))
df = pd.concat(all_data_files)
df.to_csv("CombinedProcessed.csv")
print(df.head())
print(df.tail())
print(len(df.index))
