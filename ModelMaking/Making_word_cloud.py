import wordcloud
import pandas as pd
import numpy as np
wc = wordcloud.WordCloud(width=800, height=400, background_color=(255, 255, 255))

text = ""

reviews = pd.read_csv("WithNotUnderstandALL.csv").to_numpy()[:, 1:]
for r in reviews:
    if r[4] == 1:  # Understanding is 1
        text += r[2]  # Adds clean text to text
        # print(text)

wc.generate(text)
wc.to_file("wordcloud.png")