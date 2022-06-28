import pandas as pd
import random

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
    df1['star'] = df1['star'].apply(lambda x: int(x[0]))

    df1 = df1[df1["content"].str.len().gt(2)]
    return df1


data_files_names = ["skills_review_BusinessFinance", "skills_review_Connected Car", "skills_review_EducationReference", "skills_review_FoodDrink", "skills_review_GamesTrivia", "skills_review_HealthFitness", "skills_review_Kids", "skills_review_Lifestyle", "skills_review_Local", "skills_review_MoviesTV", "skills_review_MusicAudio", "skills_review_News", "skills_review_NoveltyHumor", "skills_review_Productivity", "skills_review_Shopping", "skills_review_Smart Home", "skills_review_Social", "skills_review_Sports", "skills_review_TravelTransportation", "skills_review_Utilities", "skills_review_Weather"]

all_data_files = []
for i in range(len(data_files_names)):
    all_data_files.append(process_df(pd.read_csv("..\\Skill_Data\\" + data_files_names[i] + ".csv")))
df = pd.concat(all_data_files)
df.to_csv("CombinedProcessed.csv")
print(df.head())
print(df.tail())
print(len(df.index))
