import wordcloud
import pandas as pd
import random
import numpy as np

wc = wordcloud.WordCloud(width=400, height=800, background_color=(35, 47, 62))

color_list = [
    (5, 160, 209),
    (20, 180, 220),
    (136, 188, 204),
    (172, 194, 201)



]

def random_color(*args, **kwargs):
    return random.choice(color_list)


text = ""

reviews = pd.read_csv("ALLWithNotUnderstandV2.csv").to_numpy()[:, 1:]
about_understanding = []

for r in reviews:
    if r[4] == 1:  # Understanding is 1
        about_understanding.append(r)
        text += r[2]  # Adds clean text to text
        # print(text)

# for i, c in enumerate(check_reviews):
#     review = about_understanding[c]
#     reviews_1.append([review[0], review[4]])
#
# pd.DataFrame(reviews_1, columns=["Content", "WW"]).to_csv("AccuracyCheck.csv")
wc.generate(text)
wc.recolor(color_func=random_color)
wc.to_file("wordcloudALLVECTOR.pdf")
