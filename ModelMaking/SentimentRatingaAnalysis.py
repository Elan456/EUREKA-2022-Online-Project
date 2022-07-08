import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import statistics as stat
from scipy.stats import t as sci_t

data = pd.read_csv("WithSentimentALL.csv").to_numpy()

# Index, content, rating, clean_content, sentiment

reviews = {1: [],
           2: [],
           3: [],
           4: [],
           5: []}

x = []
y = []


for r in data:
    if len(r[1]) > 0:
        reviews[r[2]].append(r[4])
        x.append(r[2])
        y.append(r[4])
    else:
        print(r[1], r[4])





sentiment_averages = {}

# 0: 1: Content 2: Rating 3: Sentiment

for rating in reviews:
    s = 0
    for review in reviews[rating]:
        s += review
    sentiment_averages[rating] = s / len(reviews[rating])

line = np.polyfit(x, y, 1)
y_hat = np.poly1d(line)  # Linear regression equation
b, a = y_hat.coeffs
print("slope: ", b)
print("yinter: ", a)

# Statistic's averages
x_bar = stat.mean(x)
y_bar = stat.mean(y)

df = len(x) - 2  # Degrees of freedom

SESlope = math.sqrt(
    sum([(y[i] - y_hat(x[i])) ** 2 for i in range(len(x))]) / df
    ) / math.sqrt(
    sum([(x_value - x_bar) ** 2 for x_value in x])
)

print("Standard Error of Slope: ", SESlope)
print("Degrees of Freedom:", df)
t = (b - 0) / SESlope
print("T: ", t)
p_value = (sci_t.cdf(-1*abs(t), df))
print("Given that there is no linear relationship between rating and sentiment the probabilty of a slope this positive or more positive is", p_value)

print("total # of reviews averaged together: ", sum([len(reviews[a]) for a in reviews]))

# plt.plot(x, y, "o")
plt.xlabel("Sentiment")
plt.ylabel("Frequency in Scientific Notation")
plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
plt.title("Frequency of Sentiments")


# plt.plot(x, [y_hat(a) for a in x], "-g")
# plt.scatter(x, [sentiment_averages[a] for a in x], facecolors="none", edgecolors="r", s=100)
# plt.scatter(x, y)
# plt.boxplot(reviews.values(), flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': (0, 1, 1, 1)})
plt.hist(y, bins=[-1 + .1*v for v in range(20)], edgecolor="black", color=(.59,.15,.96,1), zorder=0)

# plt.hist(x, bins=[.5,1.5,2.5,3.5,4.5,5.5],edgecolor="black", color=(.95, .4, .2, 1), zorder=1)
plt.savefig("SentimentHistogram.png")
plt.show()
